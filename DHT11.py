import time

from seeed_dht import DHT

sensor = DHT('11', 5)

while True:
    humi, temp = sensor.read()
    print('Nhiet do {}C, Do am {}%'.format(temp, humi))
    time.sleep(1)
