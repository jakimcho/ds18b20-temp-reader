#! /usr/bin/env python

import os
import glob
import time
import datetime
import transmit_msg

from datetime import datetime
  
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  
  equals_pos = lines[1].find('t=')
  
  if equals_pos != -1:
    timestamp = int(time.time())
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    message = {'temp_c': temp_c, 'temp_f': temp_f, 'time': timestamp}
    return message

#messages = []
#batch = 0

#while True:
#  messages.append(read_temp().copy())
#  time.sleep(60)
  
#  if (batch == 10):
#    transmit_msg.send(messages)
#    messages = []
#    batch = 0
  
#  batch += 1

message = read_temp()
res = transmit_msg.send(message)
print ("message sent to mongo" + str(res))
