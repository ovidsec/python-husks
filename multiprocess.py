#!/usr/bin/env python

import os
import sys
from multiprocessing import Lock, Process, Queue, current_process
import socket
import signal


variables = "stringy strings"
listname = ['thingy one', 'thingy two', 'thingy three']


def signal_handler(signum, frame) :
        print "Control-C interrupt. Process Exiting..."  
        sys.exit(0)

def initiate_function(variables) :
	print "stuff: " + variables


def worker(work_queue, done_queue) :
	try :
		for variables in iter(work_queue.get, 'STOP') :
			status_code = initiate_function(variables)
	except Exception as e:
		print str(e)
	return True


def main() :
	signal.signal(signal.SIGINT, signal_handler)
	workers = 5
	work_queue = Queue()
	done_queue = Queue()
	processes = []

	for item in listname :
		work_queue.put((variables))

	for w in range(workers) :
		process = Process(target = worker, args = (work_queue, done_queue))
		process.start()
		processes.append(process)
		work_queue.put('STOP')

	for p in processes:
		process.join()

	done_queue.put('STOP')

	for status in iter(done_queue.get,'STOP') :
		print status





if __name__ == "__main__" :
	main()
