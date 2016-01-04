import RPi.GPIO as GPIO
from time import sleep

in_pin = 0

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
  while True:
    input_state = GPIO.input(in_pin)
    if input_state == False:
      print('Button Pressed')
      sleep(0.2)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()

