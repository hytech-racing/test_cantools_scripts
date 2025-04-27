import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum

bus1 = can.Bus(channel="can0", interface='socketcan')

def main():
    db = cantools.database.load_file("hytech_159.dbc")
    pedals_system = db.get_message_by_name("PEDALS_SYSTEM_DATA")
    dash_input = db.get_message_by_name("DASH_INPUT")

    pedals_brake_msg = pedals_system.encode({'brake_pedal': 0,
                                     'accel_pedal': 0.01,
                                     'implaus_exceeded_max_duration': False,
                                     'brake_accel_implausibility': False,
                                     'mechanical_brake_active': False,
                                     'accel_pedal_active': False,
                                     'brake_pedal_active': True,
                                     'brake_implausible': False,
                                     'accel_implausible': False})
    
    pedals_accel_msg = pedals_system.encode({'brake_pedal': 0,
                                     'accel_pedal': 0.01,
                                     'implaus_exceeded_max_duration': False,
                                     'brake_accel_implausibility': False,
                                     'mechanical_brake_active': False,
                                     'accel_pedal_active': False,
                                     'brake_pedal_active': True,
                                     'brake_implausible': False,
                                     'accel_implausible': False})
 
    dash_msg = dash_input.encode({'dash_dial_mode' : 0,
                                'right_shifter_button' : False,
                                'left_shifter_button' : False,
                                'data_button_is_pressed' : False,
                                'start_button' : True,
                                'mode_button' : False,
                                'motor_controller_cycle_button' : False,
                                'preset_button' : False,
                                'led_dimmer_button' : False})

    inverter_on = False
    recv = False
    while(1):
        msg=  can.Message(arbitration_id=pedals_system.frame_id, is_extended_id=False, data = pedals_brake_msg)
        bus1.send(msg)

        msg = can.Message(arbitration_id=dash_input.frame_id, is_extended_id=False, data = dash_msg)
        bus1.send(msg)

        if not recv:
            print("No messages received")
        elif inverter_on:
            print("Inverters are ON")
            time.sleep(1.0)
            break
        else:
            print("Inverters are OFF")
        
        rcvd_message = bus1.recv(timeout=0.01)
        if(rcvd_message):
            recv = False
            try:
                decoded_message = db.decode_message(rcvd_message.arbitration_id, rcvd_message.data)
                msg_info = db.get_message_by_frame_id(rcvd_message.arbitration_id)

                if( (msg_info.name.lower() == "inv3_status")):
                    inverter_on = decoded_message["inverter_on"]
            except KeyError:
                print(f"Message ID {rcvd_message.arbitration_id} not found in the DBC.")
            except Exception as e:
                print(f"Error decoding message: {e}")

        time.sleep(.005)

    while(1):
        msg = can.Message(arbitration_id=pedals_system.frame_id, is_extended_id=False, data = pedals_accel_msg)
        bus1.send(msg)

        msg = can.Message(arbitration_id=dash_input.frame_id, is_extended_id=False, data = dash_msg)
        bus1.send(msg)

        time.sleep(.005)

if __name__ == "__main__":
    main()