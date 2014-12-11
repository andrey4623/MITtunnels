# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 17:46:33 2014

@author: jaysonl
"""

import json

print('start')

data_sets = []

json_data = open('samsung5.json')
json_data = open('tunnels_for_tablet_before_averaged.json')
data_sets.append(json.load(json_data))

locations = {}
macs = {}

print('parsing started')

invalid_MAC = 0

for data in data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            locations[x['x'] + ", " + x['y']] = []
            macs[x['MAC']] = x['MAC'] 
        else:
            invalid_MAC += 1
    
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})
        else:
            invalid_MAC += 1


ave_locations = {}

for data in data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            ave_locations[x['x'] + ", " + x['y']] = []
            
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            seenMAC = False            
            for y, j in ave_locations.items():
                for k in j:
                    if x['x'] == k['x'] and x['y'] == k['y'] and x['MAC'] == k['MAC']:
                        seenMAC = True                    
            if seenMAC == False:
                ave_locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': 0, 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})


new_json = []
for i in ave_locations.values():
    for k in i:
        new_json.append(k)
new_json = json.dumps(new_json)
print(new_json)
file_str = "{\"results\": " + str(new_json) + "}"
fo = open("tunnels_for_tablet_before_averaged.json", "wb")
fo.write(bytes(file_str, "utf-8"));
fo.close

print('done')