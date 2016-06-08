#!/usr/bin/env python

__copyright__ = "Copyright 2013-2015, http://radical.rutgers.edu"
__license__   = "MIT"

import os
import sys
import radical.pilot as rp
import radical.utils as ru
import time

dh = ru.DebugHelper ()

RUNTIME  =  1800
SLEEP    =    10
PILOTS   =    32
UNITS    =    32
SCHED    = rp.SCHED_ROUND_ROBIN

resources = {
    'osg.xsede-virt-clust' : {
        'project'  : 'TG-CCR140028',
        'queue'    : None,
        'schema'   : 'ssh'
    },
    'osg.connect' : {
        'project'  : 'RADICAL',
        'queue'    : None,
        'schema'   : 'ssh'
    }
}
start_time = time.time()
p_state = []
u_state = []
#------------------------------------------------------------------------------
#
def pilot_state_cb (pilot, state):

    if not pilot:
        return

    #print "[Callback]: ComputePilot '%s' state: %s." % (pilot.uid, state)
#    p_state.append([pilot.uid, state, time.time() - start_time])
    print [pilot.uid, state, time.time() - start_time]   
    # Hello HTC :-)
    #if state == rp.FAILED:
    #    sys.exit (1)


#------------------------------------------------------------------------------
#
CNT = 0
def unit_state_cb (unit, state):

    if not unit:
        return

    global CNT

    #print "[Callback]: unit %s on %s: %s." % (unit.uid, unit.pilot_id, state)
#    u_state.append([unit.uid, unit.pilot_id, state, time.time() - start_time])
    print [unit.uid, unit.pilot_id, state, time.time() - start_time]
    if state in [rp.FAILED, rp.DONE, rp.CANCELED]:
        CNT += 1
        #print "[Callback]: # %6d" % CNT

    # Hello HTC :-)
    #if state == rp.FAILED:
    #    print "stderr: %s" % unit.stderr
    #    sys.exit(2)


#------------------------------------------------------------------------------
#
def wait_queue_size_cb(umgr, wait_queue_size):

    pass
    #print "[Callback]: wait_queue_size: %s." % wait_queue_size


#------------------------------------------------------------------------------
#
if __name__ == "__main__":

    # we can optionally pass session name to RP
    if len(sys.argv) > 1:
        resource = sys.argv[1]
    else:
        resource = 'local.localhost'

    print 'running on %s' % resource

    # Create a new session. No need to try/except this: if session creation
    # fails, there is not much we can do anyways...
    session = rp.Session()
    print "session id: %s" % session.uid

    # all other pilot code is now tried/excepted.  If an exception is caught, we
    # can rely on the session object to exist and be valid, and we can thus tear
    # the whole RP stack down via a 'session.close()' call in the 'finally'
    # clause...
    try:

        pmgr = rp.PilotManager(session=session)
        pmgr.register_callback(pilot_state_cb)

        pdescs = list()
        for p in range(PILOTS):
            pdesc = rp.ComputePilotDescription()
            pdesc.resource        = resource
            pdesc.cores           = 1
            pdesc.project         = resources[resource]['project']
            pdesc.queue           = resources[resource]['queue']
            pdesc.runtime         = RUNTIME
            pdesc.cleanup         = False
            pdesc.access_schema   = resources[resource]['schema']
            pdesc.candidate_hosts = [#'MIT_CMS',
                                     #'UConn-OSG',
                                     '!SU-OG', # No compiler
                                     '!FIU_HPCOSG_CE', # zeromq build fails
                                     #'BU_ATLAS_Tier2',
                                     '!UCSDT2', # Failing because of format character ...
                                     '~(HAS_CVMFS_oasis_opensciencegrid_org =?= TRUE)'
                                    ]
            pdescs.append(pdesc)

        pilots = pmgr.submit_pilots(pdescs)

        umgr = rp.UnitManager(session=session, scheduler=SCHED)
        umgr.register_callback(unit_state_cb,      rp.UNIT_STATE)
        umgr.register_callback(wait_queue_size_cb, rp.WAIT_QUEUE_SIZE)
        umgr.add_pilots(pilots)
        
        cuds = list()
        for unit_count in range(0, UNITS):
            cud = rp.ComputeUnitDescription()
            cud.executable     = "/bin/sh"
            cud.arguments      = ["-c", "echo $HOSTNAME:$OSG_HOSTNAME && sleep %d" % SLEEP]
            cud.cores          = 1
            cuds.append(cud)

        units = umgr.submit_units(cuds)
       
        print session
        umgr.wait_units()

        print session

        #os.system('radicalpilot-close-session -m export -s %s' %session.uid)
        #for cu in units:
            
            #print "* Task %s state %s, exit code: %s, stdout: %s, started: %s, finished: %s" \
            #    % (cu.uid, cu.state, cu.exit_code, cu.stdout, cu.start_time, cu.stop_time)

      # os.system ("radicalpilot-stats -m stat,plot -s %s > %s.stat" % (session.uid, session_name))

#        print "Pilot Information"
#        for i in range(len(p_state)):
#            print p_state[i]
#        print "\n\nUnit Information"
#        for i in range(len(u_state)):
#            print u_state[i]
    
    except Exception as e:
        # Something unexpected happened in the pilot code above
        print "caught Exception: %s" % e
        raise

    except (KeyboardInterrupt, SystemExit) as e:
        # the callback called sys.exit(), and we can here catch the
        # corresponding KeyboardInterrupt exception for shutdown.  We also catch
        # SystemExit (which gets raised if the main threads exits for some other
        # reason).
        print "need to exit now: %s" % e
        
    finally:
        # always clean up the session, no matter if we caught an exception or
        # not.
        #print "closing session"
        os.system('radicalpilot-close-session -m export -s %s' %session.uid)
        session.close (cleanup=False)

        # the above is equivalent to
        #
        #   session.close (cleanup=True, terminate=True)
        #
        # it will thus both clean out the session's database record, and kill
        # all remaining pilots (none in our example).


#-------------------------------------------------------------------------------

