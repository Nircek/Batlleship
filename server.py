#!/usr/bin/env python3
import configparser
from pypps.PyPPSPS import *
import json

def q(x):
    print(x)
    return x

class Server:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.p = PyPPSPS(config['PseudoPHPServer']['url'], config['PseudoPHPServer']['token'])
        self.p.connect()
        print(self.p.version())
        self.initVars()

    def initVars(self):
        self.rooms = []
        self.getRooms()

    def count(self):
        try:
            self.p.varwrite('i', str(q(int(self.p.varread('i')[0])+1)))
        except PPSNullError:
            self.p.varwrite('i', str(q(0)))

    def getRooms(self):
        try:
            rooms = self.p.varreadj('rooms')
        except PPSNullError:
            self.setRooms()

    def setRooms(self):
        self.p.varwritej('rooms', self.rooms)

    def handleEvent(self):
        try:
            ev = self.p.popj()
        except PPSNullError:
            return False
        print(ev)
        b = False
        if 'cmd' in ev:
            if ev['cmd'] == 'getRooms()':
                self.p.replyj(ev['user'], {'cmd': 'setRooms()', 'data': self.rooms})
            else:
                b = True
        else:
            b = True
        if b:
            self.p.replyj(ev['user'], {'cmd': 'error()', 'type': 'cmd', 'data': ev})
        return True

s = Server()
s.count()
while s.handleEvent():
    pass
