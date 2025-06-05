from json import load
import os
import json
file_path = "data/transaction.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
print(data)