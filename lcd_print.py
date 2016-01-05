#! /usr/bin/env python

import lcd_display
import ds18b20
import transmit_msg
import check_net
from time import sleep

lcd = lcd_display.Adafruit_CharLCD()
short_sleep = 5
long_sleep = 3600
counter = 0

try:
  while 1:
    ppp = check_net.GetPacketCount("ppp")
    if ppp:
      lcd.clear()
      lcd.message("Network " + ppp)

    messages = ds18b20.read_temp()
    
    for m in messages:
      lcd.clear()
      sensor_id = m.get('sensor_id')
      room_name = transmit_msg.get_room_by_sensor(sensor_id)
      data = m.get('data')[0]
      time = str(data['time'])
      temp_c = "%.2fC" % data['temp_c']
      
      message = "%s\n%s: %s" % (time, room_name, temp_c)
      lcd.message(message)
      sleep(short_sleep)
      
  counter += 1
  if counter == 2:
    counter = 0
    sleep(long_sleep)   
     
except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    lcd.clear()
    lcd.clean_gpio()
