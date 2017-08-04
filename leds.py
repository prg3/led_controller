#!/usr/bin/python

import time
import datetime
from neopixel import *
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.ioloop import PeriodicCallback
import json

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

ledStatus = []

def ledOff(strip, led):
   strip.setPixelColor(led, Color(0,0,0))
   strip.show()

def ledSet(strip, led, red, green, blue):
   color = Color(int(red), int(green), int(blue))
   strip.setPixelColor(int(led) , color )
   strip.show()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class LedAllOff(tornado.web.RequestHandler):
    def get(self):
       for i in range(0, strip.numPixels()-1):
           ledStatus[i]['on'] = 0
           ledStatus[i]['blink'] = 0
       self.set_status(200)

class LedHandler(tornado.web.RequestHandler):
    def get(self, led_id,red,green,blue):
       if int(led_id) < strip.numPixels() or int(led_id) == 0:
         id = int(led_id)
         ledStatus[id]['red'] = int(red)
         ledStatus[id]['blue'] = int(blue)
         ledStatus[id]['green'] = int(green)
         ledStatus[id]['on'] = 1
         self.set_status(200)
       else:
         self.set_status(404)

class LedBlink(tornado.web.RequestHandler):
   def get(self, led_id, blink):
       if int(led_id) < strip.numPixels() or int(led_id) == 0:
         ledStatus[int(led_id)]['blink'] = int(blink)
         self.set_status(200)
       else:
         self.set_status(404)

class LedName(tornado.web.RequestHandler):
   def get(self, led_id, name):
       if int(led_id) < strip.numPixels() or int(led_id) == 0:
         ledStatus[int(led_id)]['name'] = name
         self.set_status(200)
       else:
         self.set_status(404)

class JsonDump(tornado.web.RequestHandler):
   def get(self):
      jsonblob = {
        'data': ledStatus,
        'total': '60',
      }
      self.set_header("Access-Control-Allow-Origin", "*")
      self.write(json.dumps(jsonblob))

class Application(tornado.web.Application):
    def __init__(self):
       handlers = [
           (r"/led/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)", LedHandler),
           (r"/ledoff", LedAllOff),
           (r"/ledblink/([0-9]+)/([0-1])", LedBlink),
           (r"/ledname/([0-9]+)/(.*)", LedName),
           (r"/json", JsonDump),
           (r"/(.*)", tornado.web.StaticFileHandler, {'path': '/home/ubuntu/led_controller/static', 'default_filename' : 'index.html'})
       ]
       settings = dict(

       )
       super(Application, self).__init__(handlers, **settings)

def updateLed():
    for led in ledStatus:
        led_id = led['id']
        if led['blink'] == 0:
            if led['on'] == 0:
                strip.setPixelColor(led_id, Color(0,0,0))
            else:
                strip.setPixelColor(led_id, Color(led['red'], led['green'], led['blue']))
            continue
        elif led['blink'] > 0:
            if led['on'] == 0:
                strip.setPixelColor(led_id, Color(led['red'], led['green'], led['blue']))
                led['on'] = 1
            else:
                strip.setPixelColor(led_id, Color(0,0,0))
                led['on'] = 0
            continue
    strip.show()

if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()
    ledStatus.append({ 'red' : 64, 'blue' : 64, 'green' : 0, 'blink' : 1, 'on' : 1, 'name' : 'Heartbeat', 'id' : 0})
    for i in range(1, strip.numPixels()):
       ledStatus.append({ 'red' : 0, 'blue' : 0, 'green' : 0, 'blink' : 0 , 'on' : 0, 'name' : '', 'id': i })

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen("8080")
    PeriodicCallback(updateLed, 1000/3).start()
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.start()
    print "Foo"
