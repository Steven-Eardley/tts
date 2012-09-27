import numpy as np
import matplotlib.pyplot as plt
import os
from operator import itemgetter
import re

def plot(array = [], law = 0, k = 16, beta = 0.5):


	if law == 1:
		BLdigits = np.arange(1, 10, 1.0)
		BLpercentage = np.log10(1+1/BLdigits)
		plt.plot(BLdigits, BLpercentage, '--', linewidth=1.0)
		plt.plot(BLdigits, array, 's', linewidth=1.0)
        	plt.axis(xmin=0, xmax=10, ymin=0)
		plt.xlabel('First digit')
		plt.ylabel('Occurrence')
		plt.title('Benford\'s Law')
		plt.legend()
		plt.grid(True)
		plt.show()

	if law == 2:

		x = 100000
		if len(array) > 0:
			x = len(array)

		HLtokens = np.arange(0, x, 1.0)
		HLtypes = k*HLtokens**beta
		plt.plot(HLtokens, HLtypes, '--')
		
		if len(array) > 0:
			plt.plot(HLtokens, array)

	        plt.axis(xmin=0, xmax=x, ymin=0)

		plt.xlabel('Tokens')
		plt.ylabel('Terms')
		plt.title('Heaps\' Law')
		plt.legend()
		plt.grid(True)
		plt.show()


def countTerms(tokens):
	termCount = [0]
	lastTermCount = 0
	terms = set([])
	for token in tokens:
		if token not in terms:
			lastTermCount += 1
			terms.add(token)
		termCount.append(lastTermCount)
	return termCount

def calculatePercentages(numbers):
	percentages = [None]*9
	total = len(numbers)
	for i in range(0,9):
		percentages[i] = numbers.count(str(i+1))
	return [float(n)/total for n in percentages ] 

def readFile(filename):
	f = open(filename, 'r')
	try:
	    content = f.read()
	finally:
	    f.close()
	return content

def saveToFile(data, filename):
	string = ''
	array = []
	f = open(filename, 'w')
	try:
	    if type(data) == type(string):
	    	f.write(data)
	    if type(data) == type(array):
	    	for d in data:
			f.write(str(d) + '\n')
	finally:
	    f.close()



