"""
Request a message from a flight controller (e.g. PX4) using the MAV_CMD_REQUEST_MESSAGE command.
Here we request  MAVLINK_MSG_ID_RC_CHANNELS. The message is sent to the FC using the MAVLink protocol.
on receiving the message use chan7_raw to trigger the camera to take snapshots
The message is sent to the FC using the Yappu protocol.
"""

import asyncio
import time

from mavcom.mavlink import MAVCom, mavlink, Component
from mavcom.utils import find_uart_devices

mav_connection = find_uart_devices()[0].device


def on_message(msg: mavlink.MAVLink_message):
    """
    Handle the incoming MAVLink message.
    """
    # print(msg)
    if msg.get_type() in ['STATUSTEXT']:
        print(f"***** RC {msg}")

async def main():
    # assume that you want to create a compontent that is a camera on a UAV
    with MAVCom(mav_connection, source_system=222, loglevel=20) as mav_server:
        mav_server.on_message = on_message

        # cam_0 = GSTCamera(server_config_dict, camera_dict=toml_load(config_dir() / "test_cam_0.toml"), loglevel=LogLevels.DEBUG)
        comp: Component = mav_server.add_component(Component(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=mavlink.MAV_COMP_ID_CAMERA, loglevel=20))
        ret = await comp.wait_heartbeat(target_system=1, target_component=1, timeout=5)  # from FC
        print(f"Heartbeat {ret = }")
        cam_snapping = False
        while True:
            msg = await comp.request_message(msg_id=mavlink.MAVLINK_MSG_ID_RC_CHANNELS, target_system=1, target_component=1)
            # print(f"request_message {msg}")
            if msg == mavlink.MAVLINK_MSG_ID_RC_CHANNELS:
                print(f"request_message {msg}")
                if msg.chancount == 0:
                    print("RC might not be connected")
            if msg is not None:
                # RC channel 7 switch is used to trigger the message
                print(f"{msg.chan7_raw = }  ", end='')
                print(f"RC_CHANNELS: chancount = {msg.chancount}: {msg.chan1_raw}, {msg.chan2_raw}, {msg.chan3_raw}, {msg.chan4_raw}, {msg.chan5_raw}, {msg.chan6_raw}, {msg.chan7_raw}, {msg.chan8_raw}, {msg.chan9_raw}, {msg.chan10_raw}, {msg.chan11_raw}, {msg.chan12_raw}, {msg.chan13_raw}, {msg.chan14_raw}, {msg.chan15_raw}, {msg.chan16_raw}, {msg.chan17_raw}, {msg.chan18_raw}")

                if msg.chan7_raw > 1200:
                    if not cam_snapping:
                        text = f"Camera taking snapshots: {msg.chan7_raw}"
                        comp.master.mav.statustext_send(mavlink.MAV_SEVERITY_INFO, text=text.encode("utf-8"))
                        print(f"Start Sent ")
                        comp.send_ping(target_system=1, target_component=1)

                    cam_snapping = True

                else:
                    if cam_snapping:
                        text = f"Camera stopped taking snapshots: {msg.chan7_raw}"
                        comp.master.mav.statustext_send(mavlink.MAV_SEVERITY_INFO, text=text.encode("utf-8"))
                        print(f"Stop Sent ")
                        comp.send_ping(target_system=1, target_component=1)
                    cam_snapping = False

                    # await comp.send_command(target_system=1, target_component=1, command_id=mavlink.MAV_CMD_DO_SET_MODE, params=[mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 0, 0, 0, 0, 0, 0])
                    # print(f"Sent {mavlink.MAV_CMD_DO_SET_MODE} {mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED}")
            time.sleep(0.01)



if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
