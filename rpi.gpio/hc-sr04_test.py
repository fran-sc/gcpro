#!/usr/bin/env python3

"""Tests HC-SR04 Ping Sonar using RPi.GPIO."""

import RPi.GPIO as GPIO
import sys
import time

_HC_SR04_RANGE_MIN = 2      # Sonar minimun range (cm)
_HC_SR04_RANGE_MAX = 100    # Sonar maximun range (cm) (Theorical Max: 400)

def do_sonar_things(pin_trig, pin_echo):
    # setup pin mode
    GPIO.setup(pin_trig, GPIO.OUT)
    GPIO.setup(pin_echo, GPIO.IN)

    try:
        while True:
            # stabilize trigger signal
            GPIO.output(pin_trig, 0)
            time.sleep(5E-6)    # 5us

            # send trigger pulse: HIGH 10us
            GPIO.output(pin_trig, 1)
            time.sleep(1E-5)    # 10us            

            # wait for HIGH in echo
            while GPIO.input(pin_echo) == False: pass

            # get current time
            cur_time = time.time()

            # wait for LOW in echo
            while GPIO.input(pin_echo) == True: pass            

            # get time difference
            time_diff = time.time() - cur_time

            # calculate distance
            dist = (time_diff/2) * 34320   # 34320 cm/sg

            # show result
            """
            if _HC_SR04_RANGE_MIN <= dist <= _HC_SR04_RANGE_MAX:
                print("Distance:", dist)
            else:
                print("Out of Range")
            """
            print("Distance:", dist)

            time.sleep(0.25)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc != 3):
        print("uso: " + sys.argv[0] + " <Trigger_BCM_pin> <Echo_BCM_pin>")
        exit()    

    # init GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # init "get distances" loop
    do_sonar_things(int(sys.argv[1]), int(sys.argv[2]))

    # cleanup GPIO pin's
    GPIO.cleanup()

    print("\nBye!!")    