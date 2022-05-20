from websocket import create_connection
from builderProtocole import BuilderProtocole
import RPi.GPIO as GPIO
import dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin = 14)

ws = create_connection("ws://localhost:8000")
result = instance.read()

try:
    while True:
        
        result = instance.read()
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            ws.send(BuilderProtocole("temp",[result.temperature,result.humidity]).build())
        
        time.sleep(0)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Quit the loop...")
ws.close()