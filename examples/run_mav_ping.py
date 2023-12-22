
import time

from mavcom.mavlink import Component, MAVCom, mavlink
from mavcom.logging import LogLevels

"""Test MAVCom with a client and server on the same machine using UDP ports `14445`  with `server_system_ID=111, client_system_ID=222`"""
with MAVCom("udpin:localhost:14445", source_system=111) as client:
    with MAVCom("udpout:localhost:14445", source_system=222) as server:
        server.add_component(Component(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=22, loglevel=LogLevels.DEBUG))
        client.add_component(Component(mav_type=mavlink.MAV_TYPE_GCS, source_component=11, loglevel=LogLevels.DEBUG))

        MAX_PINGS = 4
        client.component[11].send_ping(222, 22)
        time.sleep(0.5)
