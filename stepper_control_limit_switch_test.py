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
step_num = 3500

# Step delays (seconds)
step_delay_high = 0.001
step_delay_low  = 0.001

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

i = 0
switch_state = False

try:
	# Run forever.
	while True:
		sleep(1.0)
		# Esablish the direction you want to go
		GPIO.output(DIR,CW)
		
		switch_state = read_limit_switch()
        
		# Run for 200 steps. This will change based on how you set you controller
		while not switch_state:
			GPIO.output(STEP,GPIO.HIGH)
			sleep(step_delay_high)
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low)
			i += 1
			switch_state = read_limit_switch()
		
		i = 0
        
		print(f"changing directions, did {i} steps")
		
		sleep(1.0)
		GPIO.output(DIR,CCW)
		
		switch_state = read_limit_switch()
		
		while not switch_state:
			GPIO.output(STEP,GPIO.HIGH)
			sleep(step_delay_high)
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low)
			i += 1
			switch_state = read_limit_switch()
		
		i = 0
		
		print(f"changing directions, did {i} steps")

# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()

