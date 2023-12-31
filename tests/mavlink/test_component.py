# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/api/21_mavlink.component.ipynb.

# %% auto 0
__all__ = ['MAV_TYPE_GCS', 'MAV_TYPE_CAMERA', 'Cam1', 'Cam2', 'Cli', 'test_ack']

# %% ../../nbs/api/21_mavlink.component.ipynb 9
import os

# os.environ['MAVLINK20'] == '1' should be placed in mavcom.__init__.py
assert os.environ[
           'MAVLINK20'] == '1', "Set the environment variable before from pymavlink import mavutil  library is imported"

from nbdev.showdoc import *
from fastcore.test import *


# %% ../../nbs/api/21_mavlink.component.ipynb 10
from mavcom.mavlink.component import *

# %% ../../nbs/api/21_mavlink.component.ipynb 23
from mavcom.mavlink.component import BaseComponent, mavutil
from mavcom.mavlink.mavcom import MAVCom

MAV_TYPE_GCS = mavutil.mavlink.MAV_TYPE_GCS
MAV_TYPE_CAMERA = mavutil.mavlink.MAV_TYPE_CAMERA

class Cam1(BaseComponent):
    def __init__(self, source_component, mav_type, debug=False):
        super().__init__(source_component=source_component, mav_type=mav_type,
                         debug=debug)

class Cam2(BaseComponent):
    def __init__(self, source_component, mav_type, debug=False):
        super().__init__(source_component=source_component, mav_type=mav_type,
                         debug=debug)
class Cli(BaseComponent):
    def __init__(self, source_component, mav_type, debug=False):
        super().__init__(source_component=source_component, mav_type=mav_type,
                         debug=debug)

def test_ack():
    """Test sending a command and receiving an ack from client to server"""
    with MAVCom("udpin:localhost:14445", source_system=111, debug=False) as client:
        with MAVCom("udpout:localhost:14445", source_system=222, debug=False) as server:
            client.add_component(Cli(mav_type=MAV_TYPE_GCS, source_component = 11, debug=False))
            server.add_component(Cam1(mav_type=MAV_TYPE_CAMERA, source_component = 22, debug=False))
            server.add_component(Cam1(mav_type=MAV_TYPE_CAMERA, source_component = 23, debug=False))
            
            for key, comp in client.component.items():
                if comp.wait_heartbeat(target_system=222, target_component=22, timeout=0.1):
                    print ("*** Received heartbeat **** " )
            NUM_TO_SEND = 2
            for i in range(NUM_TO_SEND):
                client.component[11]._test_command(222, 22, 1)
                client.component[11]._test_command(222, 23, 1)
                
            client.component[11]._test_command(222, 24, 1)
    
        print(f"{server.source_system = };  {server.message_cnts = }")
        print(f"{client.source_system = };  {client.message_cnts = }")
        print()
        print(f"{client.source_system = } \n{client.summary()} \n")
        print(f"{server.source_system = } \n{server.summary()} \n")
    
        assert client.component[11].num_cmds_sent == NUM_TO_SEND * 2 + 1
        assert client.component[11].num_acks_rcvd == NUM_TO_SEND * 2
        assert client.component[11].num_acks_drop == 1
        assert server.component[22].num_cmds_rcvd == NUM_TO_SEND
        assert server.component[23].num_cmds_rcvd == NUM_TO_SEND
        
test_ack()
