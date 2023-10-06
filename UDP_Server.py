import socket
import ast
import paho.mqtt.client as mqtt
from time import sleep

localIP = "0.0.0.0"
localPort = 11000
bufferSize = 1024

UDP_Server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_Server.bind((localIP, localPort))
print("UDP server up and listening")

client = mqtt.Client("BiYcOjAbJxA3CjoqJigYNAw")
client.username_pw_set(username="BiYcOjAbJxA3CjoqJigYNAw", password="uVUQyoEkj/bspEgE3lFBJDBb")


def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict

def thingspeak_mqtt(data1, data2):
    client.connect("mqtt3.thingspeak.com", 1883, 60)
    channel_ID = "2289496"
    client.publish("channels/%s/publish" %(channel_ID),"field1=%s&field2=%s&status=MQTTPUBLISH" %(data1,data2))

def checksum(start, id, cmd, length, datasets, stop):
    checksum = 0
    checksum +=(start+id+cmd+length+sum(data for data in datasets)+stop)
    return (2*checksum)+6

def framePacking(start, id, cmd, data, stop):
    data_dict = {
        "Start": start,
        "ID": id,
        "CMD": cmd,
        "Length": len(data),
        "Data": data,
        "CRC": checksum(start, id, cmd, len(data), data, stop),
        "Stop": stop
    }
    return data_dict

def checkCRC(crc1, crc2):
    if crc1 == crc2:
        return True
    else:
        return False


humi = 0
temp = 0
i = -1
led = -1
led_status = 1

while True:
    i+=1
    led+=1
    if(led < 2):
        led_status = 1
    else:
        led_status = 0
    if(led == 4):
        led = -1

    msgToClient = str(framePacking(0x01, 0x00, 0x01, [led_status], 0x00))
    bytesToSend = str.encode(msgToClient)
    ClientMsg = UDP_Server.recvfrom(bufferSize)

    ClientMsg_message = ClientMsg[0]
    ClientMsg_address = ClientMsg[1]
    data_dict = processReceived(ClientMsg_message)
    message = "Mesage from Client: {}".format(data_dict)

    crc2 = checksum(data_dict['Start'], data_dict['ID'], data_dict['CMD'], len(data_dict['Data']),data_dict['Data'], data_dict['Stop'])

    if(checkCRC(data_dict['CRC'],crc2)):
        address = "Client IP + Port: {}".format(ClientMsg_address)
        humi+=data_dict['Data'][0]
        temp+=data_dict['Data'][1]
        if i == 14:
            data2 = humi/15
            data1 = temp/15
            thingspeak_mqtt(data1, data2)
            humi = 0
            temp = 0
            i = -1
        print(data_dict)
        print(address)
        UDP_Server.sendto(bytesToSend, ClientMsg_address)
        print("-------------------------------------------------------------------")
    sleep(1)