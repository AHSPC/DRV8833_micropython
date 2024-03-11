from machine import PWM


class DRV8833:
    def throttle_a(self, throttle: float):
        self.__throttle(self.motor_a_in_1, self.motor_a_in_2, throttle)

    def throttle_b(self, throttle: float):
        self.__throttle(self.motor_b_in_1, self.motor_b_in_2, throttle)

    def stop_a(self):
        self.__stop(self.motor_a_in_1, self.motor_a_in_2)

    def stop_b(self):
        self.__stop(self.motor_b_in_1, self.motor_b_in_2)

    def deinit(self):
        self.stop_a()
        self.stop_b()
        self.motor_a_in_1.deinit()
        self.motor_a_in_2.deinit()
        self.motor_b_in_1.deinit()
        self.motor_b_in_2.deinit()
        pass

    def __stop(self, pin1: PWM, pin2: PWM):
        pin1.duty_u16(self.min_duty_cycle)
        pin2.duty_u16(self.min_duty_cycle)
        print("__stop")

    def __throttle(self, pin1: PWM, pin2: PWM, throttle: float):
        duty_cycle = int(
            abs(throttle) * (self.max_duty_cycle - self.min_duty_cycle)
            + self.min_duty_cycle
        )
        if throttle == 0:
            self.__stop(pin1, pin2)
        elif 0 < throttle <= 1:
            pin1.duty_u16(duty_cycle)
            pin2.duty_u16(self.min_duty_cycle)
        elif -1 <= throttle < 0:
            pin1.duty_u16(self.min_duty_cycle)
            pin2.duty_u16(duty_cycle)
        else:
            raise ValueError("Throttle value is out of range [ -1, 1 ]!")

    def __init__(
        self,
        ain1,
        ain2: PWM,
        bin1: PWM,
        bin2: PWM,
        max_duty_cycle=65535,
        min_duty_cycle=0,
    ) -> None:
        self.motor_a_in_1 = ain1
        self.motor_a_in_2 = ain2
        self.motor_b_in_1 = bin1
        self.motor_b_in_2 = bin2
        self.max_duty_cycle = max_duty_cycle
        self.min_duty_cycle = min_duty_cycle

    def __del__(self):
        self.deinit()
