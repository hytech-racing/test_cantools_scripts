import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum

bus1 = can.Bus(channel="can0", interface='socketcan', )

def main():
    db = cantools.database.load_file("hytech_159.dbc")
    pedals_system = db.get_message_by_name("PEDALS_SYSTEM_DATA")
    dash_input = db.get_message_by_name("DASH_INPUT")

    pedals_msg = pedals_system.encode({'brake_pedal': 0.3,
                                     'accel_pedal': 0,
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

    while(1):
        msg = can.Message(arbitration_id=pedals_system.frame_id, is_extended_id=False, data = pedals_msg)
        bus1.send(msg)

        msg = can.Message(arbitration_id=dash_input.frame_id, is_extended_id=False, data = dash_msg)
        bus1.send(msg)
        
        time.sleep(.005)

if __name__ == "__main__":
    main()