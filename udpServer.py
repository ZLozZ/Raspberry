import socket
import ast
import paho.mqtt.client as mqtt
import json
import datetime
import Adafruit_DHT
from gpiozero import LED

#Init sensors
sensor = Adafruit_DHT.DHT11
gpio = 5
relay = LED(16)

# Init broker
localIP = "0.0.0.0"
localPort = 9000
bufferSize = 1024

# Init UDP
udpServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udpServer.bind((localIP, localPort))
print("UDP server up and listening")

# Init mqtt
client = mqtt.Client("LooUp")
client.username_pw_set(username="Loo3", password="242002")
client.connect("192.168.1.86", 1883, 60)

# Init color text
txtReset = "\033[0m"
txtRed = "\033[31m"
txtGreen = "\033[32m"

# Init data
currentTimeFirst = datetime.datetime.now()
formattedTimeFirst = currentTimeFirst.strftime('%Y-%m-%d %H:%M:%S')

#Init sensor
dataRasp2 = {
    "id": 0,
    "moi": 0,
    "light": 0,
    "space": 0,
    "lcd": 0,
    "ledstick": 0,
    "led1": 0,
    "led2": 0
}

dataRasp1 = {
    "time": formattedTimeFirst,
    "humi": 0,
    "temp": 0,
    "relay": 0
}

dataUpdate={
    "lcd": 0,
    "ledstick": 0,
    "led1": 0,
    "led2": 0
}

# Init function
def mergedData(data1, data2):
    merged_dict = {**data1, **data2}
    return merged_dict

def processReceived(dataReceived):
    global dataRasp2
    global dataRasp1
    input_string = dataReceived.decode("utf-8")
    dataDict = ast.literal_eval(input_string)
    dataRasp2["id"] = dataDict["id"]
    dataRasp2["moi"] = dataDict["moi"]
    dataRasp2["light"] = dataDict["light"]
    dataRasp2["space"] = dataDict["space"]
    mergedRasp = mergedData(dataRasp1, dataRasp2)
    return mergedRasp

def sendJsonData(data: dict):
    jsonData = json.dumps(data)
    client.publish("Loo/publish", jsonData)
    
def sendJsonData(data: dict):
    jsonData = json.dumps(data)
    client.publish("Loo/publish", jsonData)

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

def on_message(client, userdata, message):
    global dataUpdate
    global dataRasp2
    if message.topic == "Loo/subscribed/lcd":
        if message.payload.decode() != 'null':
            dataUpdate["lcd"] = message.payload.decode()
            dataRasp2["lcd"] = message.payload.decode()
            print("LCD: {}".format(dataUpdate["lcd"]))
    if message.topic == "Loo/subscribed/ledstick":
        if message.payload.decode() != 'null':
            dataUpdate["ledstick"] = int(message.payload.decode())
            dataRasp2["ledstick"] = int(message.payload.decode())
            print("Led Stick: {}".format(dataUpdate["ledstick"]))
    if message.topic == "Loo/subscribed/led1":
        if message.payload.decode() != 'null':
            dataUpdate["led1"] = int(message.payload.decode())
            dataRasp2["led1"] = int(message.payload.decode())
            print("Led1: {}".format(dataUpdate["led1"]))
    if message.topic == "Loo/subscribed/led2":
        if message.payload.decode() != 'null':
            dataUpdate["led2"] = int(message.payload.decode())
            dataRasp2["led2"] = int(message.payload.decode())
            print("Led 2: {}".format(dataUpdate["led2"]))
    if message.topic == "Loo/subscribed/relay":
        if message.payload.decode() != 'null':
            dataRasp1["relay"] = int(message.payload.decode())
            print("relay: {}".format(dataRasp1["relay"]))

def relayFun():
    global dataRasp1
    
    if dataRasp1["relay"] == 1:
        relay.on()
    elif dataRasp1["relay"] == 0:
        relay.off()
        

client.subscribe("Loo/subscribed/relay")
client.subscribe("Loo/subscribed/lcd")
client.subscribe("Loo/subscribed/ledstick")
client.subscribe("Loo/subscribed/led1")
client.subscribe("Loo/subscribed/led2")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.loop_start()

while True:
    try:
        udpServer.settimeout(1)
        humi, temp = Adafruit_DHT.read_retry(sensor, gpio)
        dataRasp1["temp"] = temp
        dataRasp1["humi"] = humi
        relayFun()
        print(txtGreen + "Tác vụ nhận từ Slave" + txtReset)
        currentTime = datetime.datetime.now()
        formattedTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')
        dataRasp2["time"] = formattedTime
        msgToClient = str("ok")
        bytesToSend = str.encode(msgToClient)
        ClientMsg = udpServer.recvfrom(bufferSize)
        ClientMsg_message = ClientMsg[0]
        clientMsgAddress = ClientMsg[1]

        dataRev = processReceived(ClientMsg_message)
                    
        message = "Mesage from Client: {}".format(dataRev)
        address = "Client IP + Port: {}".format(clientMsgAddress)
        print(address)
        print(message)

        sendJsonData(dataRev)
        
        udpServer.sendto(bytesToSend, clientMsgAddress)
        print(dataUpdate)
        print("-------------------------------------------------------------------")

        print(txtGreen + "Tác vụ gửi đến slave"+txtReset)
        msgToServer = str(dataUpdate)
        bytesTServer = str.encode(msgToServer)
        
        udpServer.sendto(bytesTServer, clientMsgAddress)
        serverMsg = udpServer.recvfrom(bufferSize)
        serverMsgMessage = serverMsg[0]
        serverMsgAddress = serverMsg[1]

        message = "Message from Client: {}".format(serverMsgMessage)
        address = "Addresss from Client: {}".format(serverMsgAddress)

        print(message)
        print(address)
        print("-------------------------------------------------------------------")
    except:
        print("Not Slave")