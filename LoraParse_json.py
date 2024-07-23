import json
import csv

file_name = "parse.json"
extract_temp = []
extract_humid = []

with open(file_name, 'r', encoding='utf-8') as file:
    data = json.load(file)
    for i in data:
        if (len(i["payload"]["objectJSON"]) > 40):
            extract_temp.append({"time" : i["payload"]["publishedAt"][2:19], "data" : int(json.loads(i["payload"]["objectJSON"])["temperature"])/100, })
            extract_humid.append({"time" : i["payload"]["publishedAt"][2:19], "data" : int(json.loads(i["payload"]["objectJSON"])["humidity"])/100})
        else:
            extract_temp.append({"time" : i["payload"]["publishedAt"][2:19] , "data" : 0 })
            extract_humid.append({"time" : i["payload"]["publishedAt"][2:19], "data" : 0 })
extract_humid = list(reversed(extract_humid))
extract_temp = list(reversed(extract_temp))
csv_file_temp = 'output_temp.csv'
csv_file_humid = 'output_humid.csv'
with open(csv_file_temp, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'data'])
    writer.writeheader()
    for item in extract_temp:
        writer.writerow(item)
with open(csv_file_humid, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'data'])
    writer.writeheader()
    for item in extract_humid:
        writer.writerow(item)

