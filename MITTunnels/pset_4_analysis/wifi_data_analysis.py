import json
import matplotlib.pyplot as plt

json_data = open('ScanResult.json')
data = json.load(json_data)

print(type(data))
locations = {}

for x in data['results']:
##    print('!')
##    print(x['x'])
##    print(x['y'])
##    print(x['MAC'])
##    print(x['LEVEL'])
    locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})

for x in data['results']:
    locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y']})

for x in locations:
    print(x)

distances_loc = []
distances_signal = []

for a, i in locations.items():
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

print(distances)

plt.scatter(distances_loc, distances_signal)
plt.ylabel('Signal Euclidian Distance')
plt.xlabel('Physical Distance')
plt.show()

#for x in data.results:
#    print(x)

##print(data)
print("done")
