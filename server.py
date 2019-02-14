#!/usr/bin/env python3
import configparser
from pypps.PyPPSPS import *

config = configparser.ConfigParser()
config.read('config.ini')
p = PyPPSPS(config['PseudoPHPServer']['url'], config['PseudoPHPServer']['token'])
p.connect()
print(p.version())
def q(x):
    print(x)
    return x
try:
    p.varwrite('', 'i', str(q(int(p.varread('', 'i')[0])+1)))
except PPSNullError:
    p.varwrite('', 'i', '0')
