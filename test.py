from machine import Pin, PWM
from drv8833 import DRV8833
from time import sleep

Pin("LED").on()
sleep(1)
Pin("LED").off()

# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors; notable, it changes the motors'
# behavior at low throttle values. We recommend values no lower than 1,000 and no higher than 200,000.
# 10,000 is a good default.
frequency = 40000

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

# throttle = 1.0
# while throttle > -1.0:
#     drv.throttle_a(throttle)
#     drv.throttle_b(throttle)
#     sleep(0.1)
#     throttle -= 0.05
#     print(throttle)
#
# drv.stop_a()
# drv.stop_b()
#
# sleep(1)

for i in range(10):
    drv.throttle_a(0.5)
    drv.throttle_b(0.5)
    sleep(1)
    drv.stop_a()
    drv.stop_b()
    sleep(1)

# Will be called automatically when DRV8833 object leaves scope, but can be called manually
# drv.deinit()





######
# 1. Is it true that the pico can NOT produce 5V in VBUS unless it is powered via USB?
#    - We currently believe that VBUS is inherently linked with the USB connection,
#      hence no; the VBUS is only used to get power straight from a USB connection.
# 2. Is it harmful to power the pico with 5v through VSYS AND 5v through USB?
#    - https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
#    - Page 19: with proper shottky diode, this is perfectly fine!!
