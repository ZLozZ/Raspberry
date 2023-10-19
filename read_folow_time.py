import uvicorn  # chạy ứng dụng Fast API
from fastapi import FastAPI, HTTPException, Header,Query # framework web được sử dụng để tạo API
from pydantic import BaseModel # để định nghĩa các mô hình dữ liệu dựa trên Python, cho phép kiểm tra và xác minh dữ liệu đầu vào
import pymongo # cho phép tương tác với cơ sở dữ liệu MongoDB
import datetime # sử các chức năng liên quan tới thời gian

#API_KEY = "nhom_2"  # API key phải trùng với mã Server của bạn.
#key_read = "doc"
app = FastAPI() # tạo một phiên bản của ứng dụng FastAPI
#API_key = "nhom2"
myclient = pymongo.MongoClient("mongodb+srv://thuan:01032002@thuan.15fpr5f.mongodb.net/?retryWrites=true&w=majority")
#  kết nối đên csdl mongo vs username pass
mydb = myclient["mydatabase"] # tạo một thể hiện của cơ sở dữ liệu có tên "mydatabase"
mycol = mydb["Sensor Data"] # tạo bảng dữ liệu tên ... để lưu trữ dữ liệu

class Item(BaseModel): #một mô hình Pydantic có tên Item được định nghĩa.
    id: float         # # Nó biểu thị cấu trúc của dữ liệu mà bạn mong đợi trong yêu cầu POST.
    data1: float
    data2: float
    data3: str
    data4: str

@app.post("/update_post")
async def update_data_post(item: Item , API_key: str):
    if(API_key == "nhom2"):
        current_time = datetime.datetime.now() # lấy thời gian hiện tại
        # Định dạng thời gian chỉ lấy đến giây
        now_time = current_time.strftime('%Y-%m-%d %H:%M:%S') # Định dạng thời gian chỉ lấy đến giây
        mydict = {   # tạo 1 dictionary lưu dữ liệu và dữ liệu này sẽ được gửi lên csdl
            "id": item.id,
            "time": now_time,
            "device_name": "iot_nhom2",
            "humi": item.data1,
            "temp": item.data2,
            "led1": item.data3,
            "led2": item.data4
        }
        mycol.insert_one(mydict) # chèn dictionary và trong cơ sở dữ liệu
        return {"gui thanh cong"}
    else:
        return {"error API_key"}

@app.get("/get", response_model=list[Item]) # định nghĩa endpoint cho yêu cầu GET tại URL "/get". Endpoint này trả về dữ liệu
async def get_data(key_read: str, N: int = Query(3, description="3")): # định nghĩa hàm get_data

    if key_read == "doc":
        x = mycol.find().sort("time", -1).limit(N)
        result = []
        for record in x:
            result.append({
                "id": record['id'],
                "device_name": record['device_name'],
                "time": record['time'],
                "data1": record['humi'],
                "data2": record['temp'],
                "data3": record['led1'],
                "data4": record['led2']
            })
        return result
    else:
        raise HTTPException(status_code=400, detail="Invalid key_read")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # chạy ứng dụng FastAPI