import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
motorR_forward_pin = 23
motorR_backward_pin = 22
motorL_forward_pin = 24
motorL_backward_pin = 25

# GPIO 핀 번호 설정 모드 설정
GPIO.setmode(GPIO.BCM)

# 핀 설정
GPIO.setup(motorR_forward_pin, GPIO.OUT)
GPIO.setup(motorR_backward_pin, GPIO.OUT)
GPIO.setup(motorL_forward_pin, GPIO.OUT)
GPIO.setup(motorL_backward_pin, GPIO.OUT)

def forward():
    GPIO.output(motorR_forward_pin, GPIO.HIGH)
    GPIO.output(motorL_forward_pin, GPIO.HIGH)
    time.sleep(0.5)
    stop()

def backward():
    GPIO.output(motorR_backward_pin, GPIO.HIGH)
    GPIO.output(motorL_backward_pin, GPIO.HIGH)
    time.sleep(1)
    stop()

def left():
    GPIO.output(motorR_forward_pin, GPIO.HIGH)
    GPIO.output(motorL_backward_pin, GPIO.HIGH)
    time.sleep(0.3)
    stop()

def right():
    GPIO.output(motorR_backward_pin, GPIO.HIGH)
    GPIO.output(motorL_forward_pin, GPIO.HIGH)
    time.sleep(0.3)
    stop()

def stop():
    GPIO.output(motorR_forward_pin, GPIO.LOW)
    GPIO.output(motorR_backward_pin, GPIO.LOW)
    GPIO.output(motorL_forward_pin, GPIO.LOW)
    GPIO.output(motorL_backward_pin, GPIO.LOW)

def move():
    while True:
        print(">> Enter a command (w: forward, s: backward, a: left, d: right, q: quit): ")
        command = input()

        if command == 'w':
            forward()
        elif command == 's':
            backward()
        elif command == 'a':
            left()
        elif command == 'd':
            right()
        elif command.lower() == 'q':
            print("Exiting program...")
            stop()
            break
        else:
            print("Invalid command! Please enter w, s, a, d, or q.")

# GPIO 핀 초기화
#GPIO.cleanup()
