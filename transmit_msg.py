import pymongo
import json

from pymongo import MongoClient
rooms = {'room1': '28-0000072f378f', 
         'room2': '28-000006c9fdf1', 
         "room3": "28-0000072e65a3", 
         "room4": "28-000006cade26", 
         "room5": "28-0000072f0f6b"}
MONGO_URL = 'mongodb://jakim:12345@ds059654.mongolab.com:59654/mongojr'

def send(messages):

  client = MongoClient(MONGO_URL)
  db = client['mongojr']
  rooms_collection = db.rooms_data
  
  for m in messages:
    sensor_id = m.get('sensor_id')
    room_name = get_room_by_sensor(sensor_id)
    data      = m.get('data')[0]
    
    if not room_exists(room_name, rooms_collection):
      record_room_id = add_new_room(room_name, sensor_id, rooms_collection)
    
    record_id = append_temperature_to_room(room_name, data, rooms_collection)
    
  client.close()
  return record_id

def get_room_by_sensor(sensor_id):
  for room, sensor in rooms.items():
    if sensor == sensor_id:
      return room
    
  return ''  

def room_exists(room, collection):
  coursor = collection.find({'name': room})
  return coursor.count() > 0

def append_temperature_to_room(room, data, collection):
  collection.update({'name': room}, {'$addToSet': {'statistics.temperature.data': data}})
    
def add_new_room(room_name, sensor_id, collection):
  room_schema = {'name': room_name, 'statistics': {'temperature': {'sensor_id': sensor_id, 'data':[]}}}  
  collection.insert(room_schema)
