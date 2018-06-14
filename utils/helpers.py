#this file contains common functions to be used through ECEL

import subprocess
import shlex

#executes system command
#takes shell command to execute as input
def execCommand(cmd):
    runcmd = shlex.split(cmd)
    try:
        process = subprocess.check_call(runcmd)
        
    except subprocess.CalledProcessError as err:
        print "Error attempting to run command : %s\n" % (cmd)
        print "System Error:", err
        
    except OSError as err:
            print "OSError attempting to run command : %s\n" % (cmd)
            print "System Error:", err
