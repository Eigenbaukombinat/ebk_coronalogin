#!/bin/env python3

import os
import csv
import json


logouts_map = {}

print("Reading logouts ...")

with open('../logouts.txt') as logouts:
    logouts_data = logouts.readlines()
    for line in logouts_data:
        if '_' not in line:
            continue
        code, timestamp = line.split('_')
        logouts_map[code] = timestamp

all_data = []

print("Decrypting data ...")

os.system('for x in * ; do gpg -q --decrypt $x ; echo ";$x" ; done > ../daydata.txt')
with open('../daydata.txt', 'r') as daydata:
    for rawline in daydata.readlines():
        line, code = rawline.split(';')
        code = code.strip()
        if not line.strip():
            continue
        data = json.loads(line)
        data['login'] = data['timestamp']
        del data['timestamp']
        if code in logouts_map:
            data['logout'] = logouts_map[code].strip()
        else:
            data['logout'] = 'no logout'
        all_data.append(data)

os.unlink('../daydata.txt')


print("Writing csv to ../daydata.csv ...")

with open('../daydata.csv', 'w', newline='') as csvfile:
    fieldnames = all_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for item in all_data:
        writer.writerow(item)

print('Done. Now import ../daydata.csv in your spreadsheet and press enter when done to delete it ...')
input()
os.unlink('../daydata.csv')

