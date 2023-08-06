#!/usr/bin/env python
import sys
import os
import requests
import tarfile
import subprocess
import platform
import psutil
import threading
import socket


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DATAPATH = '/usr/share/vpnkit/'

VERSION = sys.version_info.major

DEF_IP = '192.168.1.1'

LIST_PIDS = []

#adding default route for up connection
def add_def_ip():
    global DEF_IP
    def_ip_exists = False
    check_def_exists = 'default'
    if VERSION != 2:
        check_def_exists = bytes(check_def_exists, 'utf-8')

    pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if check_def_exists in line:
            def_ip_exists = True
    if not def_ip_exists:
        p = subprocess.call(
            ['sudo', 'ip', 'route', 'add', 'default', 'via', DEF_IP],
            stdout=subprocess.PIPE)
        print(bcolors.OKGREEN+'Default connection up'+bcolors.ENDC)


# get pid of necessary process
def get_proc_pid(p):
    pid = p.pid
    return str(pid)


def get_procs_by_pid(pids, include_self=True):
    procs = []
    for p in psutil.process_iter():
        if (int(get_proc_pid(p)) in pids and
                (os.getpid() != p.pid or include_self)):
            procs.append(p)
    return procs


def kill_proc(pids, timeout=1):
    if len(pids) != 0:
        procs = get_procs_by_pid(pids, include_self=False)
        if len(procs) > 0:
            for p in procs:
                p.kill()
            _, procs = psutil.wait_procs(procs)

        if len(procs) > 0:
            print('Failed')
        else:
            print(bcolors.OKGREEN+'Process openvpn kill'+bcolors.ENDC)


def del_route(route):
    d = subprocess.call(
        ['sudo', 'ip', 'route', 'del', route ],
        stdout=subprocess.PIPE)

def get_def_ip():
    global DEF_IP

    with open(DATAPATH + 'settings.ini') as fp:
        settings = fp.readline()
        line = settings.replace('\n', '').split(',')
        DEF_IP = line[2]


def get_proc_count(name):
    count_proc = 0
    if VERSION != 2:
        name = bytes(name, 'utf-8')
    pl = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if name in line:
            count_proc += 1
    return count_proc

def main():
    global LIST_PIDS
    with open(DATAPATH + 'pids.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        LIST_PIDS.append(int(line.replace(' ','')))
    count_proc = get_proc_count('vpnkit')
    if count_proc < 7:
        try:
            kill_proc(LIST_PIDS)
        except Exception as e:
            print(e)
            print('Process openvpn  don\'t kill')
        get_def_ip()
        add_def_ip()


if __name__ == '__main__':
    main()
