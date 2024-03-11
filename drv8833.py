from machine import PWM, Pin

class DRV8833:

    def throttle_a(self, throttle: float):
        self.__throttle(self.motor_a_pin_1, self.motor_a_pin_2, throttle)

    def throttle_b(self, throttle: float):
        self.__throttle(self.motor_b_pin_1, self.motor_b_pin_2, throttle)

    def stop_a(self):
        self.__stop(self.motor_a_pin_1, self.motor_a_pin_2)

    def stop_b(self):
        self.__stop(self.motor_b_pin_1, self.motor_b_pin_2)

    def deinit(self):
        self.stop_a()
        self.stop_b()
        self.motor_a_pin_1.deinit()
        self.motor_a_pin_2.deinit()
        self.motor_b_pin_1.deinit()
        self.motor_b_pin_2.deinit()
        pass

    def __stop(self, pin1: PWM, pin2: PWM):
        pin1.duty_u16(self.min_duty_cycle)
        pin2.duty_u16(self.min_duty_cycle)

    def __throttle(self, pin1: PWM, pin2: PWM, throttle: float):
        duty_cycle = throttle * (self.max_duty_cycle - self.min_duty_cycle) + self.min_duty_cycle
        match throttle:
            case 0:
                self.__stop(pin1, pin2)
            case x if x > 0:
                pin1.duty_u16(duty_cycle)
                pin2.duty_u16(self.min_duty_cycle)
            case x if x < 0:
                pin1.duty_u16(duty_cycle)
                pin2.duty_u16(self.min_duty_cycle)

    def __init__(self, motor_a_pin_1: PWM, motor_a_pin_2: PWM, motor_b_pin_1: PWM, motor_b_pin_2: PWM, max_duty_cycle = 65535, min_duty_cycle = 0) -> None:
        self.motor_a_pin_1 = motor_a_pin_1
        self.motor_a_pin_2 = motor_a_pin_2
        self.motor_b_pin_1 = motor_b_pin_1
        self.motor_b_pin_2 = motor_b_pin_2
        self.max_duty_cycle = max_duty_cycle
        self.min_duty_cycle = min_duty_cycle

    def __del__(self):
        self.deinit()
