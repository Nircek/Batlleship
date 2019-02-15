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

s = Server()
s.count()
