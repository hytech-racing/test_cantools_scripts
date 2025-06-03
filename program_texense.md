import can

- cansend can0 7F1#101F000000000000

(get reply here for the device key in byte 6):
    - `can0  7F3   [8]  10 xx xx xx xx xx xx 05`
    
    10 [00 F5 AC E9] 1F [AD] 05
    
    - id: 01047917
    - tool key: 1F
    - device key: xx

- cansend can0 7F1#2000F5369E005E00 (enter setup)


write parameter (00) to be 10 for switching to CAN 2.0A
- cansend can0 7F1#40xxxxxxxx001000

- write parameter (05) LSB of tx1 frame id to be <0610, 0620, 0630, 0640>
- cansend can0 7F1#4001047917051000 <0610, tx2 id: 0310>
- cansend can0 7F1#4001047917052000 <0620, tx2 id: 0320>
- cansend can0 7F1#4001047917053000 <0630, tx2 id: 0330>
- cansend can0 7F1#4001047917054000 <0640, tx2 id: 0340>

- write parameter (04) MSB of tx1 frame id to be <0610, 0620, 0630, 0640>
- cansend can0 7F1#4001047917040600 <0610, 0620, 0630, 0640>

- write parameter (01) to be standard can and 100hz freq (05):

cansend can0 7F1#4001047917010500


- save params and reboot:
    - cansend can0 7F1#5001047917000000