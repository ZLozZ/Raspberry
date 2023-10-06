
import json, urllib
from urllib import request, parse
from time import sleep
from random import randint

def make_param_thingspeak(data1, data2):
    params = parse.urlencode({'field1':data1,'field2':data2}).encode()
    return params

def thing_speak_post(params):
    api_key_write = "5Y2EQSLEMU6HGSQI"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(req, data=params)
    respone_data=r.read()
    return respone_data

while True:
    try:
        data_random1=randint(0, 200)
        data_random2=randint(0, 333)
        print(data_random2)
        params_thingspeak=make_param_thingspeak(data_random1, data_random2)
        thing_speak_post(params_thingspeak)
        sleep(20)
    except:
        print("Not Connect.")
        print("Reconnect",end="")
        for i in range(10):
            print('.', end='')
        print()
        sleep(1)