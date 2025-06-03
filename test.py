import os 
import json


list_room = [
  { "room": "A101" },
  { "room": "B202" },
  { "room": "C303" },
  { "room": "C303" },
  { "room": "C303" },
  { "room": "A101" },
  { "room": "A101" }
]

dict_room = {}

for item in list_room:
    if item["room"] not in dict_room:
        dict_room[item["room"]] = 1
    else:
        dict_room[item["room"]] += 1

print(dict_room)
