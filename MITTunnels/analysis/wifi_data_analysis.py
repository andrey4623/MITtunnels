import json
import matplotlib.pyplot as plt

print('start')

json_data = open('ScanResult_G5.json')
data = json.load(json_data)

print(type(data))
locations = {}

for x in data['results']:
    locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})

for x in data['results']:
    locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y']})

for x in locations:
    print(x)

distances_loc = []
distances_signal = []
color_list = ["Black", "Bisque", "Red", "DimGray", "SkyBlue", "Orange", "DeepPink", "BlueViolet", "SaddleBrown", "Yellow", "Green", "IndianRed", "Salmon", "SpringGreen", "DarkOliveGreen", "LightSteelBlue", "Ivory", "Gray", "MistyRose", "Goldenrod", "Orchid"]
colors = []
color_count = 0 

"""for a, i in locations.items():
    color_count += 1
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
            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
	    colors.append(color_list[color_count-1])
"""
 
#plt.figure(1)           
#plt.subplot(111)
#plt.scatter(distances_loc, distances_signal)
#plt.title('Signal Distances Using Euclidian Metric')
#plt.ylabel('Signal Euclidian Distance')
#plt.xlabel('Physical Distance')

            
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
                dist_sum += current_dist
            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
            colors.append(color_list[color_count-1])
#            
#
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

plt.scatter(distances_loc, distances_signal, c = colors)
plt.title('Signal Distance from One Point Using Bit Vector Metric')
plt.ylabel('Signal Distance in # APs')
plt.xlabel('Physical Distance')
plt.show()

#for x in data.results:
#    print(x)

##print(data)
