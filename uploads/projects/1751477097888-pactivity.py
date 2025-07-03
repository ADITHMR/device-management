# ********************TouchFlow: Intelligent Fan Control**********************
import machine 
import time
from drivers.oled import oled_two_data
from utils import get_activity_params
from pin_mapping import get_trig_state
import gc
from MX1508Motor import MX1508Motor
from analog_buzzer import AnalogBuzzer

from button import Button

speed_index=0
speed_list=[]
motor = MX1508Motor(in1_pin=12, in2_pin=13)
buzzer=0

def on_switch_up(event):
    global speed_index, speed_list
    if event == 'press':
        buzzer.play_tone(2000, .2)
        speed_index+=1;
        if speed_index>5:
            speed_index=5
        motor.set_speed(speed_list[speed_index])
        oled_two_data(2,2,"Speed",f"{speed_list[speed_index]}%")
        print(f"UP Speed={speed_list[speed_index]}")
def on_switch_down(event):
    global speed_index,speed_list
    
    if event == 'press':
        buzzer.play_tone(2000, .2)
        speed_index-=1;
        if speed_index<0:
            speed_index=0
        motor.set_speed(speed_list[speed_index])
        oled_two_data(2,2,"Speed",f"{speed_list[speed_index]}%")
        print(f"down Speed={speed_list[speed_index]}")
    
def run_activity(activity):    
    oled_two_data(1,1,"Starting","TouchFlow")
    time.sleep(2)
    
  
    global speed_list, buzzer
    speed_list=[0]
    
    params=get_activity_params(activity)
    print(params)
   
    speed_list.append(int(params["speed1"]))
    speed_list.append(int(params["speed2"]))
    speed_list.append(int(params["speed3"]))
    speed_list.append(int(params["speed4"]))
    speed_list.append(int(params["speed5"]))
    speed_list.append(int(params["speed6"]))
    print(speed_list)
    up_pin=int(params["up_pin"])
    up_pin_state=get_trig_state(params["up_pin_state"])
    
    down_pin=int(params["down_pin"])
    down_pin_state=get_trig_state(params["down_pin_state"])
    
    is_buzzer= "buzzer_enabled" in params
    is_ir_remote= "is_ir_remote" in params
    
    buzzer_pin=int(params["buzzer_pin"])
    
    
    
    
    pull='up' if up_pin_state==0 else "down"
    up_switch=Button(pin_num=up_pin, callback=on_switch_up,pull=pull, long_press_time=5000,enOrDi=True)
    
    pull='up' if down_pin_state==0 else "down"
    up_switch=Button(pin_num=down_pin, callback=on_switch_down,pull=pull, long_press_time=5000,enOrDi=True)
    
   
    mtr_pin1=int(params["fan_pin1"])
    mtr_pin2=int(params["fan_pin2"])
    motor = MX1508Motor(in1_pin=mtr_pin1, in2_pin=mtr_pin2)
    
    buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=is_buzzer)
    buzzer.play_tone(2000, 1)
    
    oled_two_data(2,2,"Speed",f"{speed_list[speed_index]}%")
    while True:
        pass
          
    
        time.sleep(.1)
# run_activity("activity1")    
    
# 
#     # -----------------------------------
#     sensor_in = Pin(sensor_in_pin, Pin.IN)  # IR sensor for entry
#     sensor_out = Pin(sensor_out_pin, Pin.IN) # IR sensor for exit
#     servo_mtr = Servo(servo_mtr_pin,True)
#     buzzer_enabled=False
#     led_enabled=False
#     lid="close"
#     if is_led_used=="Enabled":
#         led_enabled=True
#         led_strip=Pin(led_strip_pin, Pin.IN)
#     if  is_buzzer_used=="Enabled":
#         buzzer_enabled=True
#     else:
#         num_pixels=0
#     buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=buzzer_enabled)
#     buzzer.play_tone(2000, 2)
#     
# #     if is_led_used=="Enabled":
#     temp=CustomNeoPixel(led_strip_pin,100,led_enabled)
#     temp.set_color_All(0,0,0)
#     del temp
#     gc.collect()
#     led=CustomNeoPixel(led_strip_pin,num_pixels,led_enabled)
#     led.clear()
#    
#     total_counts = 0
# #     red(num_pixels)
#     is_entering = 0
#     is_exiting = 0
#     time.sleep(1)
# 
#     lid_close()
#     # Main loop
#     oled_two_data(2,2,"Bin","Closed")
#     while True:
#         try:
#             if sensor_in.value() == sensor_in_active_state:
#                 print("TouchFree Bin lid opening")
#                 buzzer.play_tone(2500, .2)
#                 time.sleep(.2)
#                 lid_open()
#                 oled_two_data(2,2,"Bin","Open")
#                 while sensor_in.value() == sensor_in_active_state:
#