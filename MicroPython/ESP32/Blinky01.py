# MicroPython
# ESP32: Blink the on-board LED

import time
from machine import Pin

a_pin = Pin(2, Pin.OUT)
while True:
    a_pin.value(1)
    print(a_pin.value())
    time.sleep(1)
    a_pin.value(0)
    time.sleep(0.5)
    print(a_pin.value())



