
# ******************SentiLume: Intelligent street illumination************************


from utils import get_activity_params
from analog_buzzer import AnalogBuzzer
from pin_mapping import *
from custom_neopixel import CustomNeoPixel
from drivers.display import *
from drivers.oled import *
import gc




def run_activity(activity):
    params=get_activity_params(activity)
     
    sensor=set_pin_in(params["sensor_pin"])
    sensor_trig=get_trig_state(params["sensor_active_state"])
    
    print("starting 'SentiLume: Intelligent street illumination ' activity")
    
    buzzer_enable=params["buzzer_enable"]
    buzzer_pin=int(params["buzzer_pin"])
    led_strip_Enable= params["led_strip_Enable"]
    if led_strip_Enable == "Enabled":
        led_strip_Enable=True
    else:
        led_strip_Enable=False
    
    led_pin= int(params["led_pin"])
    led_num_pixels =int(params["led_num_pixels"])
    temp = CustomNeoPixel(pin=led_pin, num_pixels=100, enabled=led_strip_Enable)
    temp.set_color_All(0,0,0)
    del temp
    gc.collect()
    Led_strip = CustomNeoPixel(pin=led_pin, num_pixels=led_num_pixels, enabled=led_strip_Enable)

    
    if buzzer_enable=="Enabled":
        buzzer_enable=True
    else:
        buzzer_enable=False
    buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=buzzer_enable)
    buzzer.play_tone(2000, 1)
    last=0
    if sensor.value() ==sensor_trig:
        oled_three_data(2,2,2,"Street","Light","ON")
        Led_strip.set_color_All(255,255,255)
    else:
        oled_three_data(2,2,2,"Street","Light","OFF")
        Led_strip.set_color_All(0,0,0)
        
    while True: 
        if sensor.value() ==sensor_trig:
            if last==0:
                Led_strip.set_color_All(255,255,255)
                disp_seq_str(["MOON"],0)
#                 oled_log("Street Light ON")
                oled_three_data(2,2,2,"Street","Light","ON")
                last=1
                buzzer.play_tone(2000, .2)
        else:
            if last==1:
                Led_strip.set_color_All(0,0,0)
                disp_seq_str(["SUN"],0)
#                 oled_log("Street Light OFF")
                oled_three_data(2,2,2,"Street","Light","OFF")
                last=0
                buzzer.play_tone(2000, .2)
        time.sleep(.1)
     


