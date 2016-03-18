import time
import datetime
import traceback
import mraa
from twitter import *

CONSUMER_KEY = "iHG2y6wNbeqpVELTQjxE6GZLz"
CONSUMER_SECRET = "SPnOJnLcnruut2OZBKCtUE5FbKQZcMRkB98Hsf3x4k252hldOQ"
ACCESS_TOKEN = "709006709063163904-F7v7t5aCeM9EbonhTMpqSLA5gnQKnPO"
ACCESS_TOKEN_SECRET = "l9XVYNB2tfO4duRqITXa4ZhKYw4fS9fCkvvfz2XtgbX6G"
SCREEN_NAME = "isaac_iot"

print "hello"
#raise Exception('spam', 'eggs')

gpio = mraa.Gpio(13)
gpio.dir(mraa.DIR_OUT)

gpio.write(1)
time.sleep(1.0)
gpio.write(0)

auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


t = Twitter(auth=auth)
message = "AC Control Box started at " + str(datetime.datetime.now())

while True:
    try:
        t.statuses.update(status=message)
        print "Tweeted!"
        break
    except Exception as e:
        #print "Twitter error({0}): {1}".format(e.errno, e.strerror)
        print traceback.format_exc()
        time.sleep(1.0)

twitter_stream = TwitterStream(auth=auth, domain="userstream.twitter.com")
for msg in twitter_stream.user():
    if "in_reply_to_screen_name" in msg and "text" in msg:
        if msg["in_reply_to_screen_name"] == SCREEN_NAME:
            print msg["text"]
            for i in xrange(3):
                gpio.write(1)
                time.sleep(0.2)
                gpio.write(0)
                time.sleep(0.2)

