#!/usr/bin/env python3
from pypps.PyPPSPC import *
from code import interact
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
p = PyPPSPC(config['PseudoPHPServer']['url'])
p.connect()
print(p.version())
p.login(config['PseudoPHPServer']['user'], config['PseudoPHPServer']['pass'])
print(p.refreshj())
interact(local=locals())
