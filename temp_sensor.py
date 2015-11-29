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

def read_temp():
  index = 0
  timestamp = datetime.now().strftime("%y-%m-%d-%H:%M:%S")
  message = {timestamp: []}

  for file in devices_files:
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
      now = int(time.time())
      data = {'device': index, 'temp_c': temp_c, 'temp_f': temp_f, 'time': now}
      message[timestamp].append(data)
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
