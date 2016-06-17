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
    #pp.pprint(d['pilot'])
    #pp.pprint(d['unit'])

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
#print pilot

print '----------------------------------------------------------------'

if unit.empty or pilot.empty:
    if unit.empty:
        print "EMPTY UNIT DATAFRAME"
    if pilot.empty:
        print "EMPTY PILOT DATAFRAME"
    sys.exit()

#Print session
print data_file

#Prints ATTEMPT for grep later. This counts a run tried
print "ATTEMPT"

#Print total number of units
print "Number of units: ", int(pilot['num_units'].sum())

#Print distribution of units per pilot
pilot_dist = []
for i in range(int(len(pilot['num_units']))):
    pilot_dist.append(int(pilot['num_units'][i]))
print "Pilot Distribution: ", pilot_dist
#print pilot['num_units']

#Find all unique locations where the units ran
unique_runloc = {}
run_location = unit['runloc']
for i in range(len(run_location.index)):
    if run_location[i] not in unique_runloc:
        unique_runloc[run_location[i]] = 1
    else: 
        unique_runloc[run_location[i]] += 1

runloc = []
for k, v in unique_runloc.iteritems():
    runloc.append((k, v))

for i in range(len(runloc)):
    print "Unique Running Locations: ", runloc[i]
#for loc in unique_runloc:
#    print "RunLoc: ", [(loc, unique_runloc[loc])]
    #print "RunLocCount: ", unique_runloc[loc]
#print "Locations Pilots ran on: %s", run_locations

#Find Tq
Tq = []
for i in range(len(pilot.index)):
    try:
        tmp_tq = pilot['Active'][i] - pilot['PendingActive'][i]
        if not isnan(tmp_tq):
            Tq.append(tmp_tq)
    except:
        print "HELD. Tq: -1"
        sys.exit()
print "Tq per Pilot: ", Tq

#Check if there are any units which did not finish correctly (Enter Done Stage)
try:
    incomplete_units = unit['Done'].isnull().sum()
    print "Incomplete Units: %d" % incomplete_units
except:
    print "No Units were Done"
    sys.exit()

#Check if there are any units which did not finish executing
unexecuted_units = unit['PendingOutputStaging'].isnull().sum()
print "Unexecuted Units: %d" %  unexecuted_units

if incomplete_units > 0:
    print "Units were hung up"
    sys.exit()


#Find TTC
TTC = []
for i in range(len(pilot.index)):
    if 'Canceled' in pilot:
        TTC.append(pilot['Canceled'][i] - pilot['Launching'][i])
        print "CANCELED\tTTC: %f" %TTC
    elif 'Done' in pilot:
        TTC.append(pilot['Done'][i] - pilot['Launching'][i])
        print "DONE\tTTC: %f" %TTC
    else:
        try:
            if isnan(unit[unit['pilot'] ==  i]['Done'].max() - pilot['Launching'][i]):
                print "At least one pilot was not running"
            TTC.append(unit[unit['pilot'] == i]['Done'].max() - pilot['Launching'][i])
            print "CHECKING UNITS"
        except:
            print "HELD, but has Tq > 0"
            sys.exit()
print unit['Done'].max(), pilot['Launching'].min()
print "TTC: ", unit['Done'].max() - pilot['Launching'].min()
print "TTC per pilot: ", TTC

#Prints SUCCESS to indicate that run is successful. For grep later
print "SUCCESS"

#Find the total Tx of the units. Since there may be some overlap in the units,
#   sorting the list, then creating a master range by checking if there is any
#   overlap in the ranges. Then sum up the lengths of the intervals to get Tx
#This algorithm can be implemented for any timings generically
Tx_array = []
for i in range(len(unit.index)):
    if not isnan(unit['PendingOutputStaging'][i]):
        Tx_array.append([unit['Executing'][i], unit['PendingOutputStaging'][i]])

Tx_array = sorted(Tx_array, key=itemgetter(0))
Tx_interval = []
Tx_interval.append(Tx_array[0])
current_interval = 0

if len(Tx_array) > 1:
    for i in range(1, len(Tx_array)):
        if Tx_array[i][1] <= Tx_interval[current_interval][1]:
            pass
#            print "array list is contained in interval list", Tx_array[i], Tx_interval[current_interval]
#            print "skipping to next interval list"
        else:
#           print "array list extends interval list"
            if Tx_array[i][0] >= Tx_interval[current_interval][1]:
#                print "Outside of current interval. Appending, then breaking", Tx_array[i], Tx_interval[current_interval]
                Tx_interval.append(Tx_array[i])
                current_interval += 1
            else:
#                print "Overlapping range. Extending, then breaking", Tx_array[i], Tx_interval[current_interval]
                Tx_interval[current_interval][1] = Tx_array[i][1]

Tx = 0
for i in range(len(Tx_interval)):
    Tx += Tx_interval[i][1] - Tx_interval[i][0]

print "Tx: %f" % Tx

Tq_array = list()
for i in range(len(pilot.index)):
    Tq_array.append([pilot['PendingActive'][i], pilot['Active'][i]])

Tq_array = sorted(Tq_array, key=itemgetter(0))
Tq_interval = []
Tq_interval.append(Tq_array[0])

current_interval = 0

if len(Tq_array) > 1:
    for i in range(1, len(Tq_array)):
#        if Tq_array[i][0] < Tq_interval[current_interval][1]:
#            if Tq_array[i][1] > Tq_interval[current_interval][1]:
#                Tq_interval[current_interval][1] = Tq_array[i][1]
#        else:
#            Tq_interval.append(Tq_array[i])
#            current_interval += 1
        if Tq_array[i][1] <= Tq_interval[current_interval][1]:
            pass
        if Tq_array[i][1] > Tq_interval[current_interval][1]:
            if Tq_array[i][0] > Tq_interval[current_interval][1]:
                Tq_interval.append(Tq_array[i])
                current_interval += 1
            else:
                Tq_interval[current_interval][1] = Tq_array[i][1]

    for j in range(len(Tx_interval)):
        for i in range(len(Tq_interval)):
#           Checks if the Tq and Tx ranges overlap. If not, then break out of loop
            if Tq_interval[i][0] >= Tx_interval[j][1]:
                 pass
#                print "Tx Interval is before the current Tq interval"
            elif Tq_interval[i][1] <= Tx_interval[j][0]:
#                print "Tx Interval is after the current Tq interval"
                 pass
#           Checks if the Tq range is contained in the Tx. If so, then set the Tq range to have
#           Tq = 0, as the all of the time is used in Tx
            elif (Tq_interval[i][0] >= Tx_interval[j][0]) & (Tq_interval[i][1] <= Tx_interval[j][1]):
                Tq_interval[i] = [0.0, 0.0]
#                print "The current Tq Interval is contained in the Tx interval"
                continue
#           Checks if the Tx is contained in the Tq. If so, split Tq into two ranges to remove the
#           Tx from the Tq range
            elif (Tq_interval[i][0] <= Tx_interval[j][0]) & (Tq_interval[i][1] >= Tx_interval[j][1]):
#                print "Tx is contained in the Tq range"
            #   Checks if there is any waiting after Tx finishes
                if Tq_interval[i][1] > Tx_interval[j][1]:
#                    print "Adding a a subinterval for Tq after the Tx ends but before the original Tq interval ends, possibly length 0"
                    Tq_interval.insert(i + 1, [Tx_interval[j][1], Tq_interval[i][1]])

                #Tq_interval.append([Tx_interval[j][1], Tq_interval[i][1]])
            #   else: Tq_interval[i][1] == Tx_interval[j][1]:      The Tx ends when Tq ends,
            #   and there is no waiting (Tq) after Tx
                
                #Checks if there is any waiting before Tx starts

                if Tq_interval[i][0] < Tx_interval[j][0]:
#                    print "Readjusting the Tq so that it starts when the original Tq starts, but ends when the Tx starts, possibly to length 0"
                    Tq_interval[i][1] = Tx_interval[j][0]
                #Tq_interval[i][1] = Tx_interval[j][0]
            #   else: Tq_interval[0] == Tx_interval[j][0]: Tx startes when Tq starts,
            #   and there is no waiting (Tq) before Tx. Thus there is no waiting starting from
            #   the beginning of Tq

#           So the Tq and Tx overlaps, but one is not contained in the other
            else:
#                print "There is some overlap"
            #   If i-th Pilot starts waiting while j-th CU is executing
                if Tq_interval[i][0] > Tx_interval[j][0]:
#                    print "Tx before after Tq starts. Remove section of Tq where Tx also happens"
                    Tq_interval[i][0] = Tx_interval[j][1]
            #   If j-th CU start executing while i-th CU is waiting
                elif Tq_interval[i][1] < Tx_interval[j][1]:
#                    print "Tq ends beofre Tx ends. Remove section of Tq where Tx also happens"
                    Tq_interval[i][1] = Tx_interval[j][0]

Tq = 0.0
for i in range(len(Tq_interval)):
    Tq += Tq_interval[i][1] - Tq_interval[i][0]

print "Tq: %f" % Tq

tmp = unit['Done'].max() - pilot['PendingLaunch'].min()
print "Tq + Tx: %f, TTC: %f, diff: %f" % ((Tx + Tq), tmp, tmp - (Tx + Tq))
