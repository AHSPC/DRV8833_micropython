## DRV8833

Pure MicroPython driver for the DRV8833 motor driver (intended for [Adafruit's model](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-drv8833-dc-stepper-motor-driver-breakout-board.pdf), but should work with any).

Example usage:

```python
from machine import Pin
from drv8833.py import DRV8833
from time import sleep

# Make sure to set the correct pins!
# NOTE: feel free to play with the frequency value (I'm not fully sure of it's effect, but I know if does something!)
motor_a_pin_1 = PWM(Pin(0, Pin.OUT), freq=50_000)
motor_a_pin_2 = PWM(Pin(0, Pin.OUT), freq=50_000)
motor_b_pin_1 = PWM(Pin(0, Pin.OUT), freq=50_000)
motor_b_pin_2 = PWM(Pin(0, Pin.OUT), freq=50_000)

drv = DRV8833(motor_a_pin_1, motor_a_pin_2, motor_b_pin_1, motor_b_pin_2)

drv.throttle_a(0.5)
sleep(2)
drv.stop_a()

# Will be called automatically when DRV8833 object leaves scope, but can be called manually
drv.deinit()
