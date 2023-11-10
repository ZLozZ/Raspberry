# Raspberry 1
import paho.mqtt.client as mqtt
from time import sleep
from gpiozero import LED
import Adafruit_DHT
import json
import datetime
import platform

sensor = Adafruit_DHT.DHT11
gpio = 5
led1 = LED(14)
led2 = LED(15)

def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from Broker")

client = mqtt.Client("Loo_01")
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.username_pw_set(username="Loo1", password="1")
client.connect("192.168.1.3", 1883, 60)

def thingspeak_mqtt(id,data1, data2, data3, data4):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    device_name = platform.node()
    data = {
        "id": id,
        "time": formatted_time,
        "name": device_name,
        "data1": data1,
        "data2": data2,
        "data3": data3,
        "data4": data4
    }
    json_data = json.dumps(data)
    print(json_data)
    client.publish("Loo/publish/json", json_data)

i = 0
status = 0

while True:
    humi, temp = Adafruit_DHT.read_retry(sensor, gpio)

    if status == 0:
        led1.on()
        led2.on()
        status+=1
    else:
        led1.off()
        led2.off()
        status-=1

    thingspeak_mqtt(i, humi,temp, status, status)
    i+=1
    sleep(10)