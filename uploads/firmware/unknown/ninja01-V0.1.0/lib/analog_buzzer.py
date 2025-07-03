from machine import Pin, PWM
import time

class AnalogBuzzer:
    is_enabled=True
    
    def __init__(self, pin_number,enOrDi=True, frequency=1000, duty=512):
        """
        Initialize the buzzer with a specified GPIO pin.
        pin_number: GPIO pin to which the buzzer is connected.
        frequency: The frequency (Hz) of the sound. Default is 1000 Hz.
        duty: The PWM duty cycle. Default is 512 (50%).
        """
        self.is_enabled=enOrDi
#         print(f"Is enabled:{self.is_enabled}")
        if  self.is_enabled==True:
            self.buzzer_pin = Pin(pin_number, Pin.OUT)  # Set pin as output
            self.pwm = PWM(self.buzzer_pin)  # Create PWM object
            self.pwm.freq(frequency)  # Set the frequency for sound
            self.pwm.duty(duty)  # Set the PWM duty cycle (volume)

    def play_tone(self, frequency, duration):
        """
        Play a specific tone for a given duration.
        frequency: Frequency of the tone (in Hz).
        duration: Duration to play the tone (in seconds).
        """
        if self.is_enabled==True:
            self.pwm.freq(frequency)  # Change the frequency for the desired tone
            self.pwm.duty(512)  # Set a duty cycle for the sound
            time.sleep(duration)  # Play the tone for the duration
            self.stop()  # Stop playing after duration

    def stop(self):
        """Stop the buzzer sound."""
        if self.is_enabled==True:
            self.pwm.duty(0)  # Set duty cycle to 0 to stop the buzzer

    def change_frequency(self, frequency):
        """Change the frequency of the buzzer."""
        if self.is_enabled==True:
            self.pwm.freq(frequency)  # Update the frequency

    def change_duty(self, duty):
        """Change the volume (duty cycle) of the buzzer."""
        if self.is_enabled==True:
            self.pwm.duty(duty)  # Update the duty cycle (0-1023)

# # Example usage:
# # Create an instance of the AnalogBuzzer class
# buzzer = AnalogBuzzer(pin_number=32)  # Change GPIO pin as needed
# 
# # Play a tone of 1000Hz for 2 seconds
# buzzer.play_tone(1000, 2)
# 
# # Change to a different frequency (e.g., 2000Hz)
# buzzer.change_frequency(2000)
# 
# # Play a tone of 2000Hz for 1 second
# buzzer.play_tone(2000, 1)
# 
# # Stop the buzzer
# buzzer.stop()
