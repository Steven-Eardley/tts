# Plagiarism Detector for TTS Assignment 3
# Steven Eardley s0934142

import re
from glob import glob
from sys import argv, exit
from itertools import combinations

if len(argv) != 2:
    print "\nUse: detector.py dir\nWhere dir is the directory containing documents.\n"
    exit()

filenames = glob("{0}/*.txt".format(argv[1]))[:4]

# Dictionary for documents: key = doc number, value = preprocessed data
doc_dict = dict()

exact = open('exact.txt', 'w')
near = open('near.txt', 'w')
finn = open('finn.txt', 'w')

matchfileDigits = re.compile("(?<=/)\d+")
#doc_no = matchfileDigits.group()

def preprocess(doc_data):
    return doc_data

def getData(filename):
	f = open(filename, 'r')
	try:
	    rawData = f.read()
	finally:
	    f.close()
	return rawData

def buildDict(files):
    for doc in files:
        doc_dict[doc] = preprocess(getData(doc))

def checkExact(doc1, doc2):
    return True

buildDict(filenames)

# Use combinations to pair filenames and compare.
for (a,b) in combinations(filenames, 2):
    # Get document numbers
    label_a = re.search(matchfileDigits, a).group()
    label_b = re.search(matchfileDigits, b).group()

    # Write to relevant file if any checks are tripped
    if checkExact(doc_dict[a], doc_dict[b]):
        exact.write("{0}-{1}\n".format(label_a, label_b))
        
    
# Match numbers following a /
#matchfileDigits = re.search("(?<=/)\d+", doc)
#doc_no = matchfileDigits.group()