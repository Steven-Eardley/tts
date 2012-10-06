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

# Variable for statistics: [unique, visited, denied, error, noContent, external]
stats = [0,0,0,0,0,0]

baseURL = "http://ir.inf.ed.ac.uk/tts/A1/0934142/"
startpage = "0934142.html"

# Find the top level directory given a URL
def findRootURL(url):
	matchRoot = re.match('.*?[//][\w.\w]+/', url)
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
	print url
	if findRootURL(url) != findRootURL(base):
		setUpRobot(url)
		# Change the base URL to that of the new page's directory (not required for this assignment)
		# baseURL = findDirectoryURL(url)
		return True
	else:
		return False

# Load a page as a string
def loadPage(url):
	
	# Increment stats to show a unique page has been considered
	stats[0] += 1
	
	# Full URLs may point externally, short URLs need to have the base added.
	if findRootURL(url) == None:
		longURL = baseURL + url
	else:
		longURL = url
		print url
		# If the URL points outside the domain, don't follow it for this assignment
		if handleDomainChange(longURL, baseURL):
			stats[5] += 1
			return None
		
	# Open only permitted pages. Catch errors and log the stats.
	if rp.can_fetch(useragent, longURL):
		
		# Save URL to visited list so we don't go there again
		visited.append(url)
		
		try:
			page = urlopen(longURL)
			stats[1] += 1
		except HTTPError, e:
			print 'Error on page: ' + longURL
			print 'Error code: ', e.code
			stats[3] += 1
			return None
		except URLError, e:
			print 'Fatal! Connection Problems'
			print 'Reason: ', e.reason
			stats[3] += 1
			return None

		return page.read()
	else:
		stats[2] += 1
		denied.append(url)
		return None

# Parse URLs between CONTENT comments on a page
def grabURLs(page):
	if page != None:
		matchContent = re.search('<!-- CONTENT -->.*<!-- /CONTENT -->', page, re.DOTALL)
		if True: # matchContent:
			#content = matchContent.group()
			content = page
			# Once the content region has been identified, extract the URLs
			urls = re.findall('(?<=a href=")\S*\.[A-za-z]+', content)
			for url in urls:
				matchDigits = re.search('\d+', url)
				priority = int(matchDigits.group())
				
				# Only add unseen pages to the frontier
				if visited.count(url) == 0 and denied.count(url) == 0 and frontier.count((-(priority) , url)) == 0:
					
					# Add to queue. The priority must be negated because heapq implements a min heap
					heapq.heappush(frontier, (-(priority), url))
		else:
			
			# Log the number of pages without content
			stats[4] += 1

print findRootURL("http://ir.inf.ed.ac.uk/tts/A1/0934142/0934142.html")
print findRootURL("ir.inf.ed.ac.uk/tts/A1/0934142/0934142.html")
print findRootURL("0934142.html")
print findRootURL("private/0934142.html")
print findRootURL("www.google.com")
print findRootURL("http://www.google.com/test.html")

setUpRobot(baseURL)
grabURLs(loadPage(startpage))

# Run until frontier is empty (no new pages to be visited)
while len(frontier) > 0:
	#print len(frontier)
	(priority, url) = heapq.heappop(frontier)
	grabURLs(loadPage(url))
		
print "Unique URLs found: " + str(stats[0])
print "Pages Visited:  " + str(stats[1])
print "Pages Denied:  " + str(stats[2])
print "Pages With errors: " + str(stats[3])
print "Pages with no content: " + str(stats[4])
print "External pages detected: " + str(stats[5])
