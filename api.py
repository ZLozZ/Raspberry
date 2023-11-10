import uvicorn
from typing import Optional
import paho.mqtt.client as mqtt
from urllib import parse
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import json
from fastapi import Form

app = FastAPI()

myclient = pymongo.MongoClient("mongodb+srv://Loo:24@loo.isuovt2.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["DataBase"]#tao database
mycol = mydb["LooData"]#tao colection moi

def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from Broker")

client = mqtt.Client("Loo_03")
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.username_pw_set(username="Loo3", password="1")
client.connect("192.168.1.3", 1883, 60)


class Item(BaseModel):
    id: Optional[int]
    time: Optional[str]
    name: Optional[str]
    data1: Optional[float]
    data2: Optional[float]
    data3: Optional[float]
    data4: Optional[float]

def MQTTJson(data:dict):
    dict = {
        "id": data["id"],
        "time": data["time"],
        "name": data["name"],
        "data1": data["data1"],
        "data2": data["data2"],
        "data3": data["data3"],
        "data4": data["data4"]
    }
    json_data = json.dumps(dict)
    print(json_data)
    client.publish("Loo/subscribed/json/data1", data["data1"])
    client.publish("Loo/subscribed/json/data2", data["data2"])
    client.publish("Loo/subscribed/json/data3", data["data3"])
    client.publish("Loo/subscribed/json/data4", data["data4"])
    client.publish("Loo/subscribed/json", json_data)

def MQTTUrl(data:dict):
    dict = {
        "id": data["id"],
        "time": data["time"],
        "name": data["name"],
        "data1": data["data1"],
        "data2": data["data2"],
        "data3": data["data3"],
        "data4": data["data4"]
    }
    url_data = parse.urlencode(dict)
    print(url_data)
    client.publish("Loo/subscribed/url", url_data)
    client.publish("Loo/subscribed/url/data1", data["data1"])
    client.publish("Loo/subscribed/url/data2", data["data2"])
    client.publish("Loo/subscribed/url/data3", data["data3"])
    client.publish("Loo/subscribed/url/data4", data["data4"])

@app.post("/update_post")
async def update_data_post(item: Item):
    mydict = {
        "id": item.id,
        "time": item.time,
        "name": item.name,
        "data1": item.data1,
        "data2": item.data2,
        "data3": item.data3,
        "data4": item.data4,
    }
    print("update_post: {}".format(mydict))
    mycol.insert_one(mydict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"]}
    MQTTUrl(data_return)
    return {"ok"}


@app.post("/update/data1")
async def update_data(id: Optional[int] = Form(...), time: Optional[str] = Form(...), name: Optional[str] = Form(...),data1: Optional[float]= Form(...)):
    dict = {
        "id": id,
        "time": time,
        "name": name,
        "data1": data1,
        "data2": None,
        "data3": None,
        "data4": None
    }
    mycol.insert_one(dict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"],
    }
    MQTTJson(data_return)
    MQTTUrl(data_return)
    return {"ok"}

@app.post("/update/data2")
async def update_data(id: Optional[int] = Form(...), time: Optional[str] = Form(...), name: Optional[str] = Form(...),data2: Optional[float]= Form(...)):
    dict = {
        "id": id,
        "time": time,
        "name": name,
        "data1": None,
        "data2": data2,
        "data3": None,
        "data4": None
    }
    mycol.insert_one(dict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"],
    }
    MQTTJson(data_return)
    MQTTUrl(data_return)
    return {"ok"}

@app.post("/update/data3")
async def update_data(id: Optional[int] = Form(...), time: Optional[str] = Form(...), name: Optional[str] = Form(...),data3: Optional[float] = Form(...)):
    dict = {
        "id": id,
        "time": time,
        "name": name,
        "data1": None,
        "data2": None,
        "data3": data3,
        "data4": None
    }
    mycol.insert_one(dict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"],
    }
    MQTTJson(data_return)
    MQTTUrl(data_return)
    return {"ok"}

@app.post("/update/data4")
async def update_data(id: Optional[int] = Form(...), time: Optional[str] = Form(...), name: Optional[str] = Form(...),data4: float= Form(...)):
    dict = {
        "id": id,
        "time": time,
        "name": name,
        "data1": None,
        "data2": None,
        "data3": None,
        "data4": data4
    }
    mycol.insert_one(dict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"],
    }
    MQTTJson(data_return)
    MQTTUrl(data_return)
    return {"ok"}

@app.post("/update")
async def update_data(id: int = Form(...), time: str = Form(...), name: str = Form(...),data1: float= Form(...),
                       data2: float= Form(...), data3: float= Form(...), data4: float= Form(...)):
    dict = {
        "id": id,
        "time": time,
        "name": name,
        "data1": data1,
        "data2": data2,
        "data3": data3,
        "data4": data4
    }
    mycol.insert_one(dict)
    x = mycol.find().sort("_id", -1).limit(1)
    print("get: {}".format(x))
    data_return  = {
        "id": x[0]["id"],
        "time": x[0]["time"],
        "name": x[0]["name"],
        "data1": x[0]["data1"],
        "data2": x[0]["data2"],
        "data3": x[0]["data3"],
        "data4": x[0]["data4"],
    }
    MQTTJson(data_return)
    MQTTUrl(data_return)
    return {"ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)