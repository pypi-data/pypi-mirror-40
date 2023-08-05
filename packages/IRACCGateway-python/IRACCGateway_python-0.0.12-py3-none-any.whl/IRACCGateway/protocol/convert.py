from typing import *
from . import *


def fromRaw(data: bytes) -> Sequence[ACStatus]:
    n = getACUnitNum(data)
    rtn = []
    for i in range(n):
        id = i
        ac_status = ACStatus(ac_id=id,
                             target_temperature=getTargetTemperature(data, id),
                             current_temperature=getCurrentTemperature(data, id),
                             switch_status=SwitchStatus(getDeviceStatus(data, id)),
                             fan_mode=FanMode(get_device_fan_mode(data, id)),
                             mode=Mode(getDeviceMode(data, id))
                             )
        rtn.append(ac_status)

    return rtn
