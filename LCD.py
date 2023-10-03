from grove.display.jhd1802 import JHD1802

lcd = JHD1802()

while True:
    lcd.setCursor(0, 8)
    lcd.write('NHOM 6')
    lcd.setCursor(1, 6)
    lcd.write('Bao cao 2')
