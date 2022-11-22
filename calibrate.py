from time import sleep
from machine import Pin, PWM

number_of_pins = 4

claw_pin = 0
shoulder_pin = 1
elbow_pin = 2
rotate_pin = 3

increment = 50
starting_position = 5000
positions = [5000] * number_of_pins

absolute_max_position = 9000
absolute_min_position = 1000

min_positions = [absolute_max_position] * number_of_pins
max_position = [absolute_min_position] * number_of_pins
range_positions = [None] * number_of_pins

range_positions[claw_pin] = [4000,6000]
range_positions[shoulder_pin] = [4000,6000]
range_positions[elbow_pin] = [4000,6000]
range_positions[rotate_pin] = [4000,6000]

led = machine.Pin(25, machine.Pin.OUT)

range_deltas = [None] * number_of_pins

def createPwm(pin):
    pwm = PWM(Pin(pin))
    pwm.freq(50)
    pwm.duty_u16(positions[pin])
    sleep(0.2)
    return pwm

pwms = [None] * number_of_pins
for pin in range(0, number_of_pins):
    print(f'Creating pin {pin} : range : {range_positions[pin]}')
    range_deltas[pin] = range_positions[pin][1] - range_positions[pin][0]
    print(range_positions)
    # Safety checks to reduce risk of blowing servo motors.
    if (range_deltas[pin] < 0):
        raise(f'Min greater than max for pin {pin}. {range_position}')
    if (range_positions[pin][0] < absolute_min_position):
        raise(f'Min position for pin {pin} is below absolute minimum {absolute_min_position}, it is {range_positions[pin][0]}')
    if (range_positions[pin][1] > absolute_max_position):
        raise(f'Max position for pin {pin} is above absolute maximum {absolute_max_position}, it is {range_positions[pin][1]}')    

    pwms[pin] = createPwm(pin)

def moveTo(percentage, pin = 1):
    if (percentage < 0 or percentage > 100):
        raise(f'Move to position should be between 0 and 100, it was {position}')
    target_position = range_positions[pin][0] + 50 * int(int(range_deltas[pin] * percentage / 100) / increment)
    print(f'Moving {pin} to {percentage}% = from position {positions[pin]} to {target_position}')
    delta = increment if target_position > positions[pin] else -increment
    for position in range(positions[pin], target_position, delta):
        pwms[pin].duty_u16(position)
        sleep(0.05)
    positions[pin] = target_position

def rotateTo(percentage):
    moveTo(percentage, rotate_pin)
    
def clawTo(percentage):
    moveTo(percentage, claw_pin)
    
def testRotate():
    rotateTo(0)
    rotateTo(100)

def testClaw():
    clawTo(0)
    clawTo(100)

def flashLed():
    for i in range(0,6):
        led.toggle()
        sleep(0.1)
        
def pause():
    print("pause")
    sleep(0.5)

while True:
    flashLed()
    testClaw()
    pause()
