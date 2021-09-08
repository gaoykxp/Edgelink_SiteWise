import sys
import os
import json
import logging
import csv
import demjson
import argparse

debugLog = True

parser = argparse.ArgumentParser(description='Convert SIMENS Node csv file to edgelink csv file.')
parser.add_argument('--inputFile', '-i', type=str, required=True, help="The csv file to be converted.")


if debugLog:
    print(parser.parse_args())

inputFile = parser.parse_args().inputFile
outputFile = inputFile.replace(".csv", "_output.csv")

if debugLog:
    print("inputFile:" + inputFile )
    print("outputFile:" + outputFile )
    
# read the csv file and covert to required format
with open(inputFile,'r', encoding='UTF-8')  as incsvFile:
    csvReader = csv.reader(incsvFile, delimiter=',')
    lineCount = 0
    nodeData = []
    for row in csvReader:
        if lineCount == 0:
            lineCount += 1
            if debugLog:
                print(f'Column names are {", ".join(row)}')
        else:
            nameStr = str(row[0])
            AddressID = ''
            startBit = 0
            LogicAddress = row[2]
            if LogicAddress[0] == '%':
                #  %Q10.0 ->QX0010   0
                dotleft = LogicAddress.split('.')[0]
  
                if LogicAddress[1] == 'I':
                    dotleft = dotleft.split('I')[1]
                else:
                    dotleft = dotleft.split('Q')[1]

                addressnumber = dotleft.zfill(3)             
                startBit = LogicAddress.split('.')[1]               
                AddressID = LogicAddress[1]+ 'X0' + addressnumber
            else:
                AddressID = LogicAddress.replace(".DBD", ",")
                startBit = 0
                
            type = 0
            if row[1] == 'Bool':
                type = 1
            elif row[1] == 'Int':
                type = 0
            if debugLog:
                print(id)
            nameStr = nameStr.replace("-", "_")
            nameStr = nameStr.replace(" ", "_")
            nameStr = nameStr.replace("/", "_")
            nameStr = nameStr.replace(".", "_")
            nameStr = nameStr.replace("&", "_")
            if debugLog:
                print("nameStr:"+ nameStr)
            
            nodeData.append({
                'Name': nameStr,
                'Address': AddressID,
                'startBit': startBit,
                'DataType': type               
            })
                    
            lineCount += 1
            
    if debugLog:
        print(nodeData) 
    with open(outputFile, 'w', newline='') as outcsvFile:    
        head = ['Name', 'Address', 'startBit','DataType']
        writer = csv.DictWriter(outcsvFile,head)
        writer.writeheader()
        writer.writerows(nodeData)

