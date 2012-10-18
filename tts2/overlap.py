# -*- coding: utf-8 -*-
# Overlap Algorithm for TTS Assignment 2
# Steven Eardley s0934142

import re

# Return data from a file as a list of (number, [keyword]) tuples
def getData(filename):
	f = open(filename, 'r')
	try:
	    rawData = f.readlines()
	finally:
	    f.close()
	
	parsedData = []
	for rawDatum in rawData:
		matchDigits = re.match('\d+', rawDatum)
		number = matchDigits.group()
		wordStr = rawDatum[matchDigits.end():]
		words = wordStr.split()
		parsedData.append((number, words))
	return parsedData

# Write an array to a file, separated by newline characters
def saveToFile(data, filename):
	f = open(filename, 'w')
	try:
		for d in data:
			f.write(str(d) + '\n')
	finally:
	    f.close()

def evalOverlap(query, document):
	sim = 0
	if sim > 0:
		report = '{0} 0 {1} 0 {2} 0'.format(query[0], document[0], sim)
		return report
	else:
		return None

queries = getData('qrys.txt')
documents = getData('docs.txt')

print evalOverlap(queries[0],documents[0])
print documents[0]

