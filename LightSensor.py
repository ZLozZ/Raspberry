import time

from grove.grove_light_sensor_v1_2 import GroveLightSensor

sensor = GroveLightSensor(0)

while True:
    print('Gia tri dien ap Cam bien quang: {}'.format(sensor.light))

    time.sleep(1)
