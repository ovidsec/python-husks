#!/usr/bin/env python

import os
import stat
import sys
import re
import random
import socket
import signal
import time
from Crypto.PublicKey import RSA
import StringIO

port = ""
portnow = 0
portnext = 0
keydict = {}
mode = stat.S_IRUSR | stat.S_IWUSR 
end = str("*"*8 + "END" + "*"*8)
size = 64
stringfilter = re.compile(r'(-----)')

def signal_handler(signum, frame) :
    print "Control-C interrupt. Process Exiting..."
    sys.exit(0)

def seedgen() :
    seed = random.randint(10240,65535)  #starting port 
    return(seed)

def authkeyWrite(pubkey) :
    with os.fdopen(os.open("~/.ssh/authorized_keys", os.O_WRONLY | os.O_CREAT,0600),'w') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))


def keygen(mode,size) :
    key = RSA.generate(2048)
    privkey = key.exportKey('PEM')
    counter = 0
    for line in privkey.split('\n'):
        splits=[line[x:x+size] for x in range(0,len(line),size)]
        for item in splits :
            if stringfilter.search(item) :
                pass
            else :
                keydict[counter] = item
                counter = counter + 1
    keydict[counter] = end
    pubkey = key.publickey()
    authkeyWrite(pubkey) 
    with os.fdopen(os.open("~/.ssh/authorized_keys", os.O_WRONLY | os.O_CREAT,0600),'w') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))
    return keydict

def two_ports(portnow,portnext) :
    if portnow == 0 :
        portnow = random.randint(1024,65534)
    else :
        portnow = portnext
    portnext = random.randint(1024,65534)
    return(portnow,portnext)


def serversetup():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return(server)

def post_data(keydict,i,portnow,portnext,server,size):
    print str(portnow)+keydict[i] + "0"*(size-len((keydict[i]))) + "?"*(5-len(str(portnext))) + str(portnext)
    connection, addr = server.accept()
    connection.sendall(keydict[i] + "0"*(size-len((keydict[i]))) + "?"*(5-len(str(portnext))) + str(portnext) + "\r\n")
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    return

def server_port(seed,port,portnow,portnext,keydict,size) :
    rows = (1600/size)-1
    for i in random.sample(range(0,rows),rows) :
        #print str(i), str(len(keydict[i])), str(keydict[i]), str(portnow), str(portnext)
        try :
            portnow,portnext = two_ports(portnow,portnext)
            server = serversetup()
            server.bind(("127.0.0.1",portnow))
            server.listen(1)
            post_data(keydict,i,portnow,portnext,server,size)
        except Exception as e:
            print "Error:", str(e), str(keydict[i]), str(portnow), str(portnext)
            pass

def main() :
    signal.signal(signal.SIGINT, signal_handler)
    keydict = keygen(mode,size)
    #print keydict
    seed = seedgen()
    server_port(seed,port,portnow,portnext,keydict,size)
    for key,val in keydict.iteritems() :
        print key,val
    
if __name__ == "__main__" :
    main()
