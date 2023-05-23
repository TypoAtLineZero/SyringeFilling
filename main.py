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
step_sleep = 0.001
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


def turnMotor(direction, step_count, step_sleep):
    
    print("direction:", direction)
    print("step_count:", step_count)
    print("step_sleep:", step_sleep)
    
    motor_step_counter = 0
    i = 0
    
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        if direction == True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction == False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else:
            print("diretion not boolean")
            cleanup()
            exit(1)
        time.sleep(step_sleep)


def buttonGreenPressed(channel):
    ## State: Turn forward for longer period
    switchLeds(ledG, ledR)
    direction_green = True
    step_count_green = step_count * 2
    step_sleep_green = step_sleep * 0.75
    
    turnMotor(direction_green, step_count_green, step_sleep_green)
    print("Finished my turn!")
    switchLeds(ledR, ledG)


def buttonRedPressed(channel):
    ## State: Turn forward for shorter period
    switchLeds(ledG, ledR)
    direction_red = True
    step_count_red = step_count / 4
    step_sleep_red = step_sleep * 2
    
    turnMotor(direction_red, int(step_count_red), step_sleep_red)
    print("Finished my turn!")
    switchLeds(ledR, ledG)
    
    
def buttonBluePressed(channel):
    ## State: Turn backwards for shorter period
    switchLeds(ledG, ledR)
    direction_blue = False
    step_count_blue = step_count / 4
    step_sleep_blue = step_sleep * 2
    
    turnMotor(direction_blue, int(step_count_blue), step_sleep_blue)
    print("Finished my turn!")
    switchLeds(ledR, ledG)
    
    
def switchLeds(LedOff, LedOn):
    GPIO.output(LedOff, GPIO.LOW)
    GPIO.output(LedOn, GPIO.HIGH)


## main
if __name__ == '__main__':

    ## Register event detection, if button is pressed
    GPIO.add_event_detect(buttonGreenFwLong, GPIO.RISING, callback=buttonGreenPressed, bouncetime=500)
    GPIO.add_event_detect(buttonRedFwShort, GPIO.RISING, callback=buttonRedPressed, bouncetime=500)
    GPIO.add_event_detect(buttonBlueBwShort, GPIO.RISING, callback=buttonBluePressed, bouncetime=500)
    GPIO.output(ledY, GPIO.HIGH)
    time.sleep(1)
    switchLeds(ledY, ledG)
    ## State: Ready for buttonXPressed
    
    while True:
        try:
            print("Waiting for input..\n")
            time.sleep(5)
        except KeyboardInterrupt:
            cleanup()
            exit(1)





