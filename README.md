# OSG_Testing
This repository contains data gathered from testing the Open Science Grid (OSG)

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

- Description of the workload:
  . Number of tasks.
  . Number of cores of the tasks (if heterogeneous, specify the distribution).
  . Duration of the tasks (if heterogeneous, specify the distribution).
  . Executable(s) of the tasks.
  . Number of Input/Output files if any.
  . Size of Input/Output files if any (if heterogeneous, specify the distribution).

- Description of the resource overlay:
  . How many pilots.
  . Number of cores of each pilot (if heterogeneous, specify the distribution).
  . Walltime of each pilot (if heterogeneous, specify the distribution).
  . Type of scheduler used to schedule CUs to the pilot(s).
  . Number of pilots per resource (if heterogeneous, specify the distribution).

- Description of the resources:
  . Endpoint(s) used to submit pilots.



TODO: Deciding on which data to use for data/logs for failed runs.
