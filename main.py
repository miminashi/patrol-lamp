print "Hello, isaac!"

import os
import time
import datetime
import traceback
import mraa
from mqtt_client import MqttClient
from twitter import *

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
SCREEN_NAME = os.environ["TWITTER_SCREEN_NAME"]

def dot():
    gpio.write(1)
    time.sleep(0.1)
    gpio.write(0)
    time.sleep(0.1)

def dash():
    gpio.write(1)
    time.sleep(0.3)
    gpio.write(0)
    time.sleep(0.1)

def word_space():
    time.sleep(0.2)


def on_mqtt_connect(client, userdata, rc):
    print("Connected MQTT with result code "+str(rc))
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.subscribe("/button/#")

def on_mqtt_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "/button/small":
        for i in xrange(3):
           gpio.write(1)
           time.sleep(0.1)
           gpio.write(0)
           time.sleep(0.1)
    elif msg.topic == "/button/big":
        for i in xrange(3):
           gpio.write(1)
           time.sleep(0.3)
           gpio.write(0)
           time.sleep(0.1)
    elif msg.topic == "/button/demo":
        # H
        dot()
        dot()
        dot()
        dot()
        word_space()

        # A
        dot()
        dash()
        word_space()

        # J
        dot()
        dash()
        dash()
        dash()
        word_space()

        # I
        dot()
        dot()
        word_space()

        # M
        dash()
        dash()
        word_space()

        # E
        dot()
        word_space()

        # T
        dash()
        word_space()

        # E
        dot()
        word_space()

        # N
        dash()
        dot()
        word_space()

        # O
        dash()
        dash()
        dash()
        word_space()

        # O
        dash()
        dash()
        dash()
        word_space()
       
        # T
        dash()
        word_space()
        
        # O
        dash()
        dash()
        dash()
        word_space()


gpio = mraa.Gpio(13)
gpio.dir(mraa.DIR_OUT)

# boot time ring
gpio.write(1)
time.sleep(1.0)
gpio.write(0)

# MQTT
mqtt_client = MqttClient(os.environ['MQTT_URL'])
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.connect()
mqtt_client.loop_start()

# Twitter
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

