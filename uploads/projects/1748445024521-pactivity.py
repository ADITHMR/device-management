# ***********************FireGuard: Intelligent Fire Detection************************

from analog_buzzer import AnalogBuzzer
from custom_neopixel import CustomNeoPixel
from utils import get_activity_params
from machine import  Pin
from pin_mapping import *
from drivers.oled import *
from drivers.display import  *
import gc




def run_activity(activity):
    
    params=get_activity_params(activity) 
    fire_sensor=set_pin_in(params["sensor_pin"])
    fire_sensor_trig=get_trig_state(params["sensor_active_state"])
    buzzer_Enable = params["buzzer_Enable"]
    if buzzer_Enable == "Enabled":
        buzzer_Enable=True
    else:
        buzzer_Enable=False
    buzzer_pin =int(params["buzzer_pin"])
    
    led_strip_Enable= params["led_strip_Enable"]
    if led_strip_Enable == "Enabled":
        led_strip_Enable=True
    else:
        led_strip_Enable=False
    
    led_pin= int(params["led_pin"])
    led_num_pixels =int(params["led_num_pixels"])
    
    buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=buzzer_Enable)
    temp = CustomNeoPixel(pin=led_pin, num_pixels=100, enabled=led_strip_Enable)
    temp.set_color_All(0,0,0)
    del temp
    gc.collect()
    Led_strip = CustomNeoPixel(pin=led_pin, num_pixels=led_num_pixels, enabled=led_strip_Enable)
    buzzer.play_tone(2000, 0.3)
    print("Started 'FireGuard: Intelligent Fire Detection' activity")
    while True:
        while(fire_sensor.value()==fire_sensor_trig):
            oled_three_data(2,2,2,"ALERT","Fire","Detected")
            disp_seq_str(["FIRE"],0)
            #buzzer_on()
            Led_strip.set_color_All(255,0,0)
            #set_color_for(3,255, 0, 0)
            buzzer.play_tone(1500, 0.1)
            buzzer.play_tone(2000, 0.2)
            
            oled_three_data(2,2,2,"ALERT","  ","  ")
            #buzzer_off()
            Led_strip.set_color_All(0,0,0)
            time.sleep(.1)
        
        Led_strip.set_color_All(0,255,0)
        oled_two_data(1,3,"No Fire","SAFE")
        disp_seq_str(["SAFE"],0)
        

    
    
