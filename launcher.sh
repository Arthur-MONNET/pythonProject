#!/bin/sh
# launcher.sh
# Execute POC

cd /home/pi/Documents/pythonProject/pythonProject
python sound.py &
python server.py &
sleep 5
python button.py play 14 &
python button.py onoff 15 &
python volume.py &
python usbListener.py &
sudo python blueTile.py BCN-727 5 &
