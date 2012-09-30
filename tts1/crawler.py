# -*- coding: utf-8 -*-
# Web crawler for TTS Assignment 1
# Steven Eardley s0934142

import re
import urllib
import robotparser
import heapq

useragent = "TTS"
rp = robotparser.RobotFileParser()
frontier = []
visited = []
denied = []

baseURL = "http://ir.inf.ed.ac.uk/tts/A1/0934142/"
startpage = "0934142.html"

# Find the top level directory given a URL
def findRootURL(url):
	matchRoot = re.match('.*?[//]*[\w.\w]+/', url)
	return matchRoot.group()

# Sets up the restrictions for the given domain
def setUpRobot(url):
	robotURL = findRootURL(url) + "robots.txt"
	rp.set_url(robotURL)
	rp.read()
	rp.modified()

# Check if domain has changed
def checkDomainChange(url, base):
	if findRootURL(url) != findRootURL(base):
		return True
	else:
		return False

# Load a page as a string
def loadPage(url):
	longURL = baseURL + url
	if rp.can_fetch(useragent,longURL):
		page = urllib.urlopen(longURL)
		visited.append(url)
		return page.read()
	else:
		denied.append(url)
		return None

# Parse URLs between CONTENT comments on a page
def grabURLs(page):
	if page != None:
		matchContent = re.search('<!-- CONTENT -->.*<!-- /CONTENT -->', page, re.DOTALL)
		if matchContent:
			content = matchContent.group()

			# Once the content region has been identified, extract the URLs
			urls = re.findall('(?<=a href=")\S*\.[A-za-z]+', content)
			for url in urls:
				matchDigits = re.search('\d+', url)
				priority = int(matchDigits.group())
				# The priority must be negated because heapq implements a min heap
				heapq.heappush(frontier, (-(priority),url))


unique = 0
setUpRobot(baseURL)
grabURLs(loadPage(startpage))

while len(frontier) > 0:
	(priority, url) = heapq.heappop(frontier)
	if visited.count(url) == 0 and denied.count(url) == 0:
		unique += 1
		grabURLs(loadPage(url))

print len(visited)
print len(denied)
print unique
