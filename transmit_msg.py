import pymongo
import json

from pymongo import MongoClient

def send(message):
#  for temp in message:
#    print("Sending Messages" + json.dumps(message))
  client = MongoClient('mongodb://192.168.13.104:27017/')
  db = client['rachev']
  temperature = db.temperature
  record_id = temperature.insert(message)
  client.close()
#  print("DB record id" + record_id)
  return record_id


