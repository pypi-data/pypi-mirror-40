import socket, logging, time
from typing import *

from . import protocol
from .protocol import convert

BUFFER_SIZE = 1024

_remote_ip = None
_remote_port = None
_remote_poll_port = 40111

_fetch_timeout = 3
_push_timeout = 3
_discover_timeout = 3

_fetch_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_fetch_soc.settimeout(_fetch_timeout)
_fetch_soc_port = _fetch_soc.getsockname()[1]

_logger = logging.getLogger(__name__)

while _fetch_soc_port == _remote_port:
    _fetch_soc.close()
    _fetch_soc.bind(('', 0))


def set_fetch_timeout(timeout: int = _fetch_timeout):
    global _fetch_timeout
    _fetch_timeout = timeout
    _fetch_soc.settimeout(timeout)


def set_push_timeout(timeout: int = _push_timeout):
    global _push_timeout
    _push_timeout = timeout


def set_discover_timeout(timeout: int = _discover_timeout):
    global _discover_timeout
    _discover_timeout = timeout


def connect() -> Sequence[protocol.ACStatus]:
    global _remote_ip, _remote_port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as soc:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        soc.settimeout(_discover_timeout)

        poll_packet = protocol.poll_packet()
        soc.sendto(poll_packet, ('255.255.255.255', _remote_poll_port))
        data, addr = soc.recvfrom(BUFFER_SIZE)
        _remote_ip, _remote_port = addr

    return protocol.convert.fromRaw(data)


def reconnect():
    return connect()


def push_status(new_status: protocol.ACStatus) -> Sequence[protocol.ACStatus]:
    command = protocol.commandPacket(unit_id=new_status.ac_id,
                                     switch=new_status.switch_status,
                                     mode=new_status.mode,
                                     temperature=new_status.target_temperature,
                                     wind_level=new_status.fan_mode,
                                     )

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as soc:
        soc.settimeout(_push_timeout)
        soc.sendto(command, (_remote_ip, _remote_port))
        result = soc.recv(BUFFER_SIZE)

    return protocol.convert.fromRaw(result)


def fetch_status() -> Sequence[protocol.ACStatus]:
    query = protocol.poll_packet()
    _fetch_soc.sendto(query, (_remote_ip, _remote_port))
    data = _fetch_soc.recv(BUFFER_SIZE)

    return protocol.convert.fromRaw(data)


def fetch_outside_temperature() -> int:
    query = protocol.poll_packet()
    _fetch_soc.sendto(query, (_remote_ip, _remote_port))
    data = _fetch_soc.recv(BUFFER_SIZE)

    return protocol.getOutsideTemperature(data, 0)
