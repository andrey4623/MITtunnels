import json
import matplotlib.pyplot as plt

print('start')

data_sets = []

training_data = "tunnels_together"
test_data = "tunnels_together"

json_data = open(training_data+'.json')
data_sets.append(json.load(json_data))

test_data_sets = []

test_json_data = open(test_data+'.json')
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


test_locations = {}
test_macs = {}
test_invalid_MAC = 0

for data in test_data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            test_locations[x['x'] + ", " + x['y']] = []#.append({x['MAC'] : x['LEVEL']})
            test_macs[x['MAC']] = x['MAC'] 
        else:
            test_invalid_MAC += 1
    
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            test_locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': x['LEVEL'], 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})
        else:
            test_invalid_MAC += 1


test_ave_locations = {}

for data in test_data_sets:
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            test_ave_locations[x['x'] + ", " + x['y']] = []
            
    for x in data['results']:
        if x['MAC'] != "00:00:00:00:00:00":
            seenMAC = False            
            for y, j in test_ave_locations.items():
                for k in j:
                    if x['x'] == k['x'] and x['y'] == k['y'] and x['MAC'] == k['MAC']:
                        seenMAC = True                    
            if seenMAC == False:
                test_ave_locations[x['x'] + ", " + x['y']].append({'MAC':x['MAC'], 'LEVEL': 0, 'x':x['x'], 'y':x['y'], 'ave_count':0, 'std_dev':0})

new_json = []
for x, i in ave_locations.items():
    new_json.append(i[0])
file_str = "{results: " + str(new_json) + "}"
fo = open("averaged_data.json", "wb")
fo.write(bytes(file_str, "utf-8"));
fo.close

print("numer of locations: ")
print(len(locations))
##print(locations)
print("ammount of data")
print(len(data_sets[0]))
print("number of invald MACs")
print(invalid_MAC)

#ave_locations = {}
#for x, i in locations.items():
#    if ave_locations == {}:
#        ave_locations[x] = []
#        ave_locations[x].append(i[0])
#    isSame = False
#    for y, j in ave_locations.copy().items():
#        if x == y:
#            
#            isSame = True            
#    if isSame == False:
#        ave_locations[x] = []
#        ave_locations[x].append(i[0])

total_count = 0            
for x, i in locations.items():
    for y, j in ave_locations.items():
        if x == y:
            for k in i:
                for l in j:
                    if k['MAC'] == l['MAC']:
#                        l['ave_count'] += 1
#                        delta = l['LEVEL'] - l['LEVEL']
#                        l['LEVEL'] += delta / l['ave_count']
#                        l['std_dev'] += delta*(k['LEVEL'] - l['LEVEL'])
#                        total_count += 1
                        l['LEVEL'] += k['LEVEL']
                        l['std_dev'] += k['LEVEL']**2
                        l['ave_count'] += 1
            
for x, i in ave_locations.items():
    for k in i:
        k['std_dev'] -= k['LEVEL']
        k['std_dev'] = (k['std_dev']/5)**.5                
        k['LEVEL'] /= 5
        

total_count = 0            
for x, i in test_locations.items():
    for y, j in test_ave_locations.items():
        if x == y:
            for k in i:
                for l in j:
                    if k['MAC'] == l['MAC']:
#                        l['ave_count'] += 1
#                        delta = l['LEVEL'] - l['LEVEL']
#                        l['LEVEL'] += delta / l['ave_count']
#                        l['std_dev'] += delta*(k['LEVEL'] - l['LEVEL'])
#                        total_count += 1
                        l['LEVEL'] += k['LEVEL']
                        l['std_dev'] += k['LEVEL']**2
                        l['ave_count'] += 1
            
for x, i in test_ave_locations.items():
    for k in i:
        k['std_dev'] -= k['LEVEL']
        k['std_dev'] = (k['std_dev']/5)**.5                
        k['LEVEL'] /= 5
            
    
    
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
#color_list = ["Black", "Green", "Red", "DimGray", "SkyBlue", "Orange", "DeepPink", "BlueViolet", "Yellow", "Green", "IndianRed",  "SpringGreen", "DarkOliveGreen", "LightSteelBlue", "Ivory", "Gray", "MistyRose", "Goldenrod", "Orchid"]
colors = []
color_count = 0 

closest_list = []
closest_average_list = []
closest_bit_list = []
closest_bit_average_list = []
closest_sigma_list = []
closest_sigma_average_list = []
acount = -1

matches = 0
matches_bit = 0
matchless = 0
for a, i in test_ave_locations.items():
    print("matches = ", matches, " ", matches_bit)
    color_count += 1
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
        isPointMatched = False
        if i != j:
            loc_dist = ((float(i[0]['x']) - float(j[0]['x']))**2 +
            (float(i[0]['y']) - float(j[0]['y']))**2)**.5
            dist_sum = 0
            dist_sum_bit = 0            
            dist_sum_sigma = 0
            for k in i:
               ##print(k)
                current_dist = float(k['LEVEL'])
                current_bit_dist = 1
                for l in j:
                    if k['MAC'] == l['MAC']:
                        current_dist -=  float(l['LEVEL'])
                        current_bit_dist = 0
                        isMatched = True
                        isPointMatched = True
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

            distances_loc.append(loc_dist)
            distances_signal.append(dist_sum**.5)
            if dist_sum < closest_dist and isPointMatched == True:
                closest = j
                closest_dist = dist_sum
                closest_loc_dist = loc_dist
                
            distances_loc_bit.append(loc_dist)
            distances_signal_bit.append(dist_sum)
            if dist_sum_bit < closest_bit_dist and isPointMatched == True:
                closest_bit = j
                closest_bit_dist = dist_sum_bit
                closest_bit_loc_dist = loc_dist
#       colors.append(color_list[color_count-1])
        #print('distance = ', dist_sum_bit)
    if isMatched == False:
        closest_dist = -1
        closest = i
        closest_loc_dist = 0        
        closest_bit_dist = -1
        closest_bit = i
        closest_bit_loc_dist = 0
        matchless += 1
        
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
                        current_bit_dist =0
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
            if dist_sum <= closest_list[acount][2]+50:
#                print('closest distance = ',  closest_list[acount][2])
#                print('dist_sum = ', dist_sum)
                matches += 1
                x_ave += float(j[0]['x'])
                y_ave += float(j[0]['y'])
            if dist_sum_bit <= closest_bit_list[acount][2]:
#                print('closest bit distance = ',  closest_bit_list[acount][2])
#                print('dist_sum_bit = ', dist_sum_bit)                
                matches_bit += 1
                x_ave_bit += float(j[0]['x'])
                y_ave_bit += float(j[0]['y'])

    if x_ave != 0 and y_ave != 0:
        closest_average_list.append([[i[0]['x'], i[0]['y']],[float(x_ave)/(matches), float(y_ave)/(matches)]])
        closest_bit_average_list.append([[i[0]['x'], i[0]['y']],[float(x_ave_bit)/(matches_bit), float(y_ave_bit)/(matches_bit)]])
    else:
        closest_average_list.append([[i[0]['x'], i[0]['y']],[i[0]['x'], i[0]['y']]])
        closest_bit_average_list.append([[i[0]['x'], i[0]['y']],[i[0]['x'], i[0]['y']]])
        
#print(closest_bit_list)
print('analysis run')
print('number unmatched = ', matchless)

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
    
plt.figure(figsize=(10,8))
title_size = 12
line_size = 1
plt.subplot(2,2,1)
#fig = plt.subplot(2,2,1)
plt.scatter(xs, ys, color = 'green')    
plt.scatter(test_xs, test_ys, color = 'red')    
for i in closest_bit_list:
#    ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    plt.plot([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])], 'blue', lw=line_size)
    if i[3] > 300:
        print(i)
#for i in closest_list:
    #ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    #print([i[0][0], -float(i[0][1])], [float(i[1][0]), -float(i[1][1])])
plt.title('Tunnels Closest Points by # APs Matched', fontsize=title_size)
plt.ylabel('y coordinate (map pixles)')
plt.xlabel('x coordinate (map pixles)')
plt.plot()

#plt.figure(2)
plt.subplot(2,2,3)
#fig = plt.subplot(2,2,2)
plt.scatter(xs, ys, color = 'green')    
plt.scatter(test_xs, test_ys, color = 'red')    
for i in closest_bit_average_list:
#    ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    plt.plot([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])], 'blue', lw=line_size)

#for i in closest_list:
    #ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    #print([i[0][0], -float(i[0][1])], [float(i[1][0]), -float(i[1][1])])
plt.title('Tunnels Closest Points by \n # APs Matched with Averaging', fontsize=title_size)
plt.ylabel('y coordinate (map pixles)')
plt.xlabel('x coordinate (map pixles)')
plt.plot()

#plt.figure(3)
plt.subplot(2,2,2)
#fig, ax = plt.subplot(2,2,3)
plt.scatter(xs, ys, color = 'green')    
plt.scatter(test_xs, test_ys, color = 'red')    
for i in closest_list:
#    ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    plt.plot([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])], 'blue', lw=line_size)
    if i[3] > 300:
        print(i)
#for i in closest_list:
    #ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    #print([i[0][0], -float(i[0][1])], [float(i[1][0]), -float(i[1][1])])
plt.title('Tunnels Closest Points by Euclidian Metric', fontsize=title_size)
plt.ylabel('y coordinate (map pixles)')
plt.xlabel('x coordinate (map pixles)')
plt.plot()

#plt.figure(4)
plt.subplot(2,2,4)
#fig, ax = plt.subplot(2,2,4)
plt.scatter(xs, ys, color = 'green')    
plt.scatter(test_xs, test_ys, color = 'red')    
for i in closest_average_list:
#    ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    plt.plot([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])], 'blue', lw=line_size)
#for i in closest_list:
    #ax.add_line(Line2D([i[0][0], i[1][0]], [-float(i[0][1]), -float(i[1][1])]))
    #print([i[0][0], -float(i[0][1])], [float(i[1][0]), -float(i[1][1])])
plt.title('Tunnels Closest Points by \n Euclidian Metric with Averaging', fontsize=title_size)
plt.ylabel('y coordinate (map pixles)')
plt.xlabel('x coordinate (map pixles)')
plt.plot()

plt.tight_layout()
plt.subplots_adjust(hspace = .35)
plt.savefig('C:/Users/jasyonl/Documents/My Dropbox/GitHub/MITtunnels/MITTunnels/analysis/finalfigures/'+training_data+test_data+'_all_graphs')
#plt.figure(2)
#plt.savefig(training_data+test_data+'_test_bit_average')
#plt.figure(3)
#plt.savefig(training_data+test_data+'_test_euclid')
#plt.figure(4)
#plt.savefig(training_data+test_data+'_test_euclid_average_50')
#plt.figure(0)
#plt.savefig('test')

plt.show()

#print(closest_list)

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
