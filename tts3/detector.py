# Plagiarism Detector for TTS Assignment 3
# Steven Eardley s0934142

import re
import random as r
from string import punctuation
from glob import glob
from sys import argv, exit
from itertools import combinations
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from difflib import SequenceMatcher

if len(argv) != 2:
    print "\nUse: detector.py dir\nWhere dir is the directory containing documents.\n"
    exit()

filenames = glob("{0}/*.txt".format(argv[1]))

# Dictionary for documents: key = doc number, value = preprocessed data (a list of words)
doc_dict = dict()

# Dictionary for hashes: key = doc number, value = document's hash value
hash_dict = dict()

# Dictionary for word hashes: key = word, value = random binary vector
word_dict = dict()

r.seed('TTS is great')

exact = open('exact.txt', 'w')
near = open('near.txt', 'w')
finn = open('finn.txt', 'w')

# Match any punctuation as defined in string.punctuation
nonPunc = re.compile('[%s]' % re.escape(punctuation))

# A list of stopwords from NLTK
stops = [w for w in stopwords.words('english')]

# Matches digits following a / (to get file numbers from path)
matchfileDigits = re.compile("(?<=/)\d+")

# Strip punctuation and stop words
def preprocess(doc_data):
    no_punc = nonPunc.sub('', doc_data)
    words = [w.lower() for w in no_punc.split() if not (w.lower() in stops)]
    return words

# Read a file as a string
def getData(filename):
	f = open(filename, 'r')
	try:
	    rawData = f.read()
	finally:
	    f.close()
	return rawData

def uniqueBinary(length):
    bin_string = bin(r.getrandbits(length))[2:]
    return ''.join(['0']*(length-len(bin_string))) + bin_string

# Fill the dictionary with preprocessed documents
def buildDicts(files):
    for doc in files:
        doc_words = preprocess(getData(doc))
        doc_dict[doc] = doc_words

        # Add unknown words to the word dictionary
        for word in set(doc_words):
            if not word in word_dict:
                word_dict[word] = uniqueBinary(32)
        hash_dict[doc] = simhash(doc_words)

# Check for exact matches in two documents
def checkExact(doc1, doc2):
    compare_length = min(len(doc1), len(doc2))
    matches = 0
    for index in range(0, compare_length):
        if doc1[index] == doc2[index]:
            matches += 1

    # If 90% of words match, call it an exact match.
    if matches > (compare_length * 0.9):
        return True
    else:
        return False

def checkNear(hash1, hash2):
    s = SequenceMatcher(None, hash1, hash2)
    r = s.ratio()
    if r >= 0.96:
        return True
    else:
        return False

def simhash(words):
    fdist = FreqDist(words)
    v = [0]*32
    for (token, freq) in fdist.items():
        token_hash = [int(val) for val in word_dict[token]]
        for i in range(freq):
            for index in range(len(v)):
                if token_hash[index] == 1:
                    v[index] += 1
                else:
                    v[index] -= 1
    simhash = ['0']*32
    for j in range(len(v)):
        if v[j] > 0:
            simhash[j] = '1'
    return ''.join(simhash)

def checkFinn(doc1,doc2):
    return False

buildDicts(filenames)

# Use combinations to pair filenames and compare.
for (a,b) in combinations(filenames, 2):
    # Get document numbers
    label_a = re.search(matchfileDigits, a).group()
    label_b = re.search(matchfileDigits, b).group()
    # Write to relevant file if any checks are tripped
    if checkExact(doc_dict[a], doc_dict[b]):
        exact.write("{0}-{1}\n".format(label_a, label_b))
        checkNear(hash_dict[a], hash_dict[b])
    if checkNear(hash_dict[a], hash_dict[b]):
        near.write("{0}-{1}\n".format(label_a, label_b))
    if checkFinn(doc_dict[a], doc_dict[b]):
        finn.write("{0}-{1}\n".format(label_a, label_b))