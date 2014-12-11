# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 17:46:33 2014

@author: jaysonl
"""

import json
import matplotlib.pyplot as plt
from pylab import Line2D

print('start')

data_sets = []

json_data = open('tunnels-nexus5.json')
data_sets.append(json.load(json_data))

test_data_sets = []

test_json_data = open('tunnels-nexus5.json')
test_data_sets.append(json.load(test_json_data))


locations = {}
macs = {}

print('parsing started')

invalid_MAC = 0

for data in data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})
            macs[x['MAC']] = x['MAC'] 
        else:
            invalid_MAC += 1
    
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})
        else:
            invalid_MAC += 1

new_json = []
for x, i in ave_locations.items():
    new_json.append(i[0])
file_str = "{results: " + str(new_json) + "}"
fo = open("averaged_data.json", "wb")
fo.write(bytes(file_str, "utf-8"));
fo.close


print("numer of locations: ")
print(len(locations))
print("ammount of data")
print(len(data_sets[0]))
print("number of invald MACs")
print(invalid_MAC)

invalid_test_MAC = 0



test_locations = {}
test_macs = {}

for data in test_data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            test_locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})
            test_macs[x['MAC']] = x['MAC'] 
        else:
            invalid_test_MAC += 1
    
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            test_locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})
        else:
            invalid_test_MAC += 1

print("numer of locations: ")
print(len(test_locations))
print("ammount of data")
print(len(test_data_sets[0]))
print("number of invald MACs")
print(invalid_test_MAC)


ave_locations = {}
for x, i in locations.items():
    if ave_locations == {}:
        ave_locations[x] = []
        ave_locations[x].append(i[0])
    for y, j in ave_locations.copy().items():
        if x != y:
            ave_locations[x] = []
            ave_locations[x].append(i[0])
            
test_ave_locations = {}
for x, i in test_locations.items():
    if test_ave_locations == {}:
        test_ave_locations[x] = []
        test_ave_locations[x].append(i[0])
    for y, j in test_ave_locations.copy().items():
        if x != y:
            test_ave_locations[x] = []
            test_ave_locations[x].append(i[0])

total_count = 0            
for x, i in locations.items():
    for y, j in ave_locations.copy().items():
        if x == y:
            for k in j:
                for l in i:
                    if k['MAC'] == l['MAC']:
                        k['ave_count'] += 1
                        delta = l['LEVEL'] - k['LEVEL']
                        k['LEVEL'] += delta / k['ave_count']
                        k['std_dev'] += delta*(l['LEVEL'] - k['LEVEL'])
                        total_count += 1
        else:
            ave_locations[x] = []
            ave_locations[x].append(i[0])

total_count = 0            
for x, i in test_locations.items():
    for y, j in test_ave_locations.copy().items():
        if x == y:
            for k in j:
                for l in i:
                    if k['MAC'] == l['MAC']:
                        k['ave_count'] += 1
                        delta = l['LEVEL'] - k['LEVEL']
                        k['LEVEL'] += delta / k['ave_count']
                        k['std_dev'] += delta*(l['LEVEL'] - k['LEVEL'])
                        total_count += 1
        else:
            test_ave_locations[x] = []
            test_ave_locations[x].append(i[0])


print('locations computed')
print(len(ave_locations))
print(total_count)
#print(ave_locations)

parse_format_data = {"results":[ave_locations]}
with open('averaged_data.json', 'w') as outfile:
  json.dump(parse_format_data, outfile)

distances_loc = []
distances_signal = []
distances_loc_bit = []
distances_signal_bit = []
distances_loc_sigma = []
distances_signal_sigma = []

closest_list = []
closest_average_list = []
closest_bit_list = []
closest_bit_average_list = []
closest_sigma_list = []
closest_sigma_average_list = []
acount = -1

matches = 0
for a, i in test_ave_locations.items():
    print("matches = ", matches)
    closest = a
    closest_dist = 10**10
    closest_bit_dist = 10**10
    closest_sigma_dist = 10**10
    colsest_loc_dsit = 10**10
    closest_bit_loc_dist = 10**10
    closest_sigma_loc_dist = 10**10
    matches = 0
    matches_bit = 0
    acount += 1
    x_ave = 0
    y_ave = 0
    x_ave_bit = 0
    y_ave_bit = 0
    x_ave_sigma = 0
    y_ave_sigma = 0
    isMatched = False
    
    for b, j in ave_locations.items():
        if i != j:
            loc_dist = ((float(i[0]['x']) - float(j[0]['x']))**2 +
            (float(i[0]['y']) - float(j[0]['y']))**2)**.5
            dist_sum = 0
            dist_sum_bit = 0            
            dist_sum_sigma = 0
            print(i)
            print('just printed i')
            print(j)
            for k in i:
                #print(k)
                current_dist = float(k['LEVEL'])
                current_bit_dist = 1
                for l in j:
                    if k['MAC'] == l['MAC']:
                        current_dist -=  float(l['LEVEL'])
                        current_bit_dist -= 1
                        isMatched = True
                dist_sum += current_dist**2
                dist_sum_bit += current_bit_dist
            for k in j:
                current_dist = float(k['LEVEL'])
                current_bit_dist = 1
                for l in i:
                    if k['MAC'] == l['MAC']:
                        current_dist = 0
                        current_bit_dist = 0
                dist_sum += current_dist**2
                dist_sum_bit += current_bit_dist
#            for k in i:
#                current_dist = float(k['LEVEL'])
#                current_bit_dist = 1
#                for l in j:
#                    if k['MAC'] == l['MAC']:
#                        current_dist = 0
#                        current_bit_dist = 0
#                dist_sum += current_dist**2
#                dist_sum_bit += current_bit_dist
#            if dist_sum == 0:
                #print('dist_sum = 0')
            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
            if dist_sum < closest_dist:
                closest = j
                closest_dist = dist_sum
                closest_loc_dist = loc_dist
                
            distances_loc_bit.append(loc_dist)
            distances_signal_bit.append(dist_sum)
            if dist_sum_bit < closest_bit_dist:
                closest_bit = j
                closest_bit_dist = dist_sum_bit
                closest_bit_loc_dist = loc_dist
#       colors.append(color_list[color_count-1])
    if isMatched == False:
        print('no matches')
        closest_dist = -1
        closest = i
        closest_loc_dist = 0        
        closest_bit_dist = -1
        closest_bit = i
        closest_bit_loc_dist = 0
        
    closest_list.append([[i[0]['x'], i[0]['y']],[closest[0]['x'], 
                          closest[0]['y']], closest_dist, closest_loc_dist])
    closest_bit_list.append([[i[0]['x'], i[0]['y']],[closest_bit[0]['x'], 
                          closest_bit[0]['y']], closest_bit_dist, closest_bit_loc_dist])

    for b, j in ave_locations.items():
        if i != j:
            dist_sum = 0
            dist_sum_bit = 0
            for k in i:
               ##print(k)
                current_dist = float(k['LEVEL'])
                current_bit_dist = 1
                for l in j:
                    if k['MAC'] == l['MAC']:
                        current_dist -=  float(l['LEVEL'])
                        current_bit_dist -= 1
                dist_sum += current_dist**2
                dist_sum_bit += current_bit_dist
            for k in j:
               ##print(k)
                current_dist = float(k['LEVEL'])
                current_bit_dist = 1
                for l in i:
                    if k['MAC'] == l['MAC']:
                        current_dist = 0
                        current_bit_dist = 0
                dist_sum += current_dist**2
                dist_sum_bit += current_bit_dist

            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
            distances_signal_bit.append(dist_sum_bit)
            if dist_sum <= closest_list[acount][2]:
                matches += 1
                x_ave += float(j[0]['x'])
                y_ave += float(j[0]['y'])
            if dist_sum_bit <= closest_bit_list[acount][2]:
                matches_bit += 1
                x_ave_bit += float(j[0]['x'])
                y_ave_bit += float(j[0]['y'])

    if x_ave != 0 and y_ave != 0:
        closest_average_list.append([[i[0]['x'], i[0]['y']],[float(x_ave)/(matches), float(y_ave)/(matches)]])
        closest_bit_average_list.append([[i[0]['x'], i[0]['y']],[float(x_ave_bit)/(matches_bit), float(y_ave_bit)/(matches_bit)]])
    else:
        closest_average_list.append([[i[0]['x'], i[0]['y']],[i[0]['x'], i[0]['y']]])
        closest_bit_average_list.append([[i[0]['x'], i[0]['y']],[i[0]['x'], i[0]['y']]])
        
print('analysis run')
#print(closest_list)

fig, ax = plt.subplots()
xs = []
ys = []
for a, i in ave_locations.items():
    xs.append(i[0]['x'])
    ys.append(-float(i[0]['y']))
test_xs = []
test_ys = []
for a, i in test_ave_locations.items():
    test_xs.append(i[0]['x'])
    test_ys.append(-float(i[0]['y']))
plt.scatter(xs, ys, color = 'red')
plt.scatter(test_xs, test_ys, color = 'blue')
    
for i in closest_list:
    ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
plt.title('MIT Tunnles Closest Points by Euclidian Metric with Averaging')
plt.ylabel('y coordinate (map pixles)')
plt.xlabel('x coordinate (map pixles)')
plt.plot()
plt.show()
