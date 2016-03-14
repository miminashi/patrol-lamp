import time
import mraa
import yaml
import paho.mqtt.client as mqtt

CA_CERTS_FILE = "/etc/ssl/certs/ca-certificates.crt"

with open(".env.example", "r") as f:
    dic = yaml.load(f)
    HOST = dic.get("HOST")
    PORT = dic.get("PORT")
    USERNAME = dic.get("USERNAME")
    PASSWORD = dic.get("PASSWORD")

gpio = mraa.Gpio(13)
gpio.dir(mraa.DIR_OUT)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("honban/pat-lamp")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
  
    gpio.write(1)
    time.sleep(3)
    gpio.write(0)


if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(CA_CERTS_FILE)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(HOST, PORT, 60)
    client.loop_forever()
