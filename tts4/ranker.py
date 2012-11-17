# -*- coding: utf-8 -*-
# Ranking program for Text Technologies Assignment 4
# Steven Eardley s0934142

from sys import argv, exit
from math import sqrt
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
            
            scores[person] = (1.0 - lmbda) / n + lmbda * total_inc_score
    return scores

def hubs_auth(iterations):
    n = float(len(graph_info))
    
    init_score = sqrt(n)
    
    # Initialise HITS score in two dicts: {sender : score}
    hub_scores = dict(zip(graph_info.keys(), [init_score]*len(graph_info)))
    auth_scores = dict(zip(graph_info.keys(), [init_score]*len(graph_info)))
    
    for i in range(0,iterations):

        # Update the hub scores 
        norm_hub = 0.0
        for (person, (outgoing, incoming)) in graph_info.items():
            out_scores = [auth_scores[out] for out in outgoing]
            sum_out_auth = float(sum(out_scores))
            hub_scores[person] = sum_out_auth
            norm_hub += sum_out_auth * sum_out_auth

        # Update authority scores
        norm_auth = 0.0
        for (person, (outgoing, incoming)) in graph_info.items():

            inc_scores = [hub_scores[inc] for inc in incoming]
            sum_inc_hub = float(sum(inc_scores))
            auth_scores[person] = sum_inc_hub
            norm_auth += sum_inc_hub * sum_inc_hub
        
        # Normalise the scores
        for (person, hub_score) in hub_scores.items():
            hub_scores[person] = hub_score / sqrt(norm_hub)
        for (person, auth_score) in auth_scores.items():
            auth_scores[person] = auth_score / sqrt(norm_auth)

    return (hub_scores, auth_scores)
        
 

createGraph()
score_pr = pagerank(10, 0.8)
(hub_scores, auth_scores) = hubs_auth(10)

print "\nPageRank"
for (person, score) in list(sorted(score_pr.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
    print "%.8f" % score,
    print person
print 'jeff:',
print "%.8f" % score_pr['jeff.dasovich@enron.com']

print "\nHub Score"
# Print hub scores
for (person, hub_score) in list(sorted(hub_scores.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
    #if person == 'jeff.dasovich@enron.com':
    print "%.8f" % hub_score,
    print person
print 'jeff:',
print "%.8f" % hub_scores['jeff.dasovich@enron.com']

print "\nAuthority Score"
# Print authority scores
for (person, auth_score) in list(sorted(auth_scores.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
    print "%.8f" % auth_score,
    print person
print 'jeff:',
print "%.8f" % auth_scores['jeff.dasovich@enron.com']



#for (k, (o,i)) in graph_info.items():
#    print "ADDRESS %s" % k
#    print "OUTGOING"
#    print list(o)
#    print "INCOMING"
#    print list(i)

# using Decimal slowed it down too much