import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum
     
bus1 = can.Bus(channel="can0", interface='socketcan')

def main():
    inverter_on = False
    recv = False

    db = cantools.database.load_file("hytech_159.dbc")
    setpoint = db.get_message_by_name("INV3_STATUS")

    error_reset = False
    initialized = False
    while(1): 
        # if recv:
            # print("Mesg received")  

        if inverter_on:
            print("Inverters are ON")
        else:
            print("Inverters are OFF")

        rcvd_message = bus1.recv(timeout=0.01)
        if(rcvd_message):
            recv = True
            try:
                
                decoded_message = db.decode_message(rcvd_message.arbitration_id, rcvd_message.data)
                msg_info = db.get_message_by_frame_id(rcvd_message.arbitration_id)
                
                # print(f"Decoded Message: {decoded_message}")
                
                if( (msg_info.name.lower() == "inv3_status")):
                    inverter_on = decoded_message["inverter_on"]
                    # inverter_hv_on = decoded_message["quit_dc_on"]

            except KeyError:
                print(f"Message ID {rcvd_message.arbitration_id} not found in the DBC.")
            except Exception as e:
                print(f"Error decoding message: {e}")
            
        time.sleep(0.014)
        

if __name__ == "__main__":
    main()
