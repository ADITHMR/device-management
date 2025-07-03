from machine import Pin, PWM

class Servo:
    # these defaults work for the standard TowerPro SG90
    __servo_pwm_freq = 50
    __min_u10_duty = 26 + 10  # offset for correction
    __max_u10_duty = 123 - 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001
    is_enabled = True

    def __init__(self, pin, enOrDi=True):
        self.is_enabled = enOrDi
        self.__initialise(pin)

    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        if self.is_enabled:
            self.__servo_pwm_freq = servo_pwm_freq
            self.__min_u10_duty = min_u10_duty
            self.__max_u10_duty = max_u10_duty
            self.min_angle = min_angle
            self.max_angle = max_angle
            self.__initialise(pin)

    def move(self, angle):
        if self.is_enabled:  # Only move if enabled
            angle = round(angle, 2)
            # Ensure the angle is within range
            if angle < self.min_angle:
                angle = self.min_angle
            elif angle > self.max_angle:
                angle = self.max_angle

            # Allow a small margin to avoid unnecessary movements due to floating-point precision
            if abs(angle - self.current_angle) < 0.1:
                return

            self.current_angle = angle
            # calculate the new duty cycle and move the motor
            duty_u10 = self.__angle_to_u10_duty(angle)
            self.__motor.duty(duty_u10)

    def __angle_to_u10_duty(self, angle):
        if self.is_enabled:
            return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty

    def __initialise(self, pin):
        if self.is_enabled:
            self.current_angle = -0.001
            self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
            self.__motor = PWM(Pin(pin))
            self.__motor.freq(self.__servo_pwm_freq)
