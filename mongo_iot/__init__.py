"""
base package for all things mongo_iot demo
"""
import RPi.GPIO as GPIO

__VERSION__ = [0, 0, 1, 'alpha']

def init():
    # should normally be done at end but could crash so there is that
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
