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

    def getRoomInfo(self, i, user=None):
        join = (user == self.rooms[i]['user']['name'] or user == self.rooms[i]['player']['name']) and not user is None
        isUser = user == self.rooms[i]['user']['name'] if join else True
        room = self.rooms[i]
        uData = room['user' if isUser else 'player']
        pData = room['player' if isUser else 'user']
        return {
            'id': i,
            'user': uData['name'],
            'player': pData['name'],
            'uReady': uData['ready'],
            'pReady': pData['ready'],
            'move': (not room['uMove'] != isUser) and join,
            'won': room['won'],
            'isOwner': isUser and join,
            'canJoin': join
        }

    def sendRooms(self, user):
        r = []
        for i in range(len(self.rooms)):
            r += [self.getRoomInfo(i, user)]
        self.p.replyj(user, {'cmd': 'setRooms()', 'data': r})

    def sendRoom(self, user, i):
        info = self.getRoomInfo(i, user)
        if info['canJoin']:
            r = {'info': info}
            r['uBoard'] = self.rooms[i]['user' if info['isOwner'] else 'player']['board']
            r['pBoard'] = [x.replace('O', ' ').replace('/', ' ').replace('\\', '.') for x in self.rooms[i]['player' if info['isOwner'] else 'user']['board']]
            self.p.replyj(user, {'cmd': 'setRoom()', 'data': r})
        else:
            self.p.replyj(user, {'cmd': 'error()', 'type': 'you-are-not-in-the-room', 'data': [user, info['user'], info['player']]})
    r'''
    BOARD:
    ' ' - water
    '.' - bomb (shot in water)
    'O' - ship (one deck of it)
    '-' - shot deck of ship
    'X' - sank ship (all decks of it are shot)
    '/' - place where ship cannot be placed
    '\' - / but shot
    '''

    def build(self, user, i, pos):
        info = self.getRoomInfo(i, user)
        if info['canJoin']:
            x, y = pos
            data = self.rooms[i]['user' if info['isOwner'] else 'player'] # board, ready, aShips, ships, iBuilding
            outOfBoard = lambda x, y: x < 0 or y < 0 or x >= len(data['board']) or y >= len(data['board'][x])
            if outOfBoard(x, y):
                self.p.replyj(user, {'cmd': 'error()', 'type': 'coords-out-of-board', 'data': [(x, y), (len(data['board']), len(data['board'][x])]})
            def bset(x, y, c): # board set
                if outOfBoard(x,y):
                    return ' '
                data['board'][x] = data['board'][x][:y] + c + data['board'][x][y+1:]
                return data['board'][x][y]
            bget = lambda x, y: ' ' if outOfBoard(x,y) else data['board'][x][y]
            # check being of chosen coordinates out of ship being built
            # if so, end the building of previous ship
            # if it's max of such ships, send an error()
            # -------------------------------------
            # check aShips and ships
            # if there cannot be more ships with more boards, end the process of building
            # -------------------------------------
            # check if user has chosen place where ship has already been placed,
            # if so, delete whole ship
        else:
            self.p.replyj(user, {'cmd': 'error()', 'type': 'you-are-not-in-the-room', 'data': [user, info['user'], info['player']]})

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
                    aShips = [4, 3, 2, 1]
                    default = lambda x:{
                        'name': x,
                        'board': [' '*10]*10,
                        'ready': False,
                        'aShips': aShips, # amount of ships to be built
                        'ships': len(aShips) * [[]],
                        'beingBuilt': [],
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
                elif ev['cmd'] == 'joinRoom()': # i
                    self.sendRoom(ev['user'], int(ev['i']))
                elif ev['cmd'] == 'build()': # i, pos
                    self.build(user, i, pos)
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
