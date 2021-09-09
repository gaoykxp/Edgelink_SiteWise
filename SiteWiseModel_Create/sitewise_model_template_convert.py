import logging
import platform
import sys
import json
import time
import csv

with open('PLC_Demo_model_template.json', 'r') as f:
    SWModeldata = json.load(f)

# read the csv file and load into json format
with open('PLC_Tags_Information_output.csv','r', encoding='UTF-8')  as incsvFile:
    csvReader = csv.reader(incsvFile, delimiter=',')
    lineCount = 0
    for row in csvReader:
        if lineCount == 0:
            lineCount += 1
        else:
            raw_value = {}
            if row[3] == 1:
                raw_value['dataType'] = 'BOOLEAN'
            elif row[3] == 0:
                raw_value['dataType'] = 'DOUBLE'

            raw_measument = {}
            raw_measument['measurement'] = {}
            raw_value['type'] = raw_measument
            raw_value['name'] = row[0]
            print(str(raw_value['name']))
    
            SWModeldata['assetModelProperties'].append(raw_value)
            lineCount += 1
    
print(json.dumps(SWModeldata))
with open('PLC_Demo_model_template.json', 'w') as outfile:
    json.dump(SWModeldata, outfile, indent=4)