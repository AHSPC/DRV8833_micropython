## DRV8833

Pure MicroPython driver for the DRV8833 motor driver (intended for [Adafruit's model](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-drv8833-dc-stepper-motor-driver-breakout-board.pdf), but should work with any).

Example usage (tested with an RPI Pico):

```python
from machine import Pin, PWM
from drv8833 import DRV8833
from time import sleep

# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors; notable, it changes the motors'
# behavior at low throttle values. We recommend values no lower than 1,000 and no higher than 200,000.
# 20,000 is a good default.
# The lower the value, the slower the motor seems
frequency = 20_000

# Make sure to set the correct pins!
ain1 = PWM(Pin(0, Pin.OUT), freq=frequency)
ain2 = PWM(Pin(1, Pin.OUT), freq=frequency)
bin1 = PWM(Pin(2, Pin.OUT), freq=frequency)
bin2 = PWM(Pin(3, Pin.OUT), freq=frequency)

drv = DRV8833(ain1, ain2, bin1, bin2)

throttle = 1.0
while throttle > -1.0:
    drv.throttle_a(throttle)
    drv.throttle_b(throttle)
    sleep(0.1)
    throttle -= 0.05
    print(throttle)
    
drv.stop_a()
drv.stop_b()

# Will be called automatically when DRV8833 object leaves scope, but can be called manually
drv.deinit()
```
