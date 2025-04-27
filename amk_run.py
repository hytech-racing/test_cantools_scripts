import socket
import time
import can
import cantools
from pprint import pprint
import os

from enum import Enum
     
bus1 = can.Bus(channel="can0", interface='socketcan')

def main():
    inverter_ready = False
    inverter_hv_on = False # quit dc on
    inverter_enabled = False # quit inverter on

    db = cantools.database.load_file("hytech_dbc.dbc")
    setpoint = db.get_message_by_name("MC1_SETPOINTS_COMMAND")

    empty_msg = setpoint.encode({'negative_torque_limit': 0, 'positive_torque_limit': 0, 'speed_setpoint_rpm': 0, 'remove_error': 1, 'driver_enable': 0, 'hv_enable': 0, 'inverter_enable': 0})
    reset_error_msg = setpoint.encode({'negative_torque_limit': 0, 'positive_torque_limit': 0, 'speed_setpoint_rpm': 0, 'remove_error': 1, 'driver_enable': 0, 'hv_enable': 0, 'inverter_enable': 0})
    hv_on_msg = setpoint.encode({'negative_torque_limit': 0, 'positive_torque_limit': 0, 'speed_setpoint_rpm': 0, 'remove_error': 0, 'driver_enable': 0, 'hv_enable': 1, 'inverter_enable': 0})
    
    inverter_on_msg = setpoint.encode({'negative_torque_limit': 0, 'positive_torque_limit': 0, 'speed_setpoint_rpm': 0, 'remove_error': 0, 'driver_enable': 1, 'hv_enable': 1, 'inverter_enable': 1})

    rpm_msg = setpoint.encode({'negative_torque_limit': -5, 'positive_torque_limit': 5, 'speed_setpoint_rpm': 2000, 'remove_error': 0, 'driver_enable': 1, 'hv_enable': 1, 'inverter_enable': 1})
    current_rpm = 0
    # torq_msg = setpoint.encode({'negative_torque_limit': -2, 'positive_torque_limit': 2, 'speed_setpoint_rpm': 100, 'remove_error': 0, 'driver_enable': 1, 'hv_enable': 1, 'inverter_enable': 1})

    error_reset = False
    initialized = False
    while(1):
        
        if(not error_reset):
            try: 
                msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data = reset_error_msg)
                bus1.send(msg)
            except can.CanError:
                print("Message NOT sent!  Please verify can0 is working first")
            error_reset = True

        if(inverter_ready and inverter_hv_on and inverter_enabled):
            print("inverter enabled yippee, attempting cmd")
            try:
                if(current_rpm < 2000):
                    msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data=rpm_msg)
                else:
                    msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data=empty_msg)
                bus1.send(msg)
            except can.CanError:
                print("Message NOT sent!  Please verify can0 is working first")
        elif((not inverter_hv_on) and (inverter_ready) and (not inverter_enabled) and (not initialized)):
            print(inverter_hv_on)
            print(inverter_ready)
            print(inverter_enabled)
            print("inverter not ready, attempting hv init")
            try:
                msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data=hv_on_msg)
                bus1.send(msg)
            except can.CanError:
                print("Message NOT sent!  Please verify can0 is working first")
        elif(inverter_hv_on and inverter_ready and (not inverter_enabled) and (not initialized)):
            print("inverter ready and hv on but inverter not enabled")
            try:
                
                msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data=inverter_on_msg)
                bus1.send(msg)
            except can.CanError:
                print("Message NOT sent!  Please verify can0 is working first")
        elif((not inverter_hv_on) and (not inverter_ready) and (not inverter_enabled) and (not initialized)):
            print("first msg")
            try:
                
                msg = can.Message(arbitration_id=setpoint.frame_id, is_extended_id=False, data=empty_msg)
                bus1.send(msg)
            except can.CanError:
                print("Message NOT sent!  Please verify can0 is working first")

        
        rcvd_message = bus1.recv(timeout=0.01)
        if(rcvd_message):
            try:
                
                decoded_message = db.decode_message(rcvd_message.arbitration_id, rcvd_message.data)
                msg_info = db.get_message_by_frame_id(rcvd_message.arbitration_id)
                
                # print(f"Decoded Message: {decoded_message}")
                
                if( (msg_info.name.lower() == "mc1_status")):
                    inverter_ready = decoded_message["system_ready"]
                    inverter_hv_on = decoded_message["quit_dc_on"]
                    inverter_enabled = decoded_message["quit_inverter_on"]
                    current_rpm = abs(decoded_message["speed_rpm"])

            except KeyError:
                print(f"Message ID {rcvd_message.arbitration_id} not found in the DBC.")
            except Exception as e:
                print(f"Error decoding message: {e}")
            
        time.sleep(0.014)
        

if __name__ == "__main__":
    main()
