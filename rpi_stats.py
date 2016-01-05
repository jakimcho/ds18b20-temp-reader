#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os

from datetime import datetime
from pymongo import MongoClient

MONGO_URL = 'mongodb://jakim:12345@ds059654.mongolab.com:59654/mongojr'
PI_DEVICES = {"00000000eb93b7d2": "Jakim_RPi"}

def send_stats_to_mongo():
  client = MongoClient(MONGO_URL)
  db = client['mongojr']
  rpi_stats = db.rpi_stats
  time = datetime.now().strftime("%y-%m-%d-%H:%M:%S")
  data = {'cpu_load': get_load(), 'ram': get_ram(), 'disk_space': get_disk(), 'cpu_temperature': get_temperature(), 'time': time}
  
  record_id = append_stats_to_rpi(getserial(), data, rpi_stats)
  client.close()
  
def append_stats_to_rpi(serial, data, collection):
  if (not rpi_exists(serial, collection)):
    add_new_rpi(PI_DEVICES[serial], serial, collection)
  collection.update({'rpi_serial': serial}, {'$addToSet': {'statistics': data}})  
  
def add_new_rpi(pi_name, serial, collection):
  room_schema = {'name': pi_name, 'rpi_serial': serial, 'statistics': []}
  collection.insert(room_schema) 
  
def rpi_exists(serial, collection):
  coursor = collection.find({'rpi_serial': serial})
  return coursor.count() > 0
  
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

def get_load():
  try:
    s = subprocess.check_output(["cat", "/proc/loadavg"])
    return float(s.split()[0])
  except:
    return 0

# Returns the used ram as a percentage of the total available
def get_ram():
  try:
    s = subprocess.check_output(["free", "-m"])
    lines = s.split("\n")
    used_mem = float(lines[1].split()[2])
    total_mem = float(lines[1].split()[1])
    return (int((used_mem / total_mem) * 100))
  except:
    return 0

# Returns the percentage used disk space on the /dev/root partition
def get_disk():
  try:
    s = subprocess.check_output(["df", "/"])
    lines = s.split("\n")
    return int(lines[1].split("%")[0].split()[4])
  except:
    return 0

# Returns the temperature in degrees C of the CPU
def get_temperature():
  try:
    dir_path = "/opt/vc/bin/vcgencmd"
    s = subprocess.check_output([dir_path, "measure_temp"])
    return float(s.split("=")[1][:-3])
  except:
    return 0

send_stats_to_mongo()
