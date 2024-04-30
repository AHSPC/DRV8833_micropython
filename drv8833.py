from machine import PWM


class DRV8833:
    """
    Basic helper class to manipulate the DRV8833 dual motor controller.
    Partially based on adafruit's adafruit_motor library, but with custom
    decisions made for our usecases. NOTE: this helper does not currently
    support both stopping methods (high-z and low-z), but only uses low-z.
    Note about throttle()'s decay_mode parameter: SLOW_DECAY is recommended
    to improve spin threshold, speed-to-throttle linearity, and PWM
    frequency sensitivity. We use this as the default.
    """

    FAST_DECAY = 0
    SLOW_DECAY = 1
    MAX_DUTY_CYCLE = 0xFFFF  # 65535
    MIN_DUTY_CYCLE = 0

    def throttle_a(self, throttle: float, decay_mode: int = SLOW_DECAY):
        self.__throttle(self.motor_a_in_1, self.motor_a_in_2, throttle, decay_mode)

    def throttle_b(self, throttle: float, decay_mode: int = SLOW_DECAY):
        self.__throttle(self.motor_b_in_1, self.motor_b_in_2, throttle, decay_mode)

    def stop_a(self, hard: bool = False):
        if hard:
            self.throttle_a(0.0)
        else:
            self.__stop(self.motor_a_in_1, self.motor_a_in_2)

    def stop_b(self, hard: bool = False):
        if hard:
            self.throttle_b(0.0)
        else:
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
        pin1.duty_u16(self.MIN_DUTY_CYCLE)
        pin2.duty_u16(self.MIN_DUTY_CYCLE)

    def __throttle(self, pin1: PWM, pin2: PWM, throttle: float, decay_mode: int):
        if not -1.0 <= throttle <= 1.0:
            raise ValueError("Throttle value is out of range [ -1, 1 ]!")

        duty_cycle = int(abs(throttle) * self.MAX_DUTY_CYCLE)
        if throttle == 0:
            self.__stop(pin1, pin2)
        if decay_mode == self.SLOW_DECAY:
            if 0 < throttle <= 1:
                pin1.duty_u16(self.MAX_DUTY_CYCLE - duty_cycle)
                pin2.duty_u16(self.MAX_DUTY_CYCLE)
            elif -1 <= throttle < 0:
                pin1.duty_u16(self.MAX_DUTY_CYCLE)
                pin2.duty_u16(self.MAX_DUTY_CYCLE - duty_cycle)
        elif decay_mode == self.FAST_DECAY:
            if 0 < throttle <= 1:
                pin1.duty_u16(self.MIN_DUTY_CYCLE)
                pin2.duty_u16(duty_cycle)
            elif -1 <= throttle < 0:
                pin1.duty_u16(duty_cycle)
                pin2.duty_u16(self.MIN_DUTY_CYCLE)
        else:
            raise ValueError(
                "decay_mode must be one of either FAST_DECAY or SLOW_DECAY!"
            )

    def __init__(self, ain1, ain2: PWM, bin1: PWM, bin2: PWM) -> None:
        self.motor_a_in_1 = ain1
        self.motor_a_in_2 = ain2
        self.motor_b_in_1 = bin1
        self.motor_b_in_2 = bin2

    def __del__(self):
        self.deinit()
