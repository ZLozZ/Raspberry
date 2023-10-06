import http.client as httplib
import json
from urllib import request, parse
from time import sleep
from gpiozero import LED
from grove.display.jhd1802 import JHD1802
from seeed_dht import DHT
from datetime import datetime, time

buzzer = LED(12)
led = LED(26)
relay = LED(16)
lcd = JHD1802()
sensor = DHT('11', 5)
beginTime = time(10, 10)
finishTime = time(10, 11)


def make_param_thingspeak(sensor1, sensor2):
    params = parse.urlencode({'field1': sensor1, 'field2': sensor2}).encode()
    return params


def thingspeak_post(params):
    api_key_write = "5Y2EQSLEMU6HGSQI"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    request.urlopen(req, data=params)


def thingspeak_get():
    value = list()
    req = request.Request("https://api.thingspeak.com/channels/2255818/feeds.json?api_key=SGQHMWME0KLO89N3",
                          method="GET")
    req = request.urlopen(req)
    response_data = req.read().decode()
    response_data = json.loads(response_data)
    d = response_data.get("feeds")[-1]
    value.append(d.get("field3"))
    value.append(d.get("field4"))
    value.append(d.get("field5"))
    value.append(d.get("field6"))
    return value


auto = -1
while True:
    value = thingspeak_get()
    print(value)
    time = datetime.now().time()
    print(time)
    if value[3] == 1:
        auto = 1
    if value[3] == 0:
        auto = 0

    if (auto == 0):
        humi, temp = sensor.read()
        lcd.setCursor(0, 0)
        lcd.write('Temp:{}C'.format(temp))
        lcd.setCursor(0, 9)
        lcd.write('hum:{}%'.format(humi))
        lcd.setCursor(1, 0)
        lcd.write('{}'.format(time))
        params_thingspeak = make_param_thingspeak(humi, temp)
        thingspeak_post(params_thingspeak)
        if (value[1] == '1'):
            buzzer.on()
        elif (value[1] == '0'):
            buzzer.off()

        if (value[2] == '1'):
            relay.on()
        elif (value[2] == '0'):
            relay.off()

        if value[0] == '1':
            led.on()
        elif value[0] == '0':
            led.off()

    if auto == 1:
        humi, temp = sensor.read()
        lcd.setCursor(0, 0)
        lcd.write('Temp:{}C'.format(temp))
        lcd.setCursor(0, 9)
        lcd.write('hum:{}%'.format(humi))
        params_thingspeak = make_param_thingspeak(humi, temp)
        thingspeak_post(params_thingspeak)
        lcd.setCursor(1, 0)
        lcd.write('{}'.format(time))
        if (temp > 37):
            buzzer.on()
        elif temp < 31:
            buzzer.off()

        if (humi > 90):
            relay.on()
        elif humi < 60:
            relay.off()

        if beginTime <= time <= finnishTime:
            led.on()
        else:
            led.off()
    print("----------------------")
