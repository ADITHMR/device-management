import machine
import time

from machine import Pin,I2C



def set_pin_out(pin):
    pin=int(pin)
    print(pin)
    result=Pin(pin, Pin.OUT)
    return result

def set_pin_in(pin):
    pin=int(pin)
    return Pin(pin, Pin.IN)
def get_trig_state(state):
 
    if state=="Active Low":
        return 0
    elif state=="Active High":
        return 1
    else:
        return 0
    
