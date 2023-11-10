import socket
from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.display.jhd1802 import JHD1802
from rpi_ws281x import PixelStrip, Color
from gpiozero import LED
import ast

sen1 = GroveMoistureSensor(0)
sen2 = GroveUltrasonicRanger(22)
sen3 = GroveLightSensor(2)
lcd = JHD1802()
led1 = LED(5)
led2 = LED(16)

# Init UDP Server
ServerAddressPort = ("192.168.1.63", 8000)
bufferSize = 1024
udpClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Init color text
txtReset = "\033[0m"
txtRed = "\033[31m"
txtGreen = "\033[32m"

#Init data
dataRasp2 = {
    "lcd": "",
    "ledstick": 0,
    "led1": 0,
    "led2": 0
}

dataSend = {
    "moi": 0,
    "light": 0,
    "space": 0
}

# Init function
def processReceived(dataReceived):
    input_string = dataReceived.decode("utf-8")
    dataDict = ast.literal_eval(input_string)
    global dataRasp2
    dataRasp2["lcd"] = dataDict["lcd"]
    dataRasp2["ledstick"] = dataDict["ledstick"]
    dataRasp2["led1"] = dataDict["led1"]
    dataRasp2["led2"] = dataDict["led2"]
    return dataRasp2

def framePacking(data: dict):
    data_dict = {
        "id": dataid,
        "moi": moi,
        "space": space,
        "light": light
    }
    return data_dict



#Xu ly RGB Ledstick
def ledstick(leds):
    LED_COUNT = 10        
    LED_PIN = 18          
    LED_FREQ_HZ = 800000  
    LED_DMA = 10         
    LED_BRIGHTNESS = 255  
    LED_INVERT = False    
    LED_CHANNEL = 0       

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    R = 255 - leds
    G = leds%2
    B = 0 + leds

    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(R, G, B))
        strip.show()

def excute():
    global dataRasp2
    lcd_str = str(dataRasp2["lcd"])
    leds = int(dataRasp2["ledstick"])
    l1 = int(dataRasp2["led1"])
    l2 = int(dataRasp2["led2"])

    lcd.clear()
    lcd.write(lcd_str)

    ledstick(leds)
    print("LCD: {}".format(lcd_str))
    print("leds: {}".format(leds))

    if l1 == 0:
        print("LED 1: OFF")
        led1.off()
    elif l1 == 1:
        print("LED 1: ON")
        led1.on()
    
    if l2 == 0:
        led2.off()
        print("LED 2: OFF")
    elif l2 == 1:
        led2.on()
        print("LED 2: ON")

dataid = 0

while True:
    dataid += 1
    moi = sen1.moisture
    space = round(sen2.get_distance(), 2)
    light = sen3.light
    try:
        print(txtGreen + "Tac vu gui du lieu UDP" + txtReset)
        dataSend["id"] = dataid
        dataSend["moi"] = moi
        dataSend["space"] = space
        dataSend["light"] = light
        
        dataDevice = str(dataSend)
        bytesToSend = str.encode(dataDevice)

        udpClient.sendto(bytesToSend, ServerAddressPort)

        serverMsg = udpClient.recvfrom(bufferSize)
        serverMsgMessage = serverMsg[0]
        serverMsgAddress = serverMsg[1]

        message = "Message from Server: {}".format(serverMsgMessage)
        address = "addresss from Server: {}".format(serverMsgAddress)

        print(message)
        print(address)
        print("ID: ", dataid)
        print("-------------------------------------------------------------------")
        
        print(txtGreen + "Tac vu nhan du lieu UDP" + txtReset)
        msgToClient = str("OK")
        bytesToSend = str.encode(msgToClient)

        serverMsg = udpClient.recvfrom(bufferSize)
        serverMsgMessage = serverMsg[0]
        serverMsgAddress = serverMsg[1]

        processReceived(serverMsgMessage)
        message = "Message from Server: {}".format(dataRasp2)
        address = "addresss from Server: {}".format(serverMsgAddress)

        udpClient.sendto(bytesToSend, ServerAddressPort)

        print(message)
        print(address)
        print("-------------------------------------------------------------------")
        excute()
    except:
        print("Connecting Server....")