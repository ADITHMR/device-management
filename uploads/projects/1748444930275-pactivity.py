# ********************CountMaster: Student headcount Tracker**********************
from machine import Pin
import time
from drivers.oled import oled_two_data
from analog_buzzer import AnalogBuzzer
from utils import get_activity_params
from pin_mapping import get_trig_state


is_buzzer_used=None
buzzer_pin=None
timeout_duration = None
buzzer=None

   
def run_activity(activity):
    oled_two_data(1,1,"Starting","CountMaster")
    time.sleep(2)
    
    global buzzer_pin,buzzer,timeout_duration,is_buzzer_used
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
    is_buzzer_used=params["is_buzzer_used"]
    sensor_in_pin=int(params["sensor_in_pin"])
    sensor_out_pin=int(params["sensor_out_pin"])
    buzzer_pin=int(params["buzzer_pin"])
    timeout_duration = int(params["timeout_duration"])
    sensor_out_active_state=get_trig_state(params["sensor_out_active_state"])
    sensor_in_active_state=get_trig_state(params["sensor_in_active_state"])

    # -----------------------------------
    sensor_in = Pin(sensor_in_pin, Pin.IN)  # IR sensor for entry
    sensor_out = Pin(sensor_out_pin, Pin.IN) # IR sensor for exit

    buzzer_enabled=False
    
    if is_buzzer_used=="Enabled":
        buzzer_enabled=True
    buzzer = AnalogBuzzer(pin_number=buzzer_pin,enOrDi=buzzer_enabled)
    buzzer.play_tone(2000, 2)

    total_counts = 0
    is_entering = 0
    is_exiting = 0
    oled_two_data(2,3,"COUNT",str(total_counts))

    # Main loop
    while True:
        try:
            start_time = time.time()  

            if is_exiting == 0 and is_entering == 0:
                if sensor_in.value() == sensor_in_active_state:  
        #             time.sleep(0.1)  
                    print("Student Entering.")
                    is_entering = 1 

                elif sensor_out.value() == sensor_out_active_state:  
        #             time.sleep(0.1) 
                    print("Student Exiting.")
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
                            oled_two_data(2,3,"Count",str(total_counts))
                            is_exiting = 0  
                            buzzer.play_tone(2500, .5)                            
#                             time.sleep(.2)  
                            break  
                    elif is_entering == 1:
                        if sensor_out.value() == sensor_out_active_state:
                            while sensor_out.value() == sensor_out_active_state:
                                pass
        #                     time.sleep(0.1) 
                            total_counts += 1
                            print(f"Total count = {total_counts}")
                            oled_two_data(2,3,"COUNT",str(total_counts))
                            is_entering = 0  
                            buzzer.play_tone(2500, .5)                            
#                             time.sleep(.2)  
                            break  
                
              
                if time.time() - start_time >= timeout_duration:
                    print("Timeout!")
                    oled_two_data(2,1,"Timeout","Detected")
                    is_entering = 0
                    is_exiting = 0
                    time.sleep(1)  

            time.sleep(0.1)
        except Exception as e:
            print(f"Error in CountMaster activity(): {e}")


