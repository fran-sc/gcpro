#!/usr/bin/env python3

"""PWM Led using RPi.GPIO."""

import RPi.GPIO as GPIO
import time
import sys

def do_led_things(pin_led):
    # setup pin mode
    GPIO.setup(pin_led, GPIO.OUT)

    # setup pwm signal
    pwm = GPIO.PWM(pin_led, 50)
    pwm.start(0)

    try:
        while True:
            for dc in range(0, 100, 5):
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.1)
            for dc in range(100, 0, -5):
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.1)        
    
    except KeyboardInterrupt:
        pwm.stop()

if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc != 2):
        print("uso: " + sys.argv[0] + " <led_BCM_pin>")
        exit()
    
    # init GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # send pwm signals to the led
    do_led_things(int(sys.argv[1]))

    # cleanup GPIO pin's
    GPIO.cleanup()

    print("\nBye!!")

