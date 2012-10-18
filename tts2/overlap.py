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

queries = getData('qrys.txt')
documents = getData('docs.txt')

