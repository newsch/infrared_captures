#!/usr/bin/env python3
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep


def get_filename(base_string='IMG_',
                 destination='/home/pi/infrared_captures/DCIM/',
                 extension='.jpg'):
    """ Find a filename that won't overwrite existing art.
        Do this in a roudabout way of finding all the current art files that
        follow a convention of base_string + an_int + extension in the
        destination folder, finding the largest an_int, and +1-ing that to get
        the returned filename.
        The irony of this is that in the process of writing
        and testing this function many arts were created and overwritten.
        returns: filename as a string
    """
    import glob
    files = glob.glob(destination + base_string + '*' + extension)
    # parse number out of filename and get biggest one
    big_int = 1
    for filename in files:
        int_begin = filename.rfind(base_string) + len(base_string)
        int_end = filename.find(extension)
        new_int = filename[int_begin:int_end]
        # check to make sure this is really an int and if it's bigger or not
        if new_int.isdigit():
            new_int = int(new_int.lstrip('0'))
            if new_int > big_int:
                big_int = new_int

    bigger_int = big_int + 1  # make a bigger int for the new filename
    an_uncontroversial_filename = destination + base_string \
        + '%04d' % bigger_int + extension
    return(an_uncontroversial_filename)

def take_picture(stuff=None):
    print('Taking picture')
    GPIO.output(led_pin['green'], GPIO.LOW)
    GPIO.output(led_pin['red'], GPIO.HIGH)
    camera.capture(get_filename())
    GPIO.output(led_pin['red'], GPIO.LOW)
    GPIO.output(led_pin['green'], GPIO.HIGH)

# set up GPIO
input_pin = {'shutter': 17,
             'toggle': 18,}
led_pin = {'red': 24,
           'green': 22,
           'blue': 23,}

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin['shutter'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_pin['toggle'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin['red'], GPIO.OUT)
GPIO.setup(led_pin['green'], GPIO.OUT)
GPIO.setup(led_pin['blue'], GPIO.OUT)

GPIO.add_event_detect(input_pin['shutter'], GPIO.RISING, callback=take_picture, bouncetime=500)

camera = PiCamera()

try:
    print('Starting camera')
    GPIO.output(led_pin['green'], GPIO.HIGH)
    GPIO.wait_for_edge(input_pin['toggle'], GPIO.FALLING)
    print('Cleaning up')
    GPIO.cleanup()
    print('Stopping camera')
except KeyboardInterrupt:
    GPIO.cleanup()
