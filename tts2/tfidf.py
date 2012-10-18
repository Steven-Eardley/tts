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

def evalTfidf(query, document):
	similarity = 0
	
	# Remove duplicates from the document
	docSet = list(set(document[1]))
	
	# If the keyword appears in the set, increment the similarity score.
	for keyword in query[1]:
		if docSet.count(keyword) > 0:
			similarity += 1

	if similarity > 0:
		report = '{0} 0 {1} 0 {2} 0'.format(query[0], document[0], similarity)
		return report
	else:
		return None

outFile = open('overlap.top', 'w')
queries = getData('qrys.txt')
documents = getData('docs.txt')

for query in queries:
	for document in documents:
		result = evalTfidf(query, document)
		if result != None:
			outFile.write(result + '\n')
outFile.close()


