import uvicorn
from typing import Optional
import paho.mqtt.client as mqtt
from urllib import request, parse
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import json
from fastapi import Form

app = FastAPI()

myclient = pymongo.MongoClient("mongodb+srv://Loo:24@loo.isuovt2.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["DataBase"]#tao database
mycol = mydb["LooData"]#tao colection moi tao cot có tên customer

def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from Broker")

client = mqtt.Client("Loo_fast")
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.username_pw_set(username="Loo3", password="242002")
client.connect("192.168.1.26", 1883, 60)


class Item(BaseModel):
    id: Optional[int]
    time: Optional[str]
    temp: Optional[float]
    humi: Optional[float]
    relay: Optional[float]
    space: Optional[float]
    moi: Optional[float]
    light: Optional[float]
    lcd: Optional[str]
    ledstick: Optional[float]
    led1: Optional[float]
    led2: Optional[float]

def mqttJson(data:dict):
    dictData = {
        "id": data["id"],
        "time": data["time"],
        "temp": data["temp"],
        "humi": data["humi"],
        "relay": data["relay"],
        "space": data["space"],
        "moi": data["moi"],
        "light": data["light"],
        "lcd": data["lcd"],
        "ledstick": data["ledstick"],
        "led1": data["led1"],
        "led2": data["led2"]
    }
    jsonData = json.dumps(dictData)
    client.publish("Loo/publish", jsonData)

@app.post("/update_post")
async def update_data_post(item: Item):
    myDict = {
        "id": item.id,
        "time": item.time,
        "temp": item.temp,
        "humi": item.humi,
        "relay": item.relay,
        "space": item.space,
        "moi": item.moi,
        "light": item.light,
        "lcd": item.lcd,
        "ledstick": item.ledstick,
        "led1": item.led1,
        "led2": item.led2
    }
    print("update_post: {}".format(myDict))
    mycol.insert_one(myDict)
    return {"ok"}

@app.get("/getdata")
async def get_data():
    x = mycol.find().sort("_id", -1).limit(1)[0]
    print("get: {}".format(x))
    data_return  = {
        "id": x["id"],
        "time": x["time"],
        "temp": x["temp"],
        "humi": x["humi"],
        "relay": x["relay"],
        "space": x["space"],
        "moi": x["moi"],
        "light": x["light"],
        "lcd": x["lcd"],
        "ledstick": x["ledstick"],
        "led1": x["led1"],
        "led2": x["led2"]
    }
    return data_return


@app.post("/updateUrl")
async def update_data(item: Item):
    dictData = {
        "id": item.id, 
        "time": item.time, 
        "temp": item.temp, 
        "humi": item.humi,
        "relay": item.relay,
        "moi": item.moi,
        "light": item.light,
        "space": item.space,
        "lcd": item.lcd,
        "ledstick": item.ledstick,
        "led1": item.led1,
        "led2": item.led2
    }
    mycol.insert_one(dictData)
    mqttJson(dictData)
    return {"ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)