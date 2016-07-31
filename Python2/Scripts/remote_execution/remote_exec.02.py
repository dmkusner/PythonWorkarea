#!/bin/env python2.7

from argparse import ArgumentParser
import os
import sys
import multiprocessing as mp
import subprocess as sp
import socket
import paramiko
import zmq


def pickUnusedPort():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port
# end def


def start_listener(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:{}".format(port))

    while True:
        #  Wait for next request from client
        message = socket.recv()
        socket.send("")
        if message == "Done!":
            break
        print("Received message: %s" % message)
# end def


def start_sender(host,port,cmd):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:{}".format(host,port))

    try:
        cmd = cmd.split()
        p = sp.Popen(cmd,shell=False,stdout=sp.PIPE,stderr=sp.STDOUT)
        (output,_) = p.communicate()
        if output:
            for line in output.splitlines():
                socket.send(line)
                socket.recv()
    finally:
        socket.send('Done!')
        socket.recv()
# end def


def ssh_exec(host,cmd):
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host)

        stdin, stdout, stderr = client.exec_command(cmd)

        if stdout:
            for line in stdout:
                print line.rstrip()

        if stderr:
            for line in stderr:
                print line.rstrip()
# end def


def master(port,cmd):
    remote_host = 'pcubu1.home.net'
    p = mp.Process(target=ssh_exec, args=(remote_host,cmd))
    p.start()
    start_listener(port)
# end def


def worker(master,port,cmd):
    start_sender(master,port,cmd)
# end def


def main():
    """
    """
    parser = ArgumentParser(description='Create a transcription datatest')
    subparsers = parser.add_subparsers(help='subcommand help')

    parser_master = subparsers.add_parser('MASTER', help='master process')
    parser_master.add_argument('command', action='store', help="remote cmd to execute")
    parser_master.set_defaults(type='master')

    parser_worker = subparsers.add_parser('WORKER', help='worker process')
    parser_worker.add_argument('host', action='store', help="name or ip of master host")
    parser_worker.add_argument('port', action='store', help="port number")
    parser_worker.add_argument('command', action='store', help="remote cmd to execute")
    parser_worker.set_defaults(type='worker')

    args = parser.parse_args()
    hostname = socket.getfqdn()
    port = pickUnusedPort()
    
    if args.type == 'master':
        cmd = "{} {} WORKER {} {} '{}'".format(sys.executable, os.path.abspath(sys.argv[0]), hostname, port, args.command)
        master(port,cmd)
        
    if args.type == 'worker':
        worker(args.host, args.port, args.command)

# end def


if __name__ == '__main__':
    main()
