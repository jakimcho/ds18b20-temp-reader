#! /usr/bin/env python

import lcd_display
import ds18b20
import transmit_msg
from time import sleep

lcd = lcd_display.Adafruit_CharLCD()
lcd.clear()

msgs = [];
messages = ds18b20.read_temp()

for m in messages:
    sensor_id = m.get('sensor_id')
    room_name = transmit_msg.get_room_by_sensor(sensor_id)
    data      = m.get('data')[0]
    time      = str(data['time'])
    temp_c    = "%.2fC" % data['temp_c']


    msgs.append("%s\n%s - %s" % (time, room_name, temp_c))
    lcd.message(msgs[0])
    print(msgs)


try:
    while 1:
        sleep(1)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    lcd.clear()
    lcd.clean_gpio()
