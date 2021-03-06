# -*- coding: utf-8 -*-
# TTS Lab 1

#2
from Lab1Support import *
import re

def firstpart():
	text = readFile('task1.txt')
	tokens = re.split('[\\s]+', text)

	saveToFile(tokens,'tokens.txt')

#3
	numbers = [t for t in tokens if re.match('[0-9]+[\\.\\,0-9]*$', t)]

#4
	digits = [n[0:1] for n in numbers]

#5
	percentages = calculatePercentages(digits)

#6
	plot(percentages, 1)

#7
	alpha = [t for t in tokens if re.match('[a-zA-Z]+', t)]

#8
	termCounts = countTerms(alpha) 
	saveToFile(termCounts, 'termCounts.txt')

#9
	plot(termCounts, 2)

def secondPart():
	# Compares two documents with Benford's Law
	text1 = readFile('reports1.txt')
	tokens1 = re.split('[\\s]+', text1)
	
	text2 = readFile('reports2.txt')
	tokens2 = re.split('[\\s]+', text2)

	numbers1 = [ t for t in tokens1 if re.match('[0-9]+[\\.\\,0-9]*$', t) ]
	numbers2 = [ t for t in tokens2 if re.match('[0-9]+[\\.\\,0-9]*$', t) ]
	
	print numbers1[:50]

	digits1 = [n[0:1] for n in numbers1]
	digits2 = [n[0:1] for n in numbers2]

	percentages1 = calculatePercentages(digits1)
	percentages2 = calculatePercentages(digits2)
	
	plot(percentages1,1)
	plot(percentages2,1)

secondPart()
