import time
import can
import cantools

bus1 = can.Bus(channel="can0", interface="socketcan")


def main():

    db = cantools.database.load_file("hytech_168.dbc")
    config_cmd = db.get_message_by_name("BRAKE_ROTOR_SENSOR_COMMAND")

    # FL = 1220 base, FR = 1225 base
    base_id = 1220
    emissivity = 0.5
    config_cmd_msg = config_cmd.encode(
        {
            "brake_temp_sensor_prog_const": 30000,
            "brake_temp_sensor_base_can_id": base_id,
            "brake_temp_sensor_emissivity": emissivity,
            "brake_temp_sensor_sampling_freq": 7,
            "brake_temp_sensor_ch_setting": 80,
            "brake_temp_sensor_can_bitrate": 1,
        }
    )

    current_frame_id = 1220

    while 1:
        msg = can.Message(
            arbitration_id=current_frame_id, is_extended_id=False, data=config_cmd_msg
        )

        bus1.send(msg)
        time.sleep(0.9)


if __name__ == "__main__":
    main()
