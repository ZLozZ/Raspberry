from gpiozero import LED
from time import sleep

l1 = LED(22)
while True:
    l1.on()
    sleep(1)
    l1.off()
    sleep(1)
