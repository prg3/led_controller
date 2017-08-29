# Led Controller for Neopixel Led Strip

This is a simple controller for the neopixel LED strips that works with an Raspberry Pi

## Getting Started

### Prerequisites


Install rpi_ws281x from https://github.com/jgarff/rpi_ws281x including the python neopixel module (Instructions in python/README.md)
 - use swig2.0 package for Ubuntu 16.04 as per https://github.com/jgarff/rpi_ws281x/issues/115


Install python-tornado from apt:
```
apt-get install python-tornado
```

### Installation

Checkout the code into /home/ubuntu/led_controller

```
cp /home/ubuntu/led_controller/leds.service /etc/systemd/system
```

Copy the systemctl script and restart
```
sudo systemctl daemon-reload
sudo systemctl start leds
```

You should now see a blinking LED on the lowest numbered LED on the strip as a heartbeat

## Usage

Raw calls to the strip are as follows:

http://ip-address:8080/led/LEDID/RED/GREEN/BLUE

Where LEDID is the ID of the LED itself, RED, GREEN, BLUE are the values from 0 to 255 that you want the color to be set to

http://ip-address:8080/ledblink/LEDID/BLINKVAL

Where LEDID is the ID of the LED itself and BLINKVAL is either 0 or 1 to enable or disable blinking

http://ip-address:8080/ledoff

Turns off all LEDs
