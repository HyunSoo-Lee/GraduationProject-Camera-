import time
import RPi.GPIO as GPIO
import threading

stop_event = threading.Event()

def motor():
    GPIO.setmode(GPIO.BCM)
    StepPins = [12,16,20,21]

    for pin in StepPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    StepCounter = 0

    StepCount = 4

    Seq = [[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0]]


    while True:
        if stop_event.is_set():
            break
        for pin in range(0,4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += 1

        if (StepCounter == StepCount):
            StepCounter = 0
        if (StepCounter < 0):
            StepCounter = StepCount

        time.sleep(0.01)

def On(second = 30):
    thread = threading.Thread(target = motor)
    thread.start()
    time.sleep(second)
    stop_event.set()
    thread.join()
    GPIO.cleanup()