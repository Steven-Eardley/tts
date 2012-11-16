# -*- coding: utf-8 -*-
# Ranking program for Text Technologies Assignment 4
# Steven Eardley s0934142

from sys import argv, exit
import operator

if len(argv) != 2:
    print "\nUse: ranker.py inputFile.txt\n"
    exit()

# Files for output
hubs = open('hubs.txt', 'w')
auth = open('auth.txt', 'w')
pr = open('pr.txt', 'w')

# graph_info is a dict: {sender : ([outgoing], [incoming])}
graph_info = dict()

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
                graph_info[sender][0].append(recipient)
            except KeyError:
                graph_info[sender] = ([recipient], [])
            
            try:
                graph_info[recipient][1].append(sender)
            except KeyError:
                graph_info[recipient] = ([], [sender])
            
def pagerank(iterations, lmbda):
    n = float(len(graph_info))
    
    init_score = 1.0 / n
    
    # Initialise PageRank score in a dict: {sender : PageRank_score}
    scores = dict(zip(graph_info.keys(), [init_score]*len(graph_info)))
    
    for i in range(0,iterations):
        for (person, (outgoing, incoming)) in graph_info.items():
            # Sum the scores of incoming links to our person
            total_inc_score = 0.0
            for inc in incoming:
                                         # divide score by no. of outgoing links
                 total_inc_score += scores[inc] / float(len(graph_info[inc][0]))
            
            scores[person] = (1 - lmbda) / n + lmbda * total_inc_score
    return scores
    

createGraph()
score = pagerank(10, 0.8)
for (person, score) in sorted(score.iteritems(), key=operator.itemgetter(1), reverse = True):
    print "%.8f" % score,
    print person

#for (k, (o,i)) in graph_info.items():
#    print "ADDRESS %s" % k
#    print "OUTGOING"
#    print list(o)
#    print "INCOMING"
#    print list(i)

# using Decimal slowed it down too much