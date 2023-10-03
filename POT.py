#Potentiometer: POT

from time import sleep
from grove.adc import ADC

sensor = ADC()

while True:
    value = sensor.read_voltage(0)
    print("Gia tri bien tro: {}".format(value))
    sleep(1)
