## Round Robin, Test Suite (05/20/2016 - 06/06/2016)

This folder contains the log files of pilot jobs submitted to OSG using the Round Robin Sheduler

### Software and Version
1. RADICAL Pilot  v0.40.1-22ge1f4683@devel
2. RADICAL SAGA   0.40.1
3. RADICAL Utils  0.40

### Naming Convention
Each folder is denoted by p**X**u**Y**, where **X** is the number of pilot submitted, and **Y** is the number of units per pilot if a round robin scheduler is used

### Data Cleaning

* json_read.py opens a log file in order extract the relevant fields and prints them in a particular format.
* auto_read.sh runs json_read.py and iterates through all logs in the folder, and stores the printed statements into a txt file
**TODO** Further automate data aggregation

The relevant fields include:

1. Whether the Pilots where Successful
2. Number of Units submitted
3. How many Units were unexecuted (Unit never reached state PendingOutputStaging) or incomplete (unit never reached state Done)
4. Unique Running locations of the Pilots
5. **Tq per pilot** (Waiting time on OSG Queue). Some pilots may not execute any CUs, but still wait on queue
6. **Net TTC** (Time to Completion) of the entire task
7. **TTC per pilot**, how long it takes for each pilot to wait on queue and run a task (if at all)
8. **Net Tx** (Execution Time),  the net execution time of the entire submission, accounting for any overlap with Tx of all units
9. **Net Tq**, the net queue waiting time of the entire submission, accounting for any overlap with Tx and Tq of all pilots
