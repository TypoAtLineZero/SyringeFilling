#!/usr/bin/python3

import RPi.GPIO as GPIO
import time


## Pin Definition
winding1 = 4
winding2 = 17
winding3 = 23
winding4 = 24

buttonGreenFwLong = 10
buttonRedFwShort  = 9
buttonBlueBwShort = 11

ledG = 21 
ledY = 20
ledR = 26


## Stepper motor Definition
step_sleep = 0.00075
step_count = 4096
direction = True
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

## Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(winding1, GPIO.OUT)
GPIO.setup(winding2, GPIO.OUT)
GPIO.setup(winding3, GPIO.OUT)
GPIO.setup(winding4, GPIO.OUT)
GPIO.setup(ledG, GPIO.OUT)
GPIO.setup(ledY, GPIO.OUT)
GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(buttonGreenFwLong, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonRedFwShort, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonBlueBwShort, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


## Init
GPIO.output(winding1, GPIO.LOW)
GPIO.output(winding2, GPIO.LOW)
GPIO.output(winding3, GPIO.LOW)
GPIO.output(winding4, GPIO.LOW)

motor_pins = [winding1, winding2, winding3, winding4]
motor_step_counter = 0


## Function definitions
def cleanup():
    GPIO.output(winding1, GPIO.LOW)
    GPIO.output(winding2, GPIO.LOW)
    GPIO.output(winding3, GPIO.LOW)
    GPIO.output(winding4, GPIO.LOW)
    GPIO.output(ledG, GPIO.LOW)
    GPIO.output(ledY, GPIO.LOW)
    GPIO.output(ledR, GPIO.LOW)



def buttonGreenPressed(channel):
    print("Green Pressed!")

def buttonRedPressed(channel):
    print("Red Pressed!")
    
def buttonBluePressed(channel):
    print("Blue Pressed!")

## main
if __name__ == '__main__':

    ## Register event detection, if button is pressed
    GPIO.add_event_detect(buttonGreenFwLong, GPIO.RISING, callback=buttonGreenPressed, bouncetime=500)
    GPIO.add_event_detect(buttonRedFwShort, GPIO.RISING, callback=buttonRedPressed, bouncetime=500)
    GPIO.add_event_detect(buttonBlueBwShort, GPIO.RISING, callback=buttonBluePressed, bouncetime=500)

    try:
        i = 0
        for i in range(step_count):
            for pin in range(0, len(motor_pins)):
                GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
            if direction == True:
                motor_step_counter = (motor_step_counter - 1) % 8
                GPIO.output(ledG, GPIO.HIGH)
                GPIO.output(ledY, GPIO.HIGH)
                GPIO.output(ledR, GPIO.HIGH)
            elif direction == False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else:
                print("diretion not boolean")
                cleanup()
                exit(1)
            time.sleep(step_sleep)
            
    except KeyboardInterrupt:
        cleanup()
        exit(1)
        
    cleanup()
    exit(0)





