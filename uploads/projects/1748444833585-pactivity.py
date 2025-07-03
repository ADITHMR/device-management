# ********************AutoGate: Self opening gate**********************
from machine import Pin
import time
from servo import Servo
from drivers.oled import oled_two_data
from custom_neopixel import CustomNeoPixel
from analog_buzzer import AnalogBuzzer
from utils import get_activity_params
from pin_mapping import get_trig_state
import gc




is_led_used=None
is_buzzer_used=None
buzzer_pin=None
total_counts = None
timeout_duration = None
num_pixels=None
led_strip_pin=None
led=[]
buzzer=None
servo_mtr=None
open_angle=None
close_angle=None
led_strip=None


    
def run_activity(activity):    
    oled_two_data(1,2,"Running","AutoGate")
    time.sleep(2)
    
    global led, is_led_used,buzzer_pin,total_counts,buzzer,open_angle,close_angle
    global timeout_duration ,num_pixels,led_strip_pin,servo_mtr,is_buzzer_used,led_strip
    # -----------------------------------
    # User Defined Datas
#     is_led_used=1
# # Initialize IR sensors and servo motor
#     sensor_in_pin=36
#     sensor_out_pin=39
#     servo_mtr_pin=33
#           # Servo motor control
#     buzzer_pin=32
#     timeout_duration = 5 
#     num_pixels=5
#     led_strip_pin=5
    params=get_activity_params(activity)
    print(params)
    is_led_used=params["is_led_used"]
    is_buzzer_used=params["is_buzzer_used"]
    sensor_in_pin=int(params["sensor_in_pin"])
    sensor_out_pin=int(params["sensor_out_pin"])
    servo_mtr_pin=int(params["servo_mtr_pin"])
    buzzer_pin=int(params["buzzer_pin"])
    timeout_duration = int(params["timeout_duration"])
    num_pixels=int(params["num_pixels"])
    led_strip_pin=int(params["led_strip_pin"])
    sensor_out_active_state=get_trig_state(params["sensor_out_active_state"])
    sensor_in_active_state=get_trig_state(params["sensor_in_active_state"])
    open_angle=int(params["open_angle"])
    close_angle=int(params["close_angle"])
    # -----------------------------------
    sensor_in = Pin(sensor_in_pin, Pin.IN)  # IR sensor for entry
    sensor_out = Pin(sensor_out_pin, Pin.IN) # IR sensor for exit
    servo_mtr = Servo(servo_mtr_pin,True)
    buzzer_enabled=False
    led_enabled=False
    if is_led_used=="Enabled":
        led_enabled=True
        led_strip=Pin(led_strip_pin, Pin.IN)
    if  is_buzzer_used=="Enabled":
        buzzer_enabled=True
    else:
        num_pixels=0
    buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=buzzer_enabled)
    buzzer.play_tone(2000, 2)
    
#     if is_led_used=="Enabled":
    temp=CustomNeoPixel(led_strip_pin,100,led_enabled)
    temp.set_color_All(0,0,0)
    del temp
    gc.collect()
    led=CustomNeoPixel(led_strip_pin,num_pixels,led_enabled)
    led.clear()
   
    total_counts = 0
#     red(num_pixels)
    is_entering = 0
    is_exiting = 0
    time.sleep(1)

    gate_close()
    gate_close()
    gate_close()
    # Main loop
    oled_two_data(2,2,"Gate","Closed")
    while True:
        try:
            start_time = time.time()  
            
            if is_exiting == 0 and is_entering == 0:
                if sensor_in.value() == sensor_in_active_state:  
        #             time.sleep(0.1)  
                    print("Student Entering.")
                    oled_two_data(2,2,"Gate","Open")
#                     oled_two_data(2,1,"Entering","-----")
                    gate_open()
                    is_entering = 1 

                elif sensor_out.value() == sensor_out_active_state:  
        #             time.sleep(0.1) 
                    print("Student Exiting.")
                    oled_two_data(2,2,"Gate","Open")
#                     oled_two_data(2,1,"Exiting","-----")
                    gate_open()
                    is_exiting = 1  

            else:
              
                while time.time() - start_time < timeout_duration:
                    if is_exiting == 1:
                        if sensor_in.value() == sensor_in_active_state:
                            while sensor_in.value() == sensor_in_active_state:
                                pass
        #                     time.sleep(0.1)  
                            total_counts -= 1
                            print(f"Total count = {total_counts}")
                            oled_two_data(2,2,"Gate","Closed")
                            gate_close()  
                            is_exiting = 0  
                            
                            
#                             time.sleep(.2)  
                            break  
                    elif is_entering == 1:
                        if sensor_out.value() == sensor_out_active_state:
                            while sensor_out.value() == sensor_out_active_state:
                                pass
        #                     time.sleep(0.1) 
                            total_counts += 1
                            print(f"Total count = {total_counts}")
                            oled_two_data(2,2,"Gate","Closed")
                            gate_close() 
                            is_entering = 0  
                            
                            
#                             time.sleep(.2)  
                            break  
                
              
                if time.time() - start_time >= timeout_duration:
                    print("Timeout! Closing gate.")
                    gate_close()
                    oled_two_data(2,1,"Timeout","Gate Closed")
                    is_entering = 0
                    is_exiting = 0
                    time.sleep(1)  

            
        except Exception as e:
            print(f"Error in Autogate activity(): {e}")
        time.sleep(0.1)

    
def red(num_pixels):
    led.set_color_All(255,0,0)
            
def green(num_pixels):
    led.set_color_All(0,255,0)
            

def gate_open():
    global num_pixels,open_angle
    servo_mtr.move(float(open_angle))
    green(num_pixels)
    buzzer.play_tone(2500, .5)


def gate_close():
    global num_pixels,close_angle
    servo_mtr.move(float(close_angle))
    red(num_pixels)
    buzzer.play_tone(2500, .5)
    time.sleep(.5)

    

