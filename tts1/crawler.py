# -*- coding: utf-8 -*-
# Web crawler for TTS Assignment 1
# Steven Eardley s0934142

import re
from urllib2 import urlopen, URLError, HTTPError
import robotparser
import heapq

useragent = "TTS"
rp = robotparser.RobotFileParser()
frontier = []
visited = []
denied = []

# Variable for statistics: (unique, denied, error, noContent)
stats = [0,0,0,0]

baseURL = "http://ir.inf.ed.ac.uk/tts/A1/0934142/"
startpage = "0934142.html"

# Find the top level directory given a URL
def findRootURL(url):
	matchRoot = re.match('.*?[//]*[\w.\w]+/', url)
	if matchRoot:
		return matchRoot.group()
	else:
		return None

# Sets up the restrictions for the given domain
def setUpRobot(url):
	robotURL = findRootURL(url) + "robots.txt"
	rp.set_url(robotURL)
	rp.read()
	rp.modified()

# If domain has changed, set up robot rules again
def handleDomainChange(url, base):
	print url + " " + base
	if findRootURL(url) != findRootURL(base):
		setUpRobot(url)
	else:
		return False

# Load a page as a string
def loadPage(url):
	# Increment stats to show a unique page has been considered
	stats[0] += 1
	
	# URLs with a root domain may point externally
	if findRootURL(url) == None:
		longURL = baseURL + url
	else:
		longURL = url
		handleDomainChange(longURL, baseURL)
	
	# Open only permitted pages. Catch errors and log the stats.
	if rp.can_fetch(useragent,longURL):
		try:
			page = urlopen(longURL)
		except HTTPError, e:
			print 'Error on page: ' + longURL
			print 'Error code: ', e.code
			stats[2] += 1
			return None
		except URLError, e:
			print 'Fatal! Connection Problems'
			print 'Reason: ', e.reason
			stats[2] += 1
			return None
		
		# Save URL to visited list so we don't go there again
		visited.append(url)
		return page.read()
	else:
		stats[1] += 1
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
				# Only add unseen pages to the frontier
				if True: #visited.count(url) == 0 and denied.count(url) == 0:
					matchDigits = re.search('\d+', url)
					priority = int(matchDigits.group())
					
					# The priority must be negated because heapq implements a min heap
					heapq.heappush(frontier, (-(priority),url))
		else:
			print " No content found on page"
			stats[3] += 1

setUpRobot(baseURL)
grabURLs(loadPage(startpage))

# Run until frontier is empty (no new pages to be visited)
while len(frontier) > 0:
	(priority, url) = heapq.heappop(frontier)
	if visited.count(url) == 0 and denied.count(url) == 0:
		grabURLs(loadPage(url))

print "Pages Visited:  " + str(len(visited))
print "Pages Denied:  " + str(len(denied))
print "Unique URLs found: " + str(stats[0])
print stats
