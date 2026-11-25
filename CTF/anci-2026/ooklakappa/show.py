import json
d=json.load(open("ANCI/ooklakappa/database.json",encoding="utf-8"))
print(d["tables"]["secrets"])
print("users:",len(d["tables"]["users"]))
