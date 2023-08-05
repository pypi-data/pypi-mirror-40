from enum import Enum, unique
from typing import Union, Sequence


@unique
class Mode(Enum):
    FAN = 0
    COOL = 1
    DEHUMID = 2
    HEAT = 3
    WARM = 4


@unique
class FanMode(Enum):
    LOW = 1
    MID = 2
    HIGH = 3


@unique
class SwitchStatus(Enum):
    ON = 1
    OFF = 0


class ACStatus:
    def __init__(self, ac_id: int, switch_status: SwitchStatus, fan_mode: FanMode, target_temperature: int,
                 current_temperature: int, mode: Mode):
        self.ac_id: int = ac_id
        self.switch_status: SwitchStatus = switch_status
        self.fan_mode: FanMode = fan_mode
        self.target_temperature: int = target_temperature
        self.current_temperature: int = current_temperature
        self.mode: Mode = mode

    def __repr__(self):
        return str.format("""
        ac_id:{}
        switch:{}
        mode:{}
        target_temperature:{}
        current_temperature:{}
        fan_mode:{}
        """, self.ac_id, self.switch_status.name, self.mode, self.target_temperature,
                          self.current_temperature,
                          self.fan_mode.name)


__PACKET_TYPE_POS = 1
__PACKET_LENGTH = 218
__PAGE_NUM_POS = 14
__FIRST_AC_UNIT_ID_POS = 21  # to 217 each length:12
__ANDROID_ID_START_POS = 9


def getACUnitNum(data: bytes):
    return 16


def _getDeviceUnitIdPos(i):
    return __FIRST_AC_UNIT_ID_POS + i * 12


def _getDeviceModePOS(i):
    return _getDeviceUnitIdPos(i) + 1


def _getDeviceTemperaturePOS(i):
    return _getDeviceUnitIdPos(i) + 2


def _getCurrentTemperaturePos(i):
    return _getDeviceUnitIdPos(i) + 3


def _getOutsideTemperaturePos(i):
    return _getDeviceUnitIdPos(i) + 4


def _getDeviceWindLevelPos(i):
    return _getDeviceUnitIdPos(i) + 5


def _getDeviceStatusPos(data, i):
    ACUnitTypePos = _getACUnitTypePos(i)
    ACUnitType = data[ACUnitTypePos]
    if ACUnitType == 0:  # Otherwise the device/packet is broken.
        return _getDeviceUnitIdPos(i) + 6


def _getACUnitTypePos(i):
    return _getDeviceUnitIdPos(i) + 7


def _getOnTimerHPos(i):
    return _getDeviceUnitIdPos(i) + 8


def _getOnTimerMPos(i):
    return _getDeviceUnitIdPos(i) + 9


def _getOffTimerHPos(i):
    return _getDeviceUnitIdPos(i) + 10


def _getOffTimerMPos(i):
    return _getDeviceUnitIdPos(i) + 11


def getClientId(data):
    androidIdBytes = bytes([data[__ANDROID_ID_START_POS + i] for i in range(0, 4)])
    return int.from_bytes(androidIdBytes, byteorder='little')


def getDeviceUnitId(data, i):
    return data[_getDeviceUnitIdPos(i)]


def getDeviceMode(data, i) -> Union[Mode, None]:
    modeRaw = data[_getDeviceModePOS(i)]
    if modeRaw is not None:
        return Mode(modeRaw)


def getTargetTemperature(data, i):
    return data[_getDeviceTemperaturePOS(i)]


def getCurrentTemperature(data, i):
    return data[_getCurrentTemperaturePos(i)]


def getOutsideTemperature(data, i):
    return data[_getOutsideTemperaturePos(i)]


def get_device_fan_mode(data, i) -> Union[FanMode, None]:
    windLevel = data[_getDeviceWindLevelPos(i)]
    return FanMode(windLevel)


def getDeviceStatus(data, i):
    deviceStatusPos = _getDeviceStatusPos(data, i)
    if deviceStatusPos is not None:  # Otherwise device/packet is broken
        return data[deviceStatusPos]


def getACUnitType(data, i):
    return data[_getACUnitTypePos(i)]


def getOnTimerH(data, i):
    h = data[_getOnTimerHPos(i)]
    if h in range(0, 24):
        return h
    else:
        return None


def getOnTimerM(data, i):
    m = data[_getOnTimerMPos(i)]
    if m in range(0, 24):
        return m
    else:
        return None


def getOffTimerH(data, i):
    h = data[_getOffTimerHPos(i)]
    if h in range(0, 24):
        return h
    else:
        return None


def getOffTimerM(data, i):
    m = data[_getOffTimerMPos(i)]
    if m in range(0, 24):
        return m
    else:
        return None


def header() -> bytes:
    domain = 1  # 1 LAN 2 WAN
    rsv = 0
    sequence = 1
    type = 5
    clientId = 4294967295  # Client Id
    gatewayId = 0  # Id of first Unit

    header = bytearray()
    header += domain.to_bytes(1, byteorder='little')
    header += type.to_bytes(1, byteorder='little')
    header += sequence.to_bytes(2, byteorder='little')
    header += clientId.to_bytes(4, byteorder='little')
    header += gatewayId.to_bytes(4, byteorder='little')
    header += rsv.to_bytes(4, byteorder='little')

    return header


def content(payload: bytes) -> bytes:
    payload_length = int(len(payload) + 2).to_bytes(2, byteorder='little')
    crc16le = int(0).to_bytes(2, byteorder='little')  # To implement
    return payload_length + payload + crc16le


def poll_payload() -> bytes:
    return bytes([204, 170, 136])


def poll_packet() -> bytes:
    return header() + content(poll_payload())


def change_status_payload(unit_id, switch, mode, temperature,
                          wind_level: FanMode, timer_on_h, timer_on_m, timer_off_h, timer_off_m) -> bytes:
    payload = bytes([187, 170])
    payload += unit_id.to_bytes(length=1, byteorder='little')
    payload += mode.value.to_bytes(length=1, byteorder='little')
    payload += temperature.to_bytes(length=1, byteorder='little')
    payload += wind_level.value.to_bytes(length=1, byteorder='little')
    payload += switch.value.to_bytes(length=1, byteorder='little')
    payload += timer_on_h.to_bytes(length=1, byteorder='little')
    payload += timer_on_m.to_bytes(length=1, byteorder='little')
    payload += timer_off_h.to_bytes(length=1, byteorder='little')
    payload += timer_off_m.to_bytes(length=1, byteorder='little')

    tail = bytes([86, 136, 187, 170])
    payload += tail

    return payload


def commandPacket(unit_id, switch, mode, temperature,
                  wind_level: FanMode, timer_on_h: int = 255, timer_on_m=255, timer_off_h=255,
                  timer_off_m=255) -> bytes:
    return header() + content(
        change_status_payload(unit_id, switch, mode, temperature,
                              wind_level, timer_on_h, timer_on_m, timer_off_h, timer_off_m)
    )
