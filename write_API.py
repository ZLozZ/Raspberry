# gui du lieu len server
from urllib import request, parse
from time import sleep
import json
from seeed_dht import DHT
def make_params(humi, temp,i):
    data = {
    "id": i,
    "data1": humi,
    "data2": temp
    }
    params = json.dumps(data).encode()
    return params
def api_post(params):
    req = request.Request('http://192.168.1.65:8000/update_post',method="POST")
    req.add_header("Content-Type","application/json")
    req.add_header("accept", "application/json")
    r = request.urlopen(req, data= params)
    respone_data = r.read()
    return respone_data
def api_get():
    req = request.Request("http://192.168.1.65:8000/get",method="GET")
    req = request.urlopen(req)
    response_data = req.read().decode()
    response_data = json.loads(response_data)
    return response_data
i = 0
while True:
    sensor = DHT('11',5)
    humi,temp = sensor.read()
    i = i+1
    params = make_params(humi, temp, i)
    print(params)
    print(api_post(params))
    print("ĐỌC ĐÂY")
    print(api_get())
    sleep(20)