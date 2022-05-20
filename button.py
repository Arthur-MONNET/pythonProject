from websocket import create_connection
from builderProtocole import BuilderProtocole, ConnectionBuilderProtocole
import RPi.GPIO as GPIO
import dht11
import time
import sys

# python button.py name GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(int(sys.argv[2]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ws = create_connection("ws://localhost:8000")
lastData = ""
print(ws.recv())
ws.send(ConnectionBuilderProtocole("button",sys.argv[1]).build())
try:
    while True:
        if lastData != str(GPIO.input(int(sys.argv[2]))):
            if GPIO.input(int(sys.argv[2])) == GPIO.HIGH:
                ws.send(BuilderProtocole("button",sys.argv[1],[["push",True]]).build())
                time.sleep(1)
            if GPIO.input(int(sys.argv[2])) == GPIO.LOW:
                ws.send(BuilderProtocole("button",sys.argv[1],[["push",False]]).build())
                time.sleep(1)
            lastData = str(GPIO.input(int(sys.argv[2])))
            
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Quit the loop...")
ws.close()
