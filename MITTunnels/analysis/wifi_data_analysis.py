import json
import matplotlib.pyplot as plt
from pylab import figure, gca, Line2D

print('start')

json_data = open('ScanResult.json')
data = json.load(json_data)

print(type(data))
locations = {}
macs = {}

for x in data['results']:
    locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})
    macs[x['MAC']] = x['MAC'] 

for x in data['results']:
    locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y']})

for x in locations:
    print(x)

distances_loc = []
distances_signal = []
#color_list = ["Black", "Green", "Red", "DimGray", "SkyBlue", "Orange", "DeepPink", "BlueViolet", "Yellow", "Green", "IndianRed",  "SpringGreen", "DarkOliveGreen", "LightSteelBlue", "Ivory", "Gray", "MistyRose", "Goldenrod", "Orchid"]
colors = []
color_count = 0 

closest_list = []
for a, i in locations.items():
    color_count += 1
    closest = a
    closest_dist = 10**10
    colsest_loc_dsit = 10**10
    for b, j in locations.items():
        if i != j:
            loc_dist = ((float(i[0]['x']) - float(j[0]['x']))**2 + (float(i[0]['y']) - float(j[0]['y']))**2)**.5
            dist_sum = 0
            for k in i:
               ##print(k)
                current_dist = float(k['LEVEL'])
                for l in j:
                    if k['MAC'] == l['MAC']:
                        current_dist -=  float(l['LEVEL'])
                dist_sum += current_dist**2
            for k in j:
               ##print(k)
                current_dist = float(k['LEVEL'])
                for l in i:
                    if k['MAC'] == l['MAC']:
                        current_dist = 0
                dist_sum += current_dist**2

            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
            if dist_sum < closest_dist:
		closest = j
		closest_dist = dist_sum
		closest_loc_dist = loc_dist
#	    colors.append(color_list[color_count-1])
    closest_list.append([[i[0]['x'], i[0]['y']],[closest[0]['x'], closest[0]['y']], closest_dist, closest_loc_dist])
print(closest_list)

#plt.figure(1)           
#plt.subplot(111)
#plt.scatter(distances_loc, distances_signal)
#plt.title('Signal Distances Using Euclidian Metric')
#plt.ylabel('Signal Euclidian Distance')
#plt.xlabel('Physical Distance')
"""
perfect_match = []

for a, i in locations.items():
    color_count += 1
    for b, j in locations.items():
        if i != j:
            
            loc_dist = ((float(i[0]['x']) - float(j[0]['x']))**2 + (float(i[0]['y']) - float(j[0]['y']))**2)**.5
            dist_sum = 0
            for k in i:
                if k['LEVEL'] == '0':
                    current_dist = 0
                else:
                    current_dist = 1
                for l in j:
                    if k['MAC'] == l['MAC']:
                        if l['LEVEL'] == '0':
                            current_dist += 0
                        else:
                            current_dist -= 1
                dist_sum += abs(current_dist)
            for k in j:
                if k['LEVEL'] == '0':
                    current_dist = 0
                else:
                    current_dist = 1
                for l in i:
                    if k['MAC'] == l['MAC']:
                        if l['LEVEL'] == '0':
                            current_dist += 0
                        else:
                            current_dist -= 1
                dist_sum += abs(current_dist)
            if dist_sum == 0:
		perfect_match.append([a,b])
	    distances_loc.append(loc_dist)
            distances_signal.append(dist_sum)
#            colors.append(color_list[color_count-1])
#print(perfect_match)
print(len(perfect_match))
print(len(locations))
"""
#plt.scatter(distances_loc, distances_signal)
#plt.title('Signal Distances Using Bit Vector Metric')
#plt.ylabel('Signal Distance in # APs')
#plt.xlabel('Physical Distance')
#            
#first_location = 0
#for a, i in locations.items():
#    first_location = i
    
#for b, j in locations.items():
#    if i != j:
#        loc_dist = ((float(first_location[0]['x']) - float(j[0]['x']))**2 + (float(first_location[0]['y']) - float(j[0]['y']))**2)**.5
#        dist_sum = 0
#        for k in first_location:
#            if k['LEVEL'] == '0':
#                print(k['LEVEL'])
#                current_dist = 0
#            else:
#                current_dist = 1
#            for l in j:
#                if k['MAC'] == l['MAC']:
#                    current_dist -= 1
#            dist_sum += current_dist
#        distances_loc.append(loc_dist)
#        distances_signal.append(dist_sum**.5)

#print(distances)

fig, ax = plt.subplots()
for i in closest_list:
	ax.add_line(Line2D([i[0][0], i[1][0]], [i[0][1], i[1][1]]))
plt.title('pairs of closest points')
plt.ylabel('y coordinate')
plt.xlabel('x coordinate')
plt.plot()
plt.show()

#plt.scatter(distances_loc, distances_signal)
#plt.scatter([0],[0])
#plt.title('Signal Distance from One Point Using Bit Vector Metric')
#plt.ylabel('Signal Distance in # APs')
#plt.xlabel('Physical Distance')
#plt.plot()
#plt.show()


#for x in data.results:
#    print(x)

##print(data)
