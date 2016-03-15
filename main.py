import time
import mraa
from twitter import *

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
SCREEN_NAME = ""

print "hello"

gpio = mraa.Gpio(13)
gpio.dir(mraa.DIR_OUT)

auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=auth, domain="userstream.twitter.com")
for msg in twitter_stream.user():
    if "in_reply_to_screen_name" in msg and "text" in msg:
        if msg["in_reply_to_screen_name"] == SCREEN_NAME:
            print msg["text"]
            for i in xrange(3):
                gpio.write(1)
                time.sleep(1.0)
                gpio.write(0)
                time.sleep(0.5)

