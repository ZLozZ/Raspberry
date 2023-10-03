import time
from grove.grove_servo import GroveServo

servo = GroveServo(12)
while True:
    servo.setAngle(0)
    time.sleep(1)
    servo.setAngle(180)
    time.sleep(1)
