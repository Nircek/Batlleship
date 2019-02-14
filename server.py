#!/usr/bin/env python3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config['PseudoPHPServer']['url'], config['PseudoPHPServer']['token'])
