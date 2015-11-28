import pymongo
import json

from pymongo import MongoClient

def send(message):
#  print("Sending Messages" + json.dumps(message))

  client = MongoClient('mongodb://jakim:12345@ds059654.mongolab.com:59654/mongojr')

  db = client['mongojr']
  temperature = db.temperature
  record_id = temperature.insert(message)
  client.close()
#  print("DB record id" + record_id)
  return record_id


