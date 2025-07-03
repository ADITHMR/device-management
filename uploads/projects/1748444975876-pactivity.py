import machine
import time
from drivers.oled import oled_three_data
from utils import get_activity_params


# Function to measure distance
def measure_distance(trigger_pin,echo_pin):
    # Send a 10us pulse to the Trigger pin to start the measurement
    trigger_pin.on()
    time.sleep_us(10)  # Delay for 10 microseconds
    trigger_pin.off()
    pulse_end=0
    pulse_start=0
    # Wait for the Echo pin to go high (start of the pulse)
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    
    # Wait for the Echo pin to go low (end of the pulse)
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()

    # Calculate the pulse duration in microseconds
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    
    # Speed of sound is approximately 34300 cm per second at 20°C
    # The time it takes for the sound to travel to the object and back is divided by 2
    distance = (pulse_duration * 0.0343) / 2  # Distance in cm
    return distance

# Main loop
def run_activity(activity):
    params = get_activity_params(activity)
    trigger_pin_no = int(params["trig_pin"])
    echo_pin_no= int(params["echo_pin"])
# Pin configuration
    trigger_pin = machine.Pin(trigger_pin_no, machine.Pin.OUT)  # Trigger pin (GPIO13)
    echo_pin = machine.Pin(echo_pin_no, machine.Pin.IN)     # Echo pin (GPIO12)
    oled_three_data(2,2,2,"Distance","0.00","cm")
    while True:
        dist = int(measure_distance(trigger_pin,echo_pin))  # Measure the distance
        if dist>100:
            print(f"Distance: {dist} cm")  # Print the distance in cm
            oled_three_data(2,2,2,"Distance",">100","cm")
        else:
            print(f"Distance: {dist} cm")  # Print the distance in cm
            oled_three_data(2,2,2,"Distance",str(dist),"cm")

#         time.sleep(.5)  # Delay between measurements

# Run the main loop


