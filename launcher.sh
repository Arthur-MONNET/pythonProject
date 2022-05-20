sleep 5
cd /home/pi/Documents/pythonProject/pythonProject/
echo "start server" &
python server.py &
sleep 5
echo "start components" &
python button.py play 14 &
python button.py onoff 15 &
python volume.py &
sudo python blueTile.py BCN-727 5 &
