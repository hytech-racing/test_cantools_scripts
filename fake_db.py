import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum

bus1 = can.Bus(channel="can0", interface='socketcan')

def main():
    db = cantools.database.load_file("hytech_160.dbc")
    db_torque_input = db.get_message_by_name("DRIVEBRAIN_DESIRED_TORQUE_INPUT") # VCR doesn't have implementation to take this input
    db_speed_input = db.get_message_by_name("DRIVEBRAIN_SPEED_SET_INPUT")
    db_torque_limit = db.get_message_by_name("DRIVEBRAIN_TORQUE_LIM_INPUT")

    torque_zero_msg = db_torque_limit.encode({'drivebrain_torque_rr': 0,
                                       'drivebrain_torque_rl': 0,
                                       'drivebrain_torque_fr': 0,
                                       'drivebrain_torque_fl': 0})

    speed_zero_msg = db_speed_input.encode({'drivebrain_set_rpm_rr': 0,
                                     'drivebrain_set_rpm_rl': 0,
                                     'drivebrain_set_rpm_fr': 0,
                                     'drivebrain_set_rpm_fl': 0})
    
    torque_msg = db_torque_limit.encode({'drivebrain_torque_rr': 1,
                                       'drivebrain_torque_rl': 1,
                                       'drivebrain_torque_fr': 1,
                                       'drivebrain_torque_fl': 1})

    speed_msg = db_speed_input.encode({'drivebrain_set_rpm_rr': 300,
                                'drivebrain_set_rpm_rl': 300,
                                'drivebrain_set_rpm_fr': 300,
                                'drivebrain_set_rpm_fl': 300})

    while(1):
        msg = can.Message(arbitration_id=db_speed_input.frame_id, is_extended_id=False, data = speed_msg)
        bus1.send(msg)
        time.sleep(.004)
        msg = can.Message(arbitration_id=db_torque_limit.frame_id, is_extended_id=False, data = torque_msg)
        bus1.send(msg)
        print("Sent CAN msg")
        time.sleep(.004)

if __name__ == "__main__":
    main()