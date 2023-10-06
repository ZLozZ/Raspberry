import paho.mqtt.client as mqtt
from time import sleep
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor

senkc = GroveUltrasonicRanger(16)
senlight = GroveLightSensor(0)
lcd = JHD1802()
sensor = DHT('11', 5)

client = mqtt.Client("FyoHKCcKODwYBh0lNwg8HQs")
client.username_pw_set(username="FyoHKCcKODwYBh0lNwg8HQs", password="izkBa7E9esqJkLRUvYb8N3XQ")
client.connect("mqtt3.thingspeak.com", 1883, 60)


def thingspeak_mqtt(d1, d2, d3, d4):
    channel_ID = "2256756"
    client.publish("channels/%s/publish" % (channel_ID),
                   "field1=%s&field2=%s&field3=%s&field4=%s&status=MQTTPUBLISH'" % (d1, d2, d3, d4))


while True:
    try:
        humi, temp = sensor.read()
        light = senlight.light
        kc = round(senkc.get_distance(), 3)
        print('Nhiet do{}C, Do am{}%'.format(temp, humi))
        print('{} cm'.format(kc))
        print('light value {}'.format(light))

        lcd.setCursor(0, 0)
        lcd.write('{}C,{}%,{}cm'.format(temp, humi, kc))
        lcd.setCursor(1, 0)
        lcd.write('light value {}'.format(light))

        thingspeak_mqtt(temp, humi, light, kc)
        sleep(20)
    except:
        print('no internet')

