import paho.mqtt.client as mqtt
from gpiozero import LED
from grove.display.jhd1802 import JHD1802

buzzer = LED(12)
led = LED(5)
relay = LED(16)
lcd = JHD1802()


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code {}".format(rc))
    channel_ID = "2262630"
    client.subscribe("channels/%s/subscribe/fields/field1" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field2" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field3" % (channel_ID))


def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")


def on_message(client, userdata, message):
    if message.topic == 'channels/2262630/subscribe/fields/field1':
        temp = message.payload.decode()[0:2]
        print("Nhiet do: {}".format(temp))
        lcd.setCursor(0, 0)
        lcd.write('Temp:{}C'.format(temp))
        if int(temp) >= 20 and int(temp) <= 30:
            print("Giu status")
        if int(temp) < 20:
            buzzer.off()
        if int(temp) > 30:
            buzzer.on()
    if message.topic == 'channels/2262630/subscribe/fields/field2':
        humi = message.payload.decode()[0:2]
        lcd.setCursor(0, 9)
        lcd.write('hum:{}%'.format(humi))
        print("Do am: {}".format(humi))
        if int(humi) >= 80 and int(humi) <= 90:
            print("giu status")
        if int(humi) > 90:
            relay.on()
        if int(humi) < 80:
            relay.off()
    if message.topic == 'channels/2262630/subscribe/fields/field3':
        rd = message.payload.decode()
        lcd.setCursor(1, 0)
        lcd.write('Random: {}'.format(str(rd) + ' '))
        print("Random: {}".format(rd))
        print('--------------------')
        if (int(rd) > 50):
            led.on()
        if (int(rd) < 50):
            led.off()


client = mqtt.Client("KAAQChoPICUBFQUKFwcLJSs")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username="KAAQChoPICUBFQUKFwcLJSs", password="mb5R6hBfa5gKT4ymUDwk6Tjp")
client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()
