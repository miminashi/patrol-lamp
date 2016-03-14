import time
import mraa
import yaml
import paho.mqtt.client as mqtt

with open(".env", "r") as f:
    dic = yaml.load(f)
    HOST = dic.get("HOST")
    PORT = dic.get("PORT")
    USERNAME = dic.get("USERNAME")
    PASSWORD = dic.get("PASSWORD")

gpio = mraa.Gpio(13)
gpio.dir(mraa.DIR_OUT)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test/led")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
  
    for unuse in range(5):
        gpio.write(1)
        time.sleep(0.1)

        gpio.write(0)
        time.sleep(0.9)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(HOST, PORT, 60)
    client.loop_forever()
