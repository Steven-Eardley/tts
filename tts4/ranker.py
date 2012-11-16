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

# graph_info is a dict: {sender : ([outgoing], [incoming])}
graph_info = dict()

# PageRank info in a dict: {sender : PageRank_score}
scores = dict()

def createGraph():
    f = open(argv[1], 'r')
    try:
        rawData = f.readlines()
    finally:
        f.close()
    
    for line in rawData:
        [msg_id, sender, recipient] = line.split()
        if recipient != sender:
            try:
                graph_info[sender][0].add(recipient)
            except KeyError:
                graph_info[sender] = ([recipient], [])
            
            try:
                graph_info[recipient][1].add(sender)
            except KeyError:
                graph_info[recipient] = ([], [sender])
            
def pagerank(iterations, lmbda):
    n = len(graph_info)
    for i in range(0,iterations):
        for (person, (outgoing, incoming)) in graph_info.items():
            for inc in incoming:
                try:
                    
            neighbour_scores = [
            scores[person] = (1 - lmbda) / n + lmbda * sum(
            
    

createGraph()

#for (k, (o,i)) in graph_info.items():
#    print "ADDRESS %s" % k
#    print "OUTGOING"
#    print list(o)
#    print "INCOMING"
#    print list(i)