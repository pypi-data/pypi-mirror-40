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
import exit
from pathlib import Path
import base64
import readline
import time
from exit import LIST_PIDS
COMMANDS = ['start', 'accounts', 'new', 'exit','change','help']
COMMANDS_NEXT = ['close','other']

username = ''
servername = ''

VERSION = sys.version_info.major

DATAPATH = '/usr/share/vpnkit/'

# for stop check internet timer
CHECK_STATUS = True

INTERNET_STATUS = False

CHECK_DEF_EXISTS = 'default'

LIST_ACCOUNTS = []


if VERSION != 2:
    CHECK_DEF_EXISTS = bytes(CHECK_DEF_EXISTS, 'utf-8')


# Choosing action when  vpn tunnel up (exit or try new connection)
def NextChoose():
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_for_next)
    global INTERNET_STATUS
    global CHECK_STATUS

    if VERSION == 2:
        try:
            choose = raw_input("Choose [close|other]: ").replace(" ", "") or 'other'
        except KeyboardInterrupt:
            CHECK_STATUS = False
            print("\nClosing...")
            sys.exit(1)
    else:
        try:
            choose = input("Choose [close|other]: ").replace(" ", "") or 'other'
        except KeyboardInterrupt:
            CHECK_STATUS = False
            print("\nClosing...")
            sys.exit(1)

    if choose == 'close':
        with open(DATAPATH + 'pids.txt', 'w') as file:
            for pid in exit.LIST_PIDS:
                file.write(str(pid)+'\n')
        print("Closing...")
        if INTERNET_STATUS:
            CHECK_STATUS = False
            # exit.kill_proc('client.conf')
            # exit.del_route(servername)
        sys.exit(1)

    elif choose == 'other':
        CHECK_STATUS = False
        try:
            exit.kill_proc(exit.LIST_PIDS)
        except Exception as e:
            print(e)
            print('Process openvpn  don\'t kill')
        exit.del_route(servername)
        exit.get_def_ip()
        exit.add_def_ip()
        start()

    elif choose != ' ':
        print("Operation '" + choose + "' not found")
        NextChoose()


# start openvpn and delete default route  from ip route table
def startOpenVpn():
    global servername
    check_up = 'Initialization Sequence Completed'
    if VERSION != 2:
        check_up = bytes(check_up, 'utf-8')

    exit.del_route(servername)
    exit.LIST_PIDS = []
    print (exit.bcolors.OKGREEN+"Your config must be in :" + DATAPATH + exit.bcolors.ENDC)
    p = subprocess.Popen(['sudo', 'openvpn', '--config', DATAPATH + 'client.conf'], stdout=subprocess.PIPE)
    exit.LIST_PIDS.append(p.pid)
    exit.LIST_PIDS.append(int(p.pid)+2)
    internet_on(servername)

    while True:
        output = p.stdout.readline()

        if output == '' and p.poll() is not None:
            break

        if output:
            print (output.strip().decode('utf-8'))

        if check_up in output:
            pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
            for line in pl.splitlines():
                if CHECK_DEF_EXISTS in line:

                    fields = line.strip().split()
                    global def_ip
                    def_ip = fields[2]
            d = subprocess.call(
                ['sudo', 'ip', 'route', 'del', 'default'],
                stdout=subprocess.PIPE)
            NextChoose()
            break


# getting certificates for openvpn from the server by username
def getCertificate(username, servername):
        if servername != '' and username != '':
            req = requests.get('http://' + servername + '/download/' + username + '/', allow_redirects=True)
            if req.status_code == 200:
                open(username + '.tar.gz', 'wb').write(req.content)
                tar = tarfile.open(username + '.tar.gz', "r")
                tar.extractall()
                print(exit.bcolors.OKGREEN + 'Certificates received' + exit.bcolors.ENDC)
                return True
            else:
                if req.json()['response'] == 'User not exists':
                    with open(DATAPATH + 'settings.ini', 'r') as file:
                        lines = file.readlines()
                    if len(lines) > 1:
                        line_number = 0
                        for line in lines:
                            line_number += 1
                            if username in line:
                                lines.remove(line)
                        lines = lines[:-1]
                        if len(lines)>1:
                            lines.append(lines[len(lines) - 1])
                        with open(DATAPATH + 'settings.ini', 'w') as new_file:
                            new_file.truncate(0)
                            for line in lines:
                                new_file.write(line)
                    get_settings()
                if req.content:
                    print(exit.bcolors.FAIL + 'Server response: ' + req.json()['response'] + exit.bcolors.ENDC)
                else:
                    print (exit.bcolors.FAIL + 'Error download certificates.' + exit.bcolors.ENDC)
                return False
        else:
            print(exit.bcolors.WARNING+'Please, enter connection parameters by typing \'new\' '+ exit.bcolors.ENDC)


def save_settings():
    settings = username + ',' + servername + ','+def_ip.decode("utf-8")+'\n'
    with open(DATAPATH+'settings.ini', 'r') as file:
        # read a list of lines into data
        data = file.readlines()
    if len(data) == 1:
        data.append(settings)
    else:
        data[len(data)-1] = settings

    with open(DATAPATH+'settings.ini', 'a') as fs:
        fs.truncate(0)
        fs.writelines(data)
        fs.write(settings)


def set_account(account):
    global servername
    global username
    servername = LIST_ACCOUNTS[account][1]
    username = LIST_ACCOUNTS[account][0]

    with open(DATAPATH + 'settings.ini', 'r+b') as myfile:
        # Read the last 1kiB of the file
        # we could make this be dynamic, but chances are there's
        # a number like 1kiB that'll work 100% of the time for you
        myfile.seek(0, 2)
        filesize = myfile.tell()
        blocksize = min(1024, filesize)
        myfile.seek(-blocksize, 2)
        # search backwards for a newline (excluding very last byte
        # in case the file ends with a newline)
        index = myfile.read().rindex(b'\n', 0, blocksize - 1)
        # seek to the character just after the newline
        myfile.seek(index + 1 - blocksize, 2)
        # read in the last line of the file
        lastline = myfile.read()
        # modify last_line
        lastline = username + ',' + servername + ',' + def_ip.decode("utf-8") + '\n'
        # seek back to the start of the last line
        myfile.seek(index + 1 - blocksize, 2)
        # write out new version of the last line
        if VERSION == 2:
            lastline = lastline.encode('utf-8')
        else:
            lastline = bytes(lastline,'utf-8')
        myfile.write(lastline)
        myfile.truncate()


def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def complete_for_next(text, state):
    for cmd in COMMANDS_NEXT:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


# start vpnkit client. User can choose action
def start():
    global username
    global servername
    get_list_accounts()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    with open(DATAPATH + 'pids.txt', 'a') as file:
        file.truncate(0)
    print('Current - Username: {} , Servername: {}'.format(username,servername))

    if VERSION == 2:
        try:
            startChoose = raw_input("Choose operations[start|new|accounts|change|help|exit]: ").replace(" ", "") or 'start'
        except KeyboardInterrupt:
            print("\nClosing...")
            sys.exit()
    else:
        try:
            startChoose = input("Choose operations[start|new|accounts|change|help|exit]: ").replace(" ", "") or 'start'
        except KeyboardInterrupt:
            print("\nClosing...")
            sys.exit()
    if startChoose == 'new':

        if VERSION == 2:
            try:
                hex = raw_input("Enter personal code: ").replace(" ", "")
            except KeyboardInterrupt:
                print("\nClosing...")
                sys.exit()

        else:
            try:
                hex = input("Enter personal code: ").replace(" ", "")
            except KeyboardInterrupt:
                print("\nClosing...")
                sys.exit()
        try:
            decode_result = base64.b64decode(hex).decode('utf-8').split('\n')
            username = decode_result[0]
            servername = decode_result[1]
        except:
            print(exit.bcolors.FAIL + 'Incorrect code' + exit.bcolors.ENDC)
            start()

        check_account = False
        for line in LIST_ACCOUNTS:
            if line[0] == username:
                check_account = True
        if not check_account:
            save_settings()
        get_list_accounts()
        result = getCertificate(username, servername)
        if result:
            startOpenVpn()
        elif not result:
            start()

    elif startChoose == 'start':
        get_list_accounts()
        result = getCertificate(username, servername)
        if result:
            startOpenVpn()
        elif not result:
            start()

    elif startChoose == 'accounts':
        print (exit.bcolors.OKGREEN+"Your accounts:"+exit.bcolors.ENDC)
        line_number = 0
        line_count = file_len(DATAPATH + 'settings.ini')
        for line in LIST_ACCOUNTS:
            if line_number !=0 and line_number != line_count-1:
                if line[0] == username:
                    print (exit.bcolors.OKGREEN + '*{} Username:{} , server {}'.format(line_number, line[0],
                                                                                       line[1]) + exit.bcolors.ENDC)
                else:
                    print (' {} Username:{} , server {}'.format(line_number, line[0], line[1]))
            line_number += 1
        start()

    elif startChoose == 'exit':
        if INTERNET_STATUS:
            global CHECK_STATUS
            CHECK_STATUS = False
        sys.exit(1)

    elif startChoose == 'help':
        print('\nOpenvpn CLI client. Available commands:\n'
              '\n\t'+exit.bcolors.UNDERLINE+'start'+exit.bcolors.ENDC+' - default option. Start openvpn service with current parameters.\n'
              ' \n\t'+exit.bcolors.UNDERLINE+'new'+exit.bcolors.ENDC+' - option for start new connection with new parameters.\n'
              '\n\t'+exit.bcolors.UNDERLINE+'accounts'+exit.bcolors.ENDC+' - list of your active server accounts.\n'
              '\n\t'+exit.bcolors.UNDERLINE+'change'+exit.bcolors.ENDC+' - option for change accounts.\n'
              '\n\t'+exit.bcolors.UNDERLINE+'help'+exit.bcolors.ENDC+' - option for getting application helper.\n'
              '\n\t'+exit.bcolors.UNDERLINE+'exit'+exit.bcolors.ENDC+' - option for exit from the appliation , kill openvpn process and up default connection.\n'
              '\n After connect options:\n'
              '\n\t'+exit.bcolors.UNDERLINE+'close'+exit.bcolors.ENDC+' - close current connection and up default. Exit from the application.\n'
              '\n\t'+exit.bcolors.UNDERLINE+'other'+exit.bcolors.ENDC+'- close current connection and up default. You can try  up new connection to openvpn server.\n')
        start()

    elif startChoose == 'change':
        check_len = len(LIST_ACCOUNTS) - 2
        if check_len > 1:
            text = 'Enter account number 1-{}: '.format(check_len )
            if VERSION == 2:
                try:
                    choose = raw_input(text) or '1'
                except KeyboardInterrupt:
                    print("\nClosing...")
                    sys.exit()
            else:
                try:
                    choose = input(text) or '1'
                except KeyboardInterrupt:
                    print("\nClosing...")
                    sys.exit()
            if choose.isdigit():
                if int(choose) > check_len:
                    print(exit.bcolors.WARNING + "Enter correct number" + exit.bcolors.ENDC)
                    start()
                else:
                    acc = int(choose)
                    set_account(acc)
                    result = getCertificate(username, servername)
                    if result:
                        startOpenVpn()
                    else:
                        start()
            else:
                print(exit.bcolors.FAIL + 'Invalid number' + exit.bcolors.ENDC)
                start()
        else:
            print(exit.bcolors.WARNING+"You don't have accounts for change"+exit.bcolors.ENDC)
            start()

    elif startChoose != ' ':
        print(exit.bcolors.WARNING+"Operation '" + startChoose + "' not found" + exit.bcolors.ENDC)
        start()


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def internet_enter_on():
    #  check internet connection on start vpnkit
    try:
        requests.get('http://216.58.192.142', timeout=1)
        global INTERNET_STATUS
        INTERNET_STATUS = True
        return True
    except Exception as err:
        return False


def internet_on(servername):
    #  check internet connection
    global INTERNET_STATUS

    t = threading.Timer(3.0, internet_on,[servername])
    t.start()

    if not CHECK_STATUS:
        t.cancel()
    else:
        try:
            requests.get('http://216.58.192.142', timeout=1)
            INTERNET_STATUS = True
            return True
        except Exception as err:
            pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
            for line in pl.splitlines():
                if CHECK_DEF_EXISTS in line:
                    fields = line.strip().split()
                    global def_ip
                    def_ip = fields[2]
                    # delete default route to avoid several instance openvpn conflict
                    d = subprocess.call(
                        ['sudo', 'ip', 'route', 'del', 'default'],
                        stdout=subprocess.PIPE)

                    # add route for traffic to openvpn reconnect
                    p = subprocess.call(
                        ['sudo', 'ip', 'route', 'add', servername, 'via', def_ip],
                        stdout=subprocess.PIPE)
            INTERNET_STATUS = False
            return False
        except socket.timeout as e:
            pass


def get_list_accounts():
    global LIST_ACCOUNTS
    LIST_ACCOUNTS = []
    with open(DATAPATH + 'settings.ini') as fp:
        line = fp.readline()
        while line:
            lines = line.replace('\n', '').split(',')
            LIST_ACCOUNTS.append(lines)
            line = fp.readline()


def get_settings():
    global username
    global servername
    global def_ip
    global LIST_ACCOUNTS
    settings_file = DATAPATH + 'settings.ini'
    file = Path(DATAPATH + 'settings.ini')

    pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if CHECK_DEF_EXISTS in line:
            fields = line.strip().split()
            def_ip = fields[2]

    # check if file exists and it's empty
    if file.is_file() and os.stat(settings_file).st_size != 0:
        get_list_accounts()
        username = LIST_ACCOUNTS[len(LIST_ACCOUNTS)-1][0]
        servername = LIST_ACCOUNTS[len(LIST_ACCOUNTS)-1][1]
    else:
        with open(DATAPATH+'settings.ini', 'w') as file:
            file.write(username + ',' + servername + ',' + def_ip.decode("utf-8")+ '\n')


# check vpnkit already starts  or not
def check_start_status():
    proc_name = 'vpnkit.py'
    count_proc = exit.get_proc_count(proc_name)
    # this vpnkit already started and will be in processes list
    if count_proc > 2:
        print ("VpnKit is already started")
        sys.exit(1)


def main():
    # check internet connection status for start openvpn
    result = internet_enter_on()
    # check vpnkit already starts  or not
    check_start_status()
    if result:
        get_settings()
        # change dir . Openvpn can find certificates.
        os.chdir(DATAPATH)
        start()
    else:
        print("No internet connection or you were disconnected")
        sys.exit(1)


if __name__ == '__main__':
    main()
