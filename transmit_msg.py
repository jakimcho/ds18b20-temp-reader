import pymongo
import json

from pymongo import MongoClient

def send(message):
#  for temp in message:
  print("Sending Messages" + json.dumps(message))
  print("pymongo version " + pymongo.__version__)
# Old mongo connection: client = MongoClient('mongodb:// 192.168.13.104:27017/')

  client = MongoClient('mongodb://jakim:12345@ds059654.mongolab.com:59654/mongojr')
  
# old db: db = client['rachev']
  dd = client.get_default_database()
  print(dd.collection_names())

  db = client['mongojr']
  temperature = db.temperature
  record_id = temperature.insert(message)
  client.close()
#  print("DB record id" + record_id)
  return record_id


