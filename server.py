#!/usr/bin/env python3
import configparser
from pypps.PyPPSPS import *
import traceback
import time

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
            self.rooms = self.p.varreadj('rooms')
        except PPSNullError:
            self.setRooms()

    def setRooms(self):
        self.p.varwritej('rooms', self.rooms)

    def sendRooms(self, user):
        r = []
        for i in range(len(self.rooms)):
            if user == self.rooms[i]['user']['name']:
                r += [{
                    'id': i,
                    'player': self.rooms[i]['player']['name'],
                    'move': self.rooms[i]['uMove'],
                    'won': self.rooms[i]['won']
                }]
            if user == self.rooms[i]['player']['name']:
                r += [{
                    'id': i,
                    'player': self.rooms[i]['user']['name'],
                    'move': not self.rooms[i]['uMove'],
                    'won': self.rooms[i]['won']
                }]
        self.p.replyj(user, {'cmd': 'setRooms()', 'data': r})

    def handleEvent(self):
        print('handling...')
        try:
            ev = self.p.popj()
        except PPSNullError:
            return False
        print(ev)
        try:
            b = False
            if 'cmd' in ev:
                if ev['cmd'] == 'getRooms()': # void
                    self.sendRooms(ev['user'])
                elif ev['cmd'] == 'newRoom()': # player
                    default = lambda x:{
                        'name': x,
                        'board': [' '*10]*10,
                        'ready': False,
                        'ships': [4, 3, 2, 1], # to be built
                        'iBuilding': 0
                    }
                    self.rooms += [{
                        'user': default(ev['user']),
                        'player': default(ev['player']),
                        'uMove': True,
                        'won': False
                        }]
                    self.setRooms()
                    self.sendRooms(ev['user'])
                else:
                    b = True
            else:
                b = True
            if b:
                self.p.replyj(ev['user'], {'cmd': 'error()', 'type': 'cmd', 'data': ev})
            return True
        except:
            exc = traceback.format_exc()
            self.p.replyj(ev['user'], {'cmd': 'error()', 'type': 'exception', 'data': exc})
            print(exc)

s = Server()
s.count()
x = time.time()-5
while 1:
    while not time.time()-5 > x or s.handleEvent():
        pass
    x = time.time()
