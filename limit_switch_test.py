import RPi.GPIO as GPIO
from time import sleep

# Limit-switch pin
LIMIT = 22
# Holding current pin
HOLD = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(LIMIT, GPIO.IN)
GPIO.setup(HOLD, GPIO.OUT)

GPIO.output(HOLD, GPIO.LOW) 

try:
    while True:
        
        if GPIO.input(LIMIT):
            print("input high")
        else:
            print("input low")
        
        sleep(0.01)
    
# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()