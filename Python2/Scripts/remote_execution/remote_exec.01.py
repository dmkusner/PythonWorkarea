#!/bin/env python2.7

from argparse import ArgumentParser
import os
import sys
import paramiko
import zmq


def ssh_exec(cmd):
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('pcubu1.home.net')

        stdin, stdout, stderr = client.exec_command(cmd)

        if stdout:
            for line in stdout:
                print line.rstrip()

        if stderr:
            for line in stderr:
                print line.rstrip()
# end def


def master(cmd):
    print "Master issued cmd '{}'".format(cmd)
    ssh_exec(cmd)
# end def


def worker(cmd):
    print "I'm a worker!"
    print "Your '{}' is my command!".format(cmd)
# end def


def main():
    """
    """
    parser = ArgumentParser(description='Create a transcription datatest')
    parser.add_argument('type', choices=['MASTER','WORKER'], action='store', help="Execution type")
    parser.add_argument('command', action='store', help="remote cmd to execute")

    args = parser.parse_args()

    if args.type == 'MASTER':
        cmd = "{} {} WORKER '{}'".format(sys.executable, os.path.abspath(sys.argv[0]), args.command)
        master(cmd)
        
    if args.type == 'WORKER':
        worker(args.command)

# end def

if __name__ == '__main__':
    main()
