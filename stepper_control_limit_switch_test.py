import RPi.GPIO as GPIO
from time import sleep
import csv

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

# true check
true_check = 20

# Number of steps
step_num = 3500

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

# Set the first direction
GPIO.output(DIR, CW)

# Enable/diasable holding
GPIO.output(HOLD, GPIO.LOW)

def read_limit_switch():
    true_counter = 0
    
    while GPIO.input(LIMIT):
        true_counter += 1
        if true_counter >= true_check:
#             print("true")
            return True
#     print("false")
    return False

def write_to_csv(filename, data):
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])

rotation_counter = 0
rotation_step_counter = 0
release_step_counter = 0
switch_state = False

try:
	# Run forever.
	while True:
		
		switch_state = read_limit_switch()
        
		while not switch_state:
			GPIO.output(STEP,GPIO.HIGH)
			sleep(step_delay_high)
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low)
			rotation_step_counter += 1
			switch_state = read_limit_switch()
			
		rotation_counter += 1
			
		print(f"rotation {rotation_counter} complete hit limit-switch, did {rotation_step_counter} steps")
		
		write_to_csv("rotation_data.csv", rotation_step_counter)
		
		rotation_step_counter = 0
		
# 		sleep(1.0)
# 		GPIO.output(DIR,CCW)
		
		switch_state = read_limit_switch()
		
		print(f"run until switch is released")
		
		while switch_state:
			GPIO.output(STEP,GPIO.HIGH)
			sleep(step_delay_high)
			GPIO.output(STEP,GPIO.LOW)
			sleep(step_delay_low)
			release_step_counter += 1
			switch_state = read_limit_switch()
		
		print(f"switch released, did {release_step_counter} steps")
		
		write_to_csv("release_data.csv", release_step_counter)
		
		release_step_counter = 0
#             
# 		while not switch_state:
# 			GPIO.output(STEP,GPIO.HIGH)
# 			sleep(step_delay_high)
# 			GPIO.output(STEP,GPIO.LOW)
# 			sleep(step_delay_low)
# 			step_counter += 1
# 			switch_state = read_limit_switch()
# 		
# 		step_counter = 0
# 		
# 		print(f"changing directions, did {step_counter} steps")
# 		
# 		sleep(1.0)
# 		# Esablish the direction you want to go
# 		GPIO.output(DIR,CW)
# 		
# 		print(f"direction changed, run until switch is released")
# 		
# 		while switch_state:
# 			GPIO.output(STEP,GPIO.HIGH)
# 			sleep(step_delay_high)
# 			GPIO.output(STEP,GPIO.LOW)
# 			sleep(step_delay_low)
# 			step_counter += 1
# 			switch_state = read_limit_switch()
# 		
# 		print(f"switch released, did {step_counter} steps")
# 		
# 		step_counter = 0
# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()

