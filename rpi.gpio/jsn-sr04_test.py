#!/usr/bin/env python3

"""Tests JSN-SR04 Ping Sonar using RPi.GPIO."""

import RPi.GPIO as GPIO
import sys
import time

_HC_SR04_RANGE_MIN = 25     # Sonar minimun range (cm) (Theorical Min: 25)
_HC_SR04_RANGE_MAX = 300    # Sonar maximun range (cm) (Theorical Max: 450)
_ECHO_TIMEOUT = 2           # timeout 2 sg

def do_sonar_things(pin_trig, pin_echo):
    # setup pin mode
    GPIO.setup(pin_trig, GPIO.OUT)
    GPIO.setup(pin_echo, GPIO.IN)

    try:
        while True:
            # stabilize trigger signal
            GPIO.output(pin_trig, 0)
            time.sleep(1)    # 1 s (Min time between measures: 20 ms)

            # send trigger pulse: HIGH 10us
            GPIO.output(pin_trig, 1)
            time.sleep(25E-6)    # 25us (min: 10us)
            GPIO.output(pin_trig, 0)

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
            if _HC_SR04_RANGE_MIN <= dist <= _HC_SR04_RANGE_MAX:
                print("Distance:", dist)
            else:
                print("Out of Range")
            #print("Distance:", dist)

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