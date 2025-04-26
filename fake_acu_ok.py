import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum

bus1 = can.Bus(channel="can0", interface='socketcan')

def main():
    db = cantools.database.load_file("hytech_156.dbc")
    acu_ok = db.get_message_by_name("ACU_OK")

    bms_msg_00 = acu_ok.encode({'bms_ok': 0, 'imd_ok': 0})
    bms_msg_01 = acu_ok.encode({'bms_ok': 0, 'imd_ok': 1})
    bms_msg_10 = acu_ok.encode({'bms_ok': 1, 'imd_ok': 0})
    bms_msg_11 = acu_ok.encode({'bms_ok': 1, 'imd_ok': 1})

    while(1):
        msg = can.Message(arbitration_id=acu_ok.frame_id, is_extended_id=False, data = bms_msg_00)
        bus1.send(msg)
        
        time.sleep(1.0)

        msg = can.Message(arbitration_id=acu_ok.frame_id, is_extended_id=False, data = bms_msg_01)
        bus1.send(msg)
        
        time.sleep(1.0)

        msg = can.Message(arbitration_id=acu_ok.frame_id, is_extended_id=False, data = bms_msg_10)
        bus1.send(msg)
        
        time.sleep(1.0)

        msg = can.Message(arbitration_id=acu_ok.frame_id, is_extended_id=False, data = bms_msg_11)
        bus1.send(msg)
        
        time.sleep(1.0)

if __name__ == "__main__":
    main()