import socket
from time import sleep
from seeed_dht import DHT
from gpiozero import LED
import ast

led = LED(22)
sensor = DHT("11", 5)
ServerAddressPort = ("192.168.1.77", 11000)
bufferSize = 1024


def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    data_dict = ast.literal_eval(input_string)
    return data_dict


def checksum(start, id, cmd, length, datasets, stop):
    checksum = 0
    checksum += (start + id + cmd + length + sum(data for data in datasets) + stop)
    return (checksum * 2) + 6


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


list_humi = []
list_temp = []
i = -1
b = 0
while True:
    i += 1
    humi, temp = sensor.read()
    print("nhiet do: ", temp)
    print("do am: ", humi)

    msgToServer = str(framePacking(0x01, 0x01, 0x01, [humi, temp], 0x00))
    bytesToSend = str.encode(msgToServer)

    UDP_Client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_Client.sendto(bytesToSend, ServerAddressPort)

    ServerMsg = UDP_Client.recvfrom(bufferSize)
    ServerMsg_message = ServerMsg[0]
    ServerMsg_address = ServerMsg[1]

    message = "Message from Server: {}".format(ServerMsg_message)
    address = "Message from Server: {}".format(ServerMsg_address)

    a = ServerMsg_message
    data = processReceived(a)

    crc2 = checksum(data['Start'], data['ID'], data['CMD'], len(data['Data']), data['Data'], data['Stop'])
    print("crc2", crc2)
    if (checkCRC(data['CRC'], crc2)):
        print(data)
        b = data['Data'][0]
        if b == 1:
            led.on()
        else:
            led.off()

    print(message)
    print(address)
    print(i)
    print("_________________________________________________")
    sleep(1)
