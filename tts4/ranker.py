# -*- coding: utf-8 -*-
# Ranking program for Text Technologies Assignment 4
# Steven Eardley s0934142

from sys import argv, exit

if len(argv) != 2:
    print "\nUse: ranker.py inputFile.txt\n"
    exit()

# Files for output
hubs = open('hubs.txt', 'w')
auth = open('auth.txt', 'w')
pr = open('pr.txt', 'w')

def createGraph():
    f = open(argv[1], 'r')
    try:
        rawData = f.readlines()
    finally:
        f.close()
    
    for line in rawData[:10]:
        [msg_id, sender, recipient] = line.split()
        print (sender, recipient)

createGraph()