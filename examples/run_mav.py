# import asyncio
#
# from mavcom.mavlink.component import Component, mavlink
# from mavcom.mavlink.mavcom import MAVCom
#
#
# def on_message(message):
#     print(f"on_message: {message}")
#     return True  # Return True to indicate that command was ok and send ack
#
#
# class Cam1(Component):
#     def __init__(self, source_component, mav_type, debug=False):
#         super().__init__(source_component=source_component, mav_type=mav_type)
#         self._set_message_callback(on_message)
#
#
# class Cam2(Component):
#     def __init__(self, source_component, mav_type, debug=False):
#         super().__init__(source_component=source_component, mav_type=mav_type)
#         self._set_message_callback(on_message)
#
#
# class Cli(Component):
#     def __init__(self, source_component, mav_type, debug=False):
#         super().__init__(source_component=source_component, mav_type=mav_type)
#         self._set_message_callback(on_message)
#
#
# async def run_test_client_server(con1="udpin:localhost:14445", con2="udpout:localhost:14445"):
#     with MAVCom(con1, source_system=111) as client:
#         with MAVCom(con2, source_system=222) as server:
#
#             client.add_component(Cli(mav_type=mavlink.MAV_TYPE_GCS, source_component=11))
#             server.add_component(Cam1(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=22))
#             server.add_component(Cam1(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=23))
#
#             for key, comp in client.component.items():
#                 # result = await comp.wait_heartbeat(target_system=222, target_component=22)
#                 result = await comp.wait_heartbeat(remote_mav_type=mavlink.MAV_TYPE_CAMERA, target_system=222,
#                                                    target_component=22)
#                 print(f"Component {comp}, Heartbeat: {result = }")
#
#             Num_Iters = 3
#             for i in range(Num_Iters):
#                 await client.component[11]._test_command(222, 22, 1)
#
#                 await client.component[11]._test_command(222, 23, 1)
#
#             await client.component[11]._test_command(222, 24, 1)
#
#     return client, server, Num_Iters
#
#
# if __name__ == '__main__':
#     client, server, Num_Iters = asyncio.run(
#         run_test_client_server(con1="udpin:localhost:14445", con2="udpout:localhost:14445"))
#     # client, server, Num_Iters = run_test_client_server(con1="udpin:localhost:14445", con2="udpout:localhost:14445")
#     # client, server, Num_Iters = run_test_client_server(con1="/dev/ttyACM0", con2="/dev/ttyUSB0")
#
#     print(f"{server.source_system = };  {server.message_cnts = }")
#     print(f"{client.source_system = };  {client.message_cnts = }")
#     print()
#     print(f"{client.source_system = } \n{client.summary()} \n")
#     print(f"{server.source_system = } \n{server.summary()} \n")
#
#     assert client.component[11].num_cmds_sent == Num_Iters * 2 + 1
#     print(f"{server.component[22].message_cnts[111]['COMMAND_LONG'] = }")
#     assert server.component[22].message_cnts[111]['COMMAND_LONG'] == Num_Iters
#     assert client.component[11].num_acks_rcvd == Num_Iters * 2
#     assert client.component[11].num_acks_drop == 1
#     assert server.component[22].num_cmds_rcvd == Num_Iters
#     assert server.component[23].num_cmds_rcvd == Num_Iters
#
# if __name__ == '__main__':
#     print("Done")
import time

from mavcom.mavlink import Component, MAVCom, mavlink

"""Test MAVCom with a client and server on the same machine using UDP ports `14445`  with `server_system_ID=111, client_system_ID=222`"""
with MAVCom("udpin:localhost:14445", source_system=111) as client:
    with MAVCom("udpout:localhost:14445", source_system=222) as server:
        server.add_component(Component(mav_type=mavlink.MAV_TYPE_CAMERA, source_component=22, loglevel=10))
        client.add_component(Component(mav_type=mavlink.MAV_TYPE_GCS, source_component=11, loglevel=10))

        MAX_PINGS = 4
        client.component[11].send_ping(222, 22)
        time.sleep(0.5)
