import csv
import os

data = 'Edin'
poi_file = os.path.join('origin_data', f'poi-{data}.csv')
traj_file = os.path.join('origin_data', f'traj-{data}.csv')
if not os.path.exists(os.path.join('adapted_data', data)):
    os.makedirs(os.path.join('adapted_data', data))
train_file = os.path.join('adapted_data', data, 'traj_train.csv')
test_file = os.path.join('adapted_data', data, 'traj_test.csv')
valid_file = os.path.join('adapted_data', data, 'traj_valid.csv')

# read POI file in csvDictReader
poi = {}
with open(poi_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        poi[row['poiID']] = row
# find the max and min lat and lon
max_lat = max([float(poi[key]['poiLat']) for key in poi])
min_lat = min([float(poi[key]['poiLat']) for key in poi])
max_lon = max([float(poi[key]['poiLon']) for key in poi])
min_lon = min([float(poi[key]['poiLon']) for key in poi])
print('max_lat:', max_lat, 'min_lat:', min_lat, 'max_lon:', max_lon, 'min_lon:', min_lon)

# read traj file in csvDictReader
traj = {}
with open(traj_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        traj[row['trajID']] = traj.get(row['trajID'], []) + [row]
        
# sort the pois of a traj by time
for trajID in traj:
    traj[trajID] = sorted(traj[trajID], key=lambda x: x['startTime'])
    
# stack the traj records in a list
traj_list = []
for trajID, traj_records in traj.items():
    objID = traj_records[0]['userID'].split('@')[0] # userID as objID
    offsets = []
    offsets.append((0, # distance between start of the traj to the start of the segment
            int(traj_records[0]['startTime']), # start time of first poi as departure time
            float(poi[traj_records[0]['poiID']]['poiLon']),
            float(poi[traj_records[0]['poiID']]['poiLat'])))
    offsets.append((0, # distance between start of the traj to the start of the segment
            int(traj_records[-1]['startTime']), # start time of last poi as departure time
            float(poi[traj_records[-1]['poiID']]['poiLon']),
            float(poi[traj_records[-1]['poiID']]['poiLat'])))
    segSeq = []
    for record in traj_records:
        segSeq.append([int(record['poiID']), # segment id
                    int(record['startTime']), # entering time of this segment
                    10, # avg speed of this segment
                    int(record['poiDuration'])]) # duration of this segment
    traj_list.append([objID, trajID, offsets, segSeq])
    
# split the traj_list into train, test and validation set
data_len = len(traj_list)
train = traj_list[:int(data_len*0.6)]
test = traj_list[int(data_len*0.6):int(data_len*0.8)]
valid = traj_list[int(data_len*0.8):]

# write into csv files
with open(train_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(train)
with open(test_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(test)
with open(valid_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(valid)