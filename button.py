from websocket import create_connection
from builderProtocole import BuilderProtocole
import RPi.GPIO as GPIO
import dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ws = create_connection("ws://localhost:8000")
print(ws.recv())
try:
    while True:
        if GPIO.input(10) == GPIO.HIGH:
            print('button push')
            ws.send(BuilderProtocole("button",[1]).build())
        if GPIO.input(10) == GPIO.LOW:
            print('not button push')
            ws.send(BuilderProtocole("button",[0]).build())
        #time.sleep(0)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Quit the loop...")
ws.close()
