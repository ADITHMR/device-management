from process.file_mgr import  *
from drivers.oled import *


IR_DATA=0
# User callback for IR receiver
def get_IR_data():
    global IR_DATA
    return int(IR_DATA)
def set_IR_data(data):
    global IR_DATA
    if data>-1 and data<15:
        IR_DATA=data
    
def callback(data, addr, ctrl):

    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        
        ir_data=decodeKeyValue(data)
        if ir_data>-1 and ir_data<19:
            global IR_DATA
            IR_DATA=ir_data
            print(f"mode={get_IR_data()}")
            
            oled_log(f"IR-> {decodeKeyValue(data)}")
            print(decodeKeyValue(data))
        
            
           

# Decode the received data and return the corresponding key name
def decodeKeyValue(data):
    if data == 0x16:
        return 0
    if data == 0x0C:
        return 1
    if data == 0x18:
        return 2
    if data == 0x5E:
        return 3
    if data == 0x08:
        return 4
    if data == 0x1C:
        return 5
    if data == 0x5A:
        return 6
    if data == 0x42:
        return 7
    if data == 0x52:
        return 8
    if data == 0x4A:
        return 9
    if data == 0x09:
        return 18#"EQ"
    if data == 0x15:
        return 16#"+"
    if data == 0x7:
        return 17#"+"
    if data == 0x0D:
        return "U/SD"
    if data == 0x19:
        return "CYCLE"
    if data == 0x44:
        return 13#"BACKWARD"
    if data == 0x43:
        return 15#"PLAY/PAUSE"
    if data == 0x40:
        return 14#"FORWARD"
    if data == 0x45:
        return 10#"CH-"
    if data == 0x47:
        return 12#"CH+"
    if data == 0x46:
        return 11#"CH"
    return "ERROR"

