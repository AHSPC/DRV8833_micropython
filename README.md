## DRV8833

Pure MicroPython driver for the DRV8833 motor driver (intended for [Adafruit's breakout board](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-drv8833-dc-stepper-motor-driver-breakout-board.pdf), but should work with any).

For a similar (and more thorough) driver but written in CircuitPython, see [adafruit_circuitpython_motor](https://github.com/adafruit/Adafruit_CircuitPython_Motor/blob/0c598f67c4688f0108b9671c2834ef343032906b/adafruit_motor/motor.py#L6).

Example usage (tested with an RPI Pico):

```python
from machine import Pin, PWM
from drv8833 import DRV8833
from time import sleep

Pin("LED").on()
sleep(1)
Pin("LED").off()

# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors, especially at low throttle
# values. (based on very brief testing) We recommend values no lower than 1,000 and no higher than
# 200,000. 40,000 is a good default.
frequency = 40_000

# Make sure to set the correct pins!
ain1 = PWM(Pin(15, Pin.OUT))
ain2 = PWM(Pin(14, Pin.OUT))
bin1 = PWM(Pin(13, Pin.OUT))
bin2 = PWM(Pin(12, Pin.OUT))
ain1.freq(frequency)
ain2.freq(frequency)
bin1.freq(frequency)
bin2.freq(frequency)

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

# This will be called automatically when DRV8833 object leaves scope, but can be called manually if you want
# drv.deinit()
```
