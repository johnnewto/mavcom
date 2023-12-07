import asyncio
import time

from mavcom.mavlink import MAVCom, mavlink
from mavcom.mavlink.component import Component


def on_message(msg):
    try:
        print(f"on_message:  {msg.get_msgId() = } source sys/cmp = {msg.get_srcSystem()}/{msg.get_srcComponent()} target sys/cmp = {msg.target_system}/{msg.target_component}: {msg}")
    except:
        print(f"on_message:  {msg.get_msgId() = } source sys/cmp = {msg.get_srcSystem()}/{msg.get_srcComponent()} : {msg}")
        pass
    return False  # Return True to indicate that command was ok and send ack


class Cam1(Component):
    def __init__(self, source_component, mav_type, loglevel=20):
        super().__init__(source_component=source_component, mav_type=mav_type, loglevel=loglevel)
        self.append_message_handler(on_message)


class Cli(Component):
    def __init__(self, source_component, mav_type, loglevel=20):
        super().__init__(source_component=source_component, mav_type=mav_type, loglevel=loglevel)
        # self._set_message_callback(on_message)


con1, con2 = "udpin:localhost:14445", "udpout:localhost:14445"
# con1, con2 = "/dev/ttyACM0", "/dev/ttyUSB1"
# con2, con1 = "/dev/ttyACM0", "/dev/ttyACM2"

async def main():
    with MAVCom(con1, source_system=111, loglevel=10) as gcs_mavlink:
        with MAVCom(con2, source_system=222, loglevel=10) as drone_mavlink:
            gcs_cam_manager = gcs_mavlink.add_component(Cli(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=11, loglevel=10))
            drone_mavlink.add_component(Cam1(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=22, loglevel=10))
            # gcs_cam_manager = gcs_mavlink.add_component(CameraClient(mav_type=mavlink.MAV_TYPE_GCS, source_component=11, loglevel=10))
            # drone_mavlink.add_component(Cam1(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=22))

            result = await gcs_cam_manager.wait_heartbeat(remote_mav_type=mavlink.MAV_TYPE_CAMERA, target_system=222, target_component=22, timeout=2)
            print(f"Component {gcs_cam_manager}, Heartbeat: {result = }")

            Num_Iters = 10
            for i in range(Num_Iters):
                await gcs_cam_manager.test_command(222, 22, 1)
                # await gcs_cam_manager.video_start_streaming(222, 22)

                time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
