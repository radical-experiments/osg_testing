import sys
import json
import pandas as pd
import pprint
from operator import itemgetter
from math import isnan


if len(sys.argv) == 1:
    print "Need to enter name of json file\n"
    sys.exit()

else:
    data_file = sys.argv[1]


pilot =  pd.DataFrame(index=[], columns=[])
unit = pd.DataFrame(index=[], columns=[])

pp = pprint.PrettyPrinter(indent=1)

with open(data_file) as json_data:
    d = json.load(json_data)
    #pp.pprint(d['pilot'][0])

    for i in range(len(d['pilot'])):
        tmp_pilot = {}
        tmp_pilot['id'] = int(d['pilot'][i]['_id'][6:])
        tmp_pilot['num_units'] = len(d['pilot'][i]['unit_ids'])
        for j in range(len(d['pilot'][i]['statehistory'])):
            if d['pilot'][i]['statehistory'][j]['state'] not in tmp_pilot:
                tmp_pilot[d['pilot'][i]['statehistory'][j]['state']] = d['pilot'][i]['statehistory'][j]['timestamp']
            else:
                tmp_pilot[d['pilot'][i]['statehistory'][j]['state']] = \
                    min(tmp_pilot[d['pilot'][i]['statehistory'][j]['state']], d['pilot'][i]['statehistory'][j]['timestamp'])
            
        tmp_pilot_df = pd.DataFrame(tmp_pilot, index=[i])
        pilot = pilot.append(tmp_pilot_df)


    for i in range(len(d['unit'])):
        tmp_unit = {}
        tmp_unit['id'] = int(d['unit'][i]['_id'][5:])
        tmp_unit['pilot'] = int(d['unit'][i]['pilot'][6:])
        tmp_unit['runloc'] = d['unit'][i]['stdout']
        #print d['unit']
        #print len(d['unit'][i]['statehistory']), d['unit'][i]['statehistory']
        for j in range(len(d['unit'][i]['statehistory'])):
            if d['unit'][i]['statehistory'][j]['state'] not in tmp_unit:
                tmp_pilot[d['unit'][i]['statehistory'][j]['state']] = d['unit'][i]['statehistory'][j]['timestamp']
            else:
                tmp_pilot[d['unit'][i]['statehistory'][j]['state']] = \
                    min(tmp_pilot[d['unit'][i]['statehistory'][j]['state']], d['unit'][i]['statehistory'][j]['timestamp'])
            
            tmp_unit[d['unit'][i]['statehistory'][j]['state']] = d['unit'][i]['statehistory'][j]['timestamp']
            #tmp_unit['StagingInput'] = d['unit'][i]['statehistory']['StagingInput']
            #tmp_unit['AgentStagingInput'] = d['unit'][i]['statehistory']['AgentStagingInput']

        tmp_unit_df = pd.DataFrame(tmp_unit, index=[i])
        unit = unit.append(tmp_unit_df)

 
#print unit
print pilot

#Print session
print data_file

#Print total number of units
print "Number of units: ", pilot['num_units']

#Find all unique locations where the units ran
run_locations = unit['runloc'].unique()
print "Locations Pilots ran on: %s", run_locations

#Find Tq

for i in range(len(pilot.index)):
    Tq = pilot['Active'][i] - pilot['PendingActive'][i]
    print "Tq: %f" % Tq

#Find TTC
for i in range(len(pilot.index)):
    if 'Canceled' in pilot:
        print "CANCELED"
        TTC = pilot['Canceled'][i] - pilot['Launching'][i]
    elif 'Done' in pilot:
        print "DONE"
        TTC = pilot['Done'][i] - pilot['Launching'][i]
    else:
        print "CHECKING UNITS"
        TTC = unit['Done'].max() - pilot['Launching'][0]
    print "TTC: %f" % TTC


#Check if there are any units which did not finish correctly (Enter Done Stage)
incomplete_units = unit['Done'].isnull().sum()
print "Num Incomplete Units: %d" % incomplete_units

#Check if there are any units which did not finish executing
unexecuted_units = unit['PendingOutputStaging'].isnull().sum()
print "Num Unexecuted Units: %d" %  unexecuted_units


#Find the total Tx of the units. Since there may be some overlap in the units,
#   sorting the list, then creating a master range by checking if there is any
#   overlap in the ranges. Then sum up the lengths of the intervals to get Tx
#This algorithm can be implemented for any timings generically
Tx_array = []
for i in range(pilot['num_units'][0]):
    if not isnan(unit['PendingOutputStaging'][i]):
        Tx_array.append([unit['Executing'][i], unit['PendingOutputStaging'][i]])

Tx_array = sorted(Tx_array, key=itemgetter(0))

Tx_interval = []
print Tx_interval
Tx_interval.append(Tx_array[0])

current_interval = 0

for i in range(1, len(Tx_array)):
    if Tx_array[i][0] < Tx_interval[current_interval][1]:
        Tx_interval[current_interval][1] = Tx_array[i][1]
    else:
        Tx_interval.append(Tx_array[i])
        current_interval += 1

Tx = 0
for i in range(len(Tx_interval)):
    Tx += Tx_interval[i][1] - Tx_interval[i][0]

print "Tx: %f" % Tx
