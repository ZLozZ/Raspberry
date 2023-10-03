import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

sensor = GroveUltrasonicRanger(5)

while True:
    distance = sensor.get_distance()
    print('{} cm'.format(distance))

    time.sleep(1)
