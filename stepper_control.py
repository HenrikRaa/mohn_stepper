import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 24
# Step pin from controller
STEP = 23
# Holding current pin
HOLD = 25
# Limit-switch pin
LIMIT = 22 
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Number of steps
step_num = 40000

# Step delays (seconds)
step_delay_high = 0.0005
step_delay_low  = 0.0005

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(HOLD, GPIO.OUT)
GPIO.setup(LIMIT, GPIO.IN)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)

# Enable/diasable holding
GPIO.output(HOLD, GPIO.LOW)

def read_limit_switch():
    if GPIO.input(LIMIT):
        print("true")
        return True
    else:
        print("false")
        return False
    
    sleep(0.01)

try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		# Esablish the direction you want to go
		GPIO.output(DIR,CW)
		
        
		# Run for 200 steps. This will change based on how you set you controller
		for x in range(step_num):

			# Set one coil winding to high
			GPIO.output(STEP,GPIO.HIGH)
			# Allow it to get there.
			sleep(step_delay_high) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low) # Dictates how fast stepper motor will run
			
			read_limit_switch()
			
		print("changing directions")

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		GPIO.output(DIR,CCW)
		for x in range(step_num):
			GPIO.output(STEP,GPIO.HIGH)
			sleep(step_delay_high)
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low)
			
			read_limit_switch()

# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()
	


