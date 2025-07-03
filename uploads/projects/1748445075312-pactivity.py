import time
import random
import neopixel
from machine import Pin
from pin_mapping import *
from drivers.ir_decode import get_IR_data, callback,set_IR_data
from ir_rx.nec import NEC_8
from utils import get_activity_params
from drivers.oled import oled_two_data
ir_receiver_enabled=None
import gc

class NeoPixelEffects:
    def __init__(self, pin, num_pixels, increment_pin, decrement_pin):
        # Initialize NeoPixel setup
        self.pin = Pin(pin, Pin.OUT)
        self.num_pixels = num_pixels
        self.np = neopixel.NeoPixel(self.pin, self.num_pixels)
        self.old_ir_code = -1
        self.ir_code = 0
        self.loopExit = False
        
        temp=neopixel.NeoPixel(self.pin, 100)
        temp.fill((0, 0, 0))  # More efficient to fill all pixels at once
        temp.write()
        
        del temp
        gc.collect()

        # Colors for rainbow effect
        self.rainbow_colors = [
    (255, 0, 0),      # Red
    (0, 255, 255),    # Cyan
    (255, 127, 0),    # Orange
    (75, 0, 130),     # Indigo
    (255, 255, 0),    # Yellow
    (173, 0, 255),    # Electric Violet
    (0, 255, 0),      # Green
    (255, 0, 127),    # Hot Pink
    (0, 0, 255),      # Blue
    (255, 191, 0),    # Yellow-Orange
    (191, 0, 255),    # Purple-Magenta
    (0, 255, 127),    # Aqua Green
    (148, 0, 211),    # Violet
    (255, 64, 0),     # Reddish-Orange
    (0, 64, 255),     # Electric Blue
    (127, 255, 0),    # Light Green
    (255, 0, 255),    # Magenta
    (0, 127, 255),    # Deep Sky Blue
    (255, 64, 127),   # Deep Pink
    (191, 255, 0),    # Yellow-Green
    (37, 0, 224),     # Royal Blue
    (255, 191, 224),  # Pinkish Lavender
    (0, 255, 191),    # Turquoise
    (208, 127, 255),  # Lavender
    (0, 191, 255),    # Sky Blue
    (255, 127, 191),  # Light Pink
    (111, 0, 148),    # Dark Purple
    (224, 191, 255),  # Light Lavender
    (255, 0, 191),    # Neon Pink
    (255, 191, 255)   # Soft Pink
]

        # Setup the IR receiver
        

        # Pins for increment and decrement switches
        self.increment_pin = Pin(increment_pin, Pin.IN, Pin.PULL_UP)
        self.decrement_pin = Pin(decrement_pin, Pin.IN, Pin.PULL_UP)

        # Attach interrupts to handle switch presses
        self.increment_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.increment_ir_code)
        self.decrement_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.decrement_ir_code)
        
    def increment_ir_code(self, pin):
        """Increment the IR code when the increment button is pressed."""
       
        set_IR_data(self.ir_code+1)
        print(f"Incremented IR Code: {self.ir_code+1}")

    def decrement_ir_code(self, pin):
        """Decrement the IR code when the decrement button is pressed."""
        set_IR_data(self.ir_code-1)
        print(f"Decremented IR Code: {self.ir_code-1}")

    def get_random_color(self):
        """Generates a random color with RGB values."""
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    def led_write(self):
        try:
            time.sleep(0.1) 
            self.np.write()
        except Exception as e:
            print(f"Error in RGB led_write(): {e}")
        
    def circular_chase(self,speed=0.1):
        """Creates a circular chase effect with random colors."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                for i in range(self.num_pixels):
                    for j in range(self.num_pixels):
                        self.np[j] = color if j == i else (0, 0, 0)  # Light up one pixel at a time
                    self.led_write()
                    time.sleep(speed)
                    if self.check_for_exit():
                        return

    def rainbow_effect(self):
        """Displays a rainbow effect cycling through the colors."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                for i in range(self.num_pixels):
                    self.np[i] = color
                self.led_write()
                time.sleep(0.5)

                if self.check_for_exit():
                    return

    def filling_effect(self):
        """Creates a filling effect where colors fill in both directions."""
        while not self.loopExit:
            for i in range(len(self.rainbow_colors)):
                color = self.rainbow_colors[(i - 1) % len(self.rainbow_colors)]
                next_color = self.rainbow_colors[(i + 1) % len(self.rainbow_colors)]

                for j in range(self.num_pixels):
                    self.np[j] = color
                    self.led_write()
                    time.sleep(0.1)

                    if self.check_for_exit():
                        return

                color = next_color

                for j in range(self.num_pixels - 1, -1, -1):
                    self.np[j] = color
                    self.led_write()
                    time.sleep(0.1)

                    if self.check_for_exit():
                        return
    def pulse_effect(self, speed=0.01, max_brightness=255):
        """Makes the LEDs pulse in and out with a smooth brightness transition."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                for brightness in range(0, max_brightness + 1, 30):  # Increase brightness
                    for i in range(self.num_pixels):
                        self.np[i] = (int(color[0] * brightness / max_brightness), 
                                      int(color[1] * brightness / max_brightness), 
                                      int(color[2] * brightness / max_brightness))
                    self.led_write()
                    time.sleep(speed)
                    if self.check_for_exit():  # Check if IR code was received
                        return  # Exit the effect immediately when check_for_exit returns True
                for brightness in range(max_brightness, -1, -30):  # Decrease brightness
                    for i in range(self.num_pixels):
                        self.np[i] = (int(color[0] * brightness / max_brightness), 
                                      int(color[1] * brightness / max_brightness), 
                                      int(color[2] * brightness / max_brightness))
                    self.led_write()
                    time.sleep(speed)
                    if self.check_for_exit():  # Exit if IR signal detected
                        return
#     def color_wave_effect(self):
#         """Creates a color wave effect moving along the LED strip."""
#         while not self.loopExit:
#             for i in range(self.num_pixels):
#                 # Determine which color to use at the given position
#                 color_index = (i + int(time.time() * 10)) % len(self.rainbow_colors)
#                 color = self.rainbow_colors[color_index]
#                 self.np[i] = color
#             self.led_write()
#             time.sleep(0.1)
    def sparkle_effect(self,  spark_chance=0.1, speed=0.05):
        """Creates a sparkling effect with random pixels lighting up in the given color."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                for i in range(self.num_pixels):
                    if random.random() < spark_chance:
                        self.np[i] = color
                    else:
                        self.np[i] = (0, 0, 0)  # Turn off other pixels
                    if self.check_for_exit():
                        return
                self.led_write()
                time.sleep(speed)
    def colorful_fade_effect(self, fade_time=1):
        """Smoothly fades through a set of rainbow colors."""
        while not self.loopExit:
            for i in range(len(self.rainbow_colors)):
                color_start = self.rainbow_colors[i]
                color_end = self.rainbow_colors[(i + 1) % len(self.rainbow_colors)]
                
                # Fade from color_start to color_end
                for t in range(101):
                    r = int(color_start[0] * (1 - t / 100) + color_end[0] * (t / 100))
                    g = int(color_start[1] * (1 - t / 100) + color_end[1] * (t / 100))
                    b = int(color_start[2] * (1 - t / 100) + color_end[2] * (t / 100))
                    if self.check_for_exit():
                        return
                    for j in range(self.num_pixels):
                        self.np[j] = (r, g, b)
                        if self.check_for_exit():
                            return
                    self.led_write()
                    time.sleep(fade_time / 100)
   
    def alternating_stripes_effect(self,  stripe_size=1, speed=0.1):
        """Alternates blocks of colors across the LED strip."""
        while not self.loopExit:
            for i in range(len(self.rainbow_colors)):
                color1=self.rainbow_colors[i]
                color2=self.rainbow_colors[i-1]
                for i in range(0, self.num_pixels, stripe_size * 2):
                    # Set color for the first stripe
                    for j in range(i, min(i + stripe_size, self.num_pixels)):
                        self.np[j] = color1
                     
                    # Set color for the second stripe
                    for j in range(i + stripe_size, min(i + 2 * stripe_size, self.num_pixels)):
                        self.np[j] = color2
                        
                self.led_write()
                if self.check_for_exit():
                    return
                time.sleep(speed)
                for i in range(0, self.num_pixels, stripe_size * 2):
                    # Set color for the first stripe
                    for j in range(i, min(i + stripe_size, self.num_pixels)):
                        self.np[j] = color2
                    # Set color for the second stripe
                    for j in range(i + stripe_size, min(i + 2 * stripe_size, self.num_pixels)):
                        self.np[j] = color1
                self.led_write()
                if self.check_for_exit():
                    return
                time.sleep(speed)
    def ripple_effect(self, speed=0.01, ripple_size=1):
        """Creates a ripple effect moving across the LED strip."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                for ripple_start in range(self.num_pixels):
                    # Create a ripple at the starting position
                    for i in range(ripple_size):
                        if ripple_start + i < self.num_pixels:
                            self.np[ripple_start + i] = color
                            
                    self.led_write()
                    if self.check_for_exit():
                        return
                    time.sleep(speed)
                    
                    # Clear the ripple after it moves
                    for i in range(self.num_pixels):
                        self.np[i] = (0, 0, 0)

    def zigzag_effect(self,  speed=0.1):
        """Creates a zigzag motion across the LED strip."""
        while not self.loopExit:
            for color in self.rainbow_colors:
                # Zigzag motion
                for i in range(self.num_pixels):
                    # Set the color for one side and reverse it on the other
                    if i % 2 == 0:
                        self.np[i] = color
                    else:
                        self.np[i] = (0, 0, 0)
                self.led_write()
                if self.check_for_exit():
                    return
                time.sleep(speed)
                
                # Reverse the effect
                for i in range(self.num_pixels):
                    if i % 2 == 0:
                        self.np[i] = (0, 0, 0)
                    else:
                        self.np[i] = color
                self.led_write()
                if self.check_for_exit():
                    return
                time.sleep(speed)
    def candlelight_flicker(self, speed=0.1, max_brightness=200):
        """Simulates candlelight by flickering the light randomly."""
        while not self.loopExit:
            for i in range(self.num_pixels):
                flicker_brightness = random.randint(0, max_brightness)
                self.np[i] = (flicker_brightness, flicker_brightness // 2, 0)  # Yellowish flicker
            self.led_write()
            if self.check_for_exit():
                return
            time.sleep(speed)
    
    def check_for_exit(self):
        """Checks if IR signal is received and exits the effect."""
        self.ir_code = get_IR_data()
        if self.ir_code > 9:
            self.ir_code=9
            set_IR_data(9)
        
        if self.ir_code != self.old_ir_code:
            self.old_ir_code = self.ir_code
            self.loopExit = True  # Exit the current effect
            
            print(f"IR Code: {self.ir_code}")

            return True
        
        return False
    

    def run(self,num_pixels):
        """Main loop to control the effect switching based on IR input."""
        while True:
            # Check for specific IR codes and switch effects
            if self.ir_code == 0:  # IR code for Circular Chase
                print("Switching to Circular Chase")
                self.loopExit = False
                oled_two_data(2,2,"Circular","Chase")
                self.circular_chase()
                

            elif self.ir_code == 1:  # IR code for Rainbow Effect
                print("Switching to Rainbow Effect")
                self.loopExit = False
                oled_two_data(2,2,"Rainbow","Effect")
                self.rainbow_effect()

            elif self.ir_code == 2:  # IR code for Filling Effect
                print("Switching to Filling Effect")
                self.loopExit = False
                oled_two_data(2,2,"Filling","Effect")
                self.filling_effect()
            elif self.ir_code == 3:  # IR code for Circular Chase
                print("Switching to Pulse Effect")
                self.loopExit = False
                oled_two_data(2,2,"Pulse","Effect")
                self.pulse_effect()
            elif self.ir_code == 4:  # IR code for Circular Chase
                print("Switching to Sparkle Effect")
                self.loopExit = False
                oled_two_data(2,2,"Sparkle","Effect")
                self.sparkle_effect()
            elif self.ir_code == 5:  # IR code for Circular Chase
                print("Switching to Colorful fade  Effect")
                self.loopExit = False
                oled_two_data(2,2,"Fade","Effect")
                self.colorful_fade_effect()
            
            if self.ir_code == 6:  # IR code for Circular Chase
                print("Switching to Alternating stripes Chase")
                self.loopExit = False
                oled_two_data(2,2,"Stripes","Chase")
                self.alternating_stripes_effect()
            if self.ir_code == 7:  # IR code for Circular Chase
                print("Switching to riplle effect")
                self.loopExit = False
                oled_two_data(2,2,"Ripple","Effect")
                self.ripple_effect(ripple_size=num_pixels)
            if self.ir_code == 8:  # IR code for Circular Chase
                print("Switching to ZigZag effect")
                self.loopExit = False
                oled_two_data(2,2,"ZigZag","Effect")
                self.zigzag_effect()
            if self.ir_code == 9:  # IR code for Circular Chase
                print("Switching to candlelight flicker effect")
                self.loopExit = False
                oled_two_data(2,2,"Candle","Flicker")
                self.candlelight_flicker()
            


def run_activity(activity):
    """Starts the LED effects based on the given activity parameters."""
    global ir_receiver_enabled
    params = get_activity_params(activity)

    # Assuming the activity params include pin and LED count
    led_pin = set_pin_out(params["strip_led_pin"])  # Ensure this function returns a valid Pin object
    num_pixels = int(params["led_num"])
    ir_receiver_enabled=params["remote_enabled"]
    pin_ir=int(params["remote_pin"])
    pin_ir=Pin(pin_ir, Pin.IN) # IR receiver
    # Specify the pins for increment and decrement switches
    increment_pin = 14  # Pin 14 for increment
    decrement_pin = 15  # Pin 15 for decrement
    if ir_receiver_enabled=="Enabled":
        ir = NEC_8(pin_ir, callback)
    
   
    neo_effects = NeoPixelEffects(pin=led_pin, num_pixels=num_pixels, increment_pin=increment_pin, decrement_pin=decrement_pin)
    print("Starting 'Luminous Play: LED light magic' activity")
    neo_effects.run(num_pixels)

