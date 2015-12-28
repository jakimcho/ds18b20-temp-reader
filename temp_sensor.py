#! /usr/bin/env python

import os
import glob
import time
import re
import datetime
import transmit_msg

from datetime import datetime
  
base_dir = '/sys/bus/w1/devices/'

devices_folders = glob.glob(base_dir + '28*')

def list_all_files():
  files = []
  for device_folder in devices_folders:
    files.append(device_folder + '/w1_slave')
  return files

devices_files = list_all_files()

def read_temp_raw(file):
  f = open(file, 'r')
  lines = f.readlines()
  f.close()
  return lines
  
def get_sensor_id(sensor_file_name):
  try:
    sensor_id = re.search('devices/(.+?)/w1_slave', sensor_file_name).group(1)
  except AttributeError:
    sensor_id = ''
    
  return sensor_id

def read_temp():
  index = 0
  timestamp = datetime.now().strftime("%y-%m-%d-%H:%M:%S")
  messages = [];

  for file in devices_files:
    sensor_id = get_sensor_id(file)  
    lines = read_temp_raw(file)
    index += 1
    
    while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = read_temp_raw(file)
  
    equals_pos = lines[1].find('t=')
  
    if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      
      temp_c = float(temp_string) / 1000.0
      temp_f = temp_c * 9.0 / 5.0 + 32.0
      data = {'sensor_id': sensor_id, 'data': [{'temp_c': temp_c, 'temp_f': temp_f, 'time': timestamp}]}
      messages.append(data)
  return messages

messages = read_temp()
print(messages)
res = transmit_msg.send(messages)
print ("message sent to mongo" + str(res))
