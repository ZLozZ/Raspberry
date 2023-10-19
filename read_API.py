import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import datetime
app = FastAPI()
myclient = pymongo.MongoClient("mongodb+srv://Loo:24@cluster0.bu8vihs.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]#tao database
mycol = mydb["Sensor Data"]#tao colection moi tao cot có tên customer
class Item(BaseModel):
    id: int
    data1: float
    data2: float
@app.get("/update")
async def update_data(id: int, dev: str, time: str, humi: float, temp: float):
    dict = {
    "id": id,
    "device_name": dev,
    "time": str(time),
    "humi": humi,
    "temp": temp,
    }
    mycol.insert_one(dict)
    return dict
@app.get("/get")
async def get_data():
    data = mycol.find().sort("_id", -1).limit(1)
    dict = {
    "id": data[0]['id'],
    "device_name": data[0]['device_name'],
    "time": data[0]['time'],
    "humi": data[0]['humi'],
    "temp": data[0]['temp']
    }
    return dict
@app.post("/update_post")
async def update_data_post(item: Item):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    dict = {
    "id": item.id,
    "device_name": 'Loo',
    "time": formatted_time,
    "humi": item.data1,
    "temp": item.data2
    }
    mycol.insert_one(dict)
    return {"ok"}
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)