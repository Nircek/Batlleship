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
            self.p.varwrite('', 'i', str(q(int(self.p.varread('', 'i')[0])+1)))
        except PPSNullError:
            self.p.varwrite('', 'i', str(q(0)))

    def getRooms(self):
        try:
            rooms = json.loads(''.join(self.p.varread('', 'rooms')))
        except PPSNullError:
            self.setRooms()

    def setRooms(self):
        self.p.varwrite('', 'rooms', json.dumps(self.rooms))

    def handleEvent(self):
        try:
            ev = self.p.pop()
        except PPSNullError:
            return False
        print(ev)
        if len(ev) > 1:
            if ev[1] == 'getRooms()':
                self.p.reply(ev[0], json.dumps({'cmd': 'setRooms()', 'data': json.dumps(self.rooms)}))
        return True

s = Server()
s.count()
while s.handleEvent():
    pass
