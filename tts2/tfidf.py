# -*- coding: utf-8 -*-
# Overlap Algorithm for TTS Assignment 2
# Steven Eardley s0934142

import re
import math

# Save the dfw data to ease computation
dfwDict = dict()

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

def findDfw(word,documents):
	if word not in dfwDict:
		dfw = len([1 for document in documents if document[1].count(word) > 0])
		dfwDict[word] = dfw
		return dfw
	else:
		return dfwDict[word]

def evalTfidf(query, documents, c, k, avgD):
	reports = []
	
	for document in documents:
		similarity = 0
		
		# The set of unique query words
		queryVocab = list(set(query[1]))
		

		for keyword in queryVocab:
			
			# The number of occurances of the keyword in the query
			tfwq = float(query[1].count(keyword))
			
			# The number of occurances of the keyword in the document
			tfwd = float(document[1].count(keyword))
			
			# The number of occurances of the keyword in all documents
			dfw = float(findDfw(keyword, documents))

			# |D| The document length
			d = float(len(document[1]))
			
			# tf.idf weighted sum
			similarity += (tfwq * (tfwd / (tfwd + ((k * d) / avgD))) *
math.log(c / dfw))

		if similarity > 0:
			report = '{0} 0 {1} 0 {2} 0'.format(query[0], document[0],
similarity)
			reports.append(report)
	return reports

outFile = open('tfidf.top', 'w')
queries = getData('qrys.txt')
documents = getData('docs.txt')

# |C| The total number of documents
c = float(len(documents))

# avg|D| The mean document length
avgD = float(sum([len(doc[1]) for doc in documents]) / c)

k = 2.0

for query in queries:
	results = evalTfidf(query, documents, c, k, avgD)
	for result in results:
		outFile.write(result + '\n')
outFile.close()


