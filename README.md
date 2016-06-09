# OSG_Testing
This repository contains data gathered from testing the Open Science Grid (OSG)

##### TODO: Deciding on which data to use for data/logs for failed runs.
##### TODO: Writing more READMEs in subdirectories

### Setup

#### Software and Version

1. RADICAL Pilot Version    v0.40.1-22-ge1f4683@devel
2. RADICAL SAGA Version     0.40.1
3. RADICAL Utils Version    0.40

#### Execution Location
* RADICAL VM (144.76.72.175)

#### Scripts
* osg_char_setup.sh
  * Used to setup environment for testing
* getting_started_osg_early.py 
  * Uses Round Robin Scheduler
* getting_started_osg.py
  * Uses Backfilling Scheduler
* raw_data/round_robin/json_read.py
  * Used to read data from logs and extract relevant fields (TTC, Tx, Tq, etc...)
* raw_data/round_robin/auto_read.sh
  * Goes through all json files (assuming the json files are in the folders corresponding the #Pilots and #Units Per Pilot (if even distributed)

##### TODO: Create ./bin and move json_read.py and auto_read.sh to ./bin, additional scripts to further automate data collection

#### Data Location
* raw_data/
  * Contains log files (JSON) for successful runs, and some log files of unsuccessful runs. In case of unsuccessful runs, there are callback files (DAT) which try to capture the behavior of the runs, if possible
* cleaned_data/
  * Contains cleaned data (in csv or xlsx form), scripts to generate plots and the plots themselves

### Workload
* Executable Information
 * /bin/sh -c "sleep 10" (Duration is 10 sec)
  * It should be noted that the script also echos the OSG HostName, but sleep 10 dominates the execution in time
* Task Information
 * The number of tasks equals the number of units
 * The range of number of units submitted is [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048] 

### Resource Overlay
* The range of number of pilots submitted is [1, 2, 4, 8, 16, 32]
* Each pilot gets 1 Core (?? Need to double check)
* Each pilot has Walltime = 1800 min
* The scheduler is either Round Robin or Backfilling, depending on the script

### Resource
* OSG
 * Endpoint: xd-loging.opensciencegrid.org


