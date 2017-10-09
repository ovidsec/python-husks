#!/usr/bin/env python

import multiprocessing, sys, time, re
from multiprocessing import Pool, Manager, current_process, cpu_count 

class bcolors :
    red         = "\033[1;31m"
    darkred     = "\033[0;31m"
    green       = "\033[1;32m"
    yellow      = "\033[1;33m"
    blue        = "\033[1;34m"
    darkblue    = "\033[0;34m"
    silver      = "\033[0;37m"
    white       = "\033[1;37m"
    close       = "\033[1;m"

oddRE = re.compile(r'(.+[1|3|5])')
evenRE = re.compile(r'(.+[2|4|6])')

variable1 = "\x31"*5; variable2 = "2"; variable3 = ["3"] 
variable4 = {"variable4":"4"}; variable5 = 5
variable6 = {"variable6":[variable1,variable2,variable3,variable4,variable5]}

def print_function(Name,procname,variableA,variableB,variableC) :
    print "%s:\t -> %s %s %s %s" % (procname,Name,variableA,variableB,variableC); return

def even_function(Name,procname,host,command,shellcode) :
    print "%s:\t" % (procname),"Printing even function!"
    print_function(Name,procname,variable2,variable4,variable6)
    return

def odd_function(Name,procname,variable1,variable3,variable5) :
    print "%s:\t" % (procname),"Printing odd function!"
    print_function(Name,procname,variable1,variable3,variable5)
    return

def tasks_function(Name,variable1,variable2,variable3,variable4,variable5,variable6) :
    current = multiprocessing.current_process()
    procname = current.name
    try :
        if evenRE.search(Name) :
            print "%s:\tDoing stuff for %s." % (procname,Name)
            even_function(Name,procname,variable2, variable4, variable6)
            
        if oddRE.search(Name) :
            print "%s:\tDoing stuff for %s." % (procname,Name), "...but sleeping first"
            time.sleep(3)
            odd_function(Name,procname,variable1, variable3, variable5)
    except Exception as e:
        print e
    return

def multi_run_wrapper(args) :
    return tasks_function(*args)

def main() :
    print "Title here"
    multiprocessing.freeze_support()
    PROCESSES = 4
    print '\r\n\tCreating pool with:\t%d processes' % PROCESSES
    pool = Pool(PROCESSES)
    print '\tNo. of cpu\'s present:\t%d cores' % cpu_count()
    procList = ["process1", "process2", "process3", "process4", "process5", "process6" ]
    for Name in procList :
        pool.imap_unordered(multi_run_wrapper,[(Name,variable1,variable2,variable3, variable4,variable5,variable6)])
    pool.close();    pool.join()

if __name__ == '__main__' :
    main()

