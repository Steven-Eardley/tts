# -*- coding: utf-8 -*-
# Ranking program for Text Technologies Assignment 4
# Steven Eardley s0934142

from sys import argv, exit
from math import sqrt
from nltk.probability import FreqDist
import operator

if len(argv) != 2:
    print "\nUse: ranker.py inputFile.txt\n"
    exit()

# Files for output
#hubs = open('hubs.txt', 'w')
#auth = open('auth.txt', 'w')
#pr = open('pr.txt', 'w')

# graph_info is a dict: {sender : ([outgoing], [incoming])}
graph_info = dict()

def createGraph():
    f = open(argv[1], 'r')
    try:
        raw_data = f.readlines()
    finally:
        f.close()
    
    for line in raw_data:
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
    
    for i in range(iterations):
        
        # Identify the sink nodes and sum their scores
        sink = 0.0
        for (person, score) in scores.items():
            if len(graph_info[person][0]) == 0:
                sink += score
      
        for (person, (outgoing, incoming)) in graph_info.items():
            # Sum the scores of incoming links to our person
            total_inc_score = 0.0
            
            for inc in incoming:
                 # divide score by no. of outgoing links
                 total_inc_score += scores[inc] / float(len(graph_info[inc][0]))
                 
            scores[person] = (1.0 - lmbda + lmbda * sink) / n + lmbda * total_inc_score
    return scores

def hubs_auth(iterations):
    # n is the number of people (pages)
    n = float(len(graph_info))
    init_score = sqrt(n)
    
    # Initialise HITS score in two dicts: {sender : initial_score}
    hub_scores = dict(zip(graph_info.keys(), [init_score]*len(graph_info)))
    auth_scores = dict(zip(graph_info.keys(), [init_score]*len(graph_info)))
    
    for i in range(iterations):

        # Update the hub scores 
        norm_hub = 0.0
        for (person, (outgoing, incoming)) in graph_info.items():
            # Sum the authority scores of all outgoing links from our hub
            out_scores = [auth_scores[out] for out in outgoing]
            sum_out_auth = float(sum(out_scores))
            hub_scores[person] = sum_out_auth
            norm_hub += sum_out_auth * sum_out_auth

        # Update authority scores
        norm_auth = 0.0
        for (person, (outgoing, incoming)) in graph_info.items():
            # Sum the hub scores of all incoming links to our authority
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
        
def part_one():
    # Run both algorithms on the graph and write results to files
    pr_scores = pagerank(10, 0.8)
    (hub_scores, auth_scores) = hubs_auth(10)

    print "\nPageRank"
    for (person, score) in list(sorted(pr_scores.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
        pr.write("{0:.8f} {1}\n".format(score, person))
    pr.close()

    print "\nHub Score"
    # Print hub scores
    for (person, hub_score) in list(sorted(hub_scores.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
        hubs.write("{0:.8f} {1}\n".format(hub_score, person))
    hubs.close()

    print "\nAuthority Score"
    # Print authority scores
    for (person, auth_score) in list(sorted(auth_scores.iteritems(), key=operator.itemgetter(1), reverse = True))[:10]:
        auth.write("{0:.8f} {1}\n".format(auth_score, person))
    auth.close()

def part_two():
    # Read back the top list of names from part one
    pr_read = open('pr.txt', 'r')
    hubs_read = open('hubs.txt', 'r')
    auth_read = open('auth.txt', 'r')
    try:
        pr_data = pr_read.readlines()
        hub_data = hubs_read.readlines()
        auth_data = auth_read.readlines()
    finally:
        pr_read.close()
        hubs_read.close()
        auth_read.close()

    # interesting people have high page rank scores
    interesting_people = []
    for line in pr_data:
        [score, person] = line.split()
        interesting_people.append(person)
        
    # hub-y people have high hub scores
    hub_people = []
    for line in hub_data:
        [score, person] = line.split()
        hub_people.append(person)
    
    # authority-y people have high auth scores
    auth_people = []
    for line in auth_data:
        [score, person] = line.split()
        auth_people.append(person)
    
    # Lets see who the interesting people email / are emailed by most
    for int_person in interesting_people:
        (out_connections, in_connections)= graph_info[int_person]
        out_fdist = FreqDist(out_connections)
        in_fdist = FreqDist(in_connections)
        print int_person,
        print out_fdist.items()[:5]
        print in_fdist.items()[:5]
        
        
createGraph()
#part_one()
part_two()