# -*- coding: utf-8 -*-
# Web crawler for TTS Assignment 1
# Steven Eardley s0934142

import re
import urllib
import robotparser
import heapq

useragent = "TTS"
rp = robotparser.RobotFileParser()

startpage = "http://ir.inf.ed.ac.uk/tts/A1/0934142/0934142.html"

def setUpRobot(robotURL):
	rp.set_url(robotURL)
	rp.read()
	rp.modified()

def loadPage(url):
	if rp.can_fetch(useragent,url):
		return page = urllib.urlopen(url)
	else:
		return None

# Nab URLs between CONTENT comments on a page
def grabURLs(page):
	if page != None
	return 0

# Add a page to our frontier queue
def addPage(page,queue):
	return 0

setUpRobot("http://ir.inf.ed.ac.uk/robots.txt")

loadPage(startpage)

