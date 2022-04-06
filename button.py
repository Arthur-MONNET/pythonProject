from websocket import create_connection
from builderProtocole import BuilderProtocole
import RPi.GPIO as GPIO
import dht11
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(int(sys.argv[2]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ws = create_connection("ws://localhost:8000")
print(ws.recv())
try:
    while True:
        if GPIO.input(int(sys.argv[2])) == GPIO.HIGH:
            print('button push')
            ws.send(BuilderProtocole("button",sys.argv[1],[["push",True]]).build())
        if GPIO.input(int(sys.argv[2])) == GPIO.LOW:
            print('not button push')
            ws.send(BuilderProtocole("button",sys.argv[1],[["push",False]]).build())
        #time.sleep(0)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Quit the loop...")
ws.close()
