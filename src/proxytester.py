#!/usr/bin/env python
'''
    Created Dec 1, 2009
    Main driver for application
    Author: Sam Gleske
'''


import urllib2
import socket
import sys
import os.path

from lib.ThreadPool import *
from lib.SwitchParser import *
from lib.UniqueList import UniqueList
from lib.GenerateWPAD import *
from time import sleep
from time import ctime
from sys import exit
from bisect import bisect_right

TAB = "\t"
NEW_LINE = "\n"
wpad=GenerateWPAD()

# Country lookup structs
tup = [] # split list of 'hash, countryID' goes here
numberlist = [] # inorder hash list goes here

""" make configuration adjustments based on given arguments """
config=SwitchParser(sys.argv)

print "Generate wpad.dat:", str(config.WPAD)
if config.Threads > 1:
    print "Multi-Threading: Enabled"
else:
    print "Multi-Threading: Disabled"
if config.excludeFile == None :
    print "Exclude certain proxies: False"
else:
    print "Exclude certain proxies: False"
print "Testing URL:", config.restrictedURL
print "Check proxy response against:",config.responseFile
print "Proxy Timeout:", str(config.Timeout)
print "Unique List:", str(config.unique)
if config.countryFilter == False :
  print "Country Filter: All"
else:
  print "Country Filter: "  + str(config.countryCode)
#remove duplicate file entries
config.fileList=UniqueList(config.fileList).unique

#test to make sure all files exist
for filename in config.fileList:
    if not os.path.isfile(filename):
        print "All files in your fileList must exist!" + " " + filename + " seems to not exist."
        config.syntaxErr()
    elif filename == config.outFile:
        print "One of your fileList files are the same as your outFile"
        config.syntaxErr()
if not config.quietMode :
    if os.path.isfile(config.outFile) :
        answer=raw_input("It appears your outFile already exists!" + NEW_LINE + "Do you want to overwrite (Y/N)?: ")
        if answer.upper() not in ('Y','YE','YES') :
            print "User aborted command!"
            exit()

#testing swich accuracy only
#print "config.outFile: " + config.outFile
#print "config.fileList: " + str(config.fileList)
#print "config.WPAD: " + str(config.WPAD)
#print "config.Threads: " + str(config.Threads)
#print "config.quietMode: " + str(config.quietMode)
#print "config.restrictedURL: " + config.restrictedURL
#print "config.Timeout: " + str(config.Timeout)
#print "config.unique:", str(config.unique)
#exit()

# the status will be True if the proxy is good for use!
def checkProxy(pip):
    status=-1
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req = urllib2.Request(config.restrictedURL)
        sock = urllib2.urlopen(req)
        if config.Response != None:
            response = sock.read();
            response = response.strip('\r')
            responseList = []
            responseList = response.split(NEW_LINE)
            for line in responseList :
                if line not in config.Response:
                    status = False
        if not status :
            print "ERROR: Response test failed"
            print "Bad Proxy", pip
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        print "Bad Proxy", pip
        status = False
    except Exception, detail:
        print "ERROR:", detail
        print "Bad Proxy", pip
        status = False
    finally:
        if status == -1:
            print pip, "is working"
            status = True
    return (pip, status)


# use this to load up the country file
# file format is iphash;code
# once loaded we can close the file and move on
def loadCountries():
  if not os.path.isfile("ipdb.txt"):
    print "ipdb not found."
    exit(1)
  # Open list
  print "Loading country file..."
  countryFile = open('ipdb.txt')

	# Tuple contains matched pairs of iphash and two letter country code.
	# Numberlist contains hashes at the indices that match indices of tuple.
	# The reason for this is bisect_right() can only take an array as a parameter and
	# I'm not sure how to unwind the tuple so that it will eat it.

	# Penalty : Double the memory usage. Whole of IPv4 space: ~120k entries * 16bit number
	# Short answer: No one cares.	
	
	# Two crappy hacks here:

	# How do we get get bisect_right() to work with tuples? Eh.
	# How do we get current line number while inputting from a file? :/

	#hack #2, can't figure out how to get line number - dumb 
  i = 0

  for line in countryFile:
    tup.append(line.split(";"))
    numberlist.append(int(tup[i][0])) # hack #2, ah well
    i = i + 1 # here we go...

  countryFile.close()
	
# ip -> iphash function
# requires ip as a string, gives ip hash int corresponding to db
def iphash(ip):
  iphash = ip.split(".")
  iphash = ((int(iphash[0])*256+int(iphash[1]))*256+int(iphash[2]))*256+int(iphash[3])
  return(iphash)
# hash -> country code
# takes a hash from hash calculator and looks it up in country table
# modified binary search for finding country code, uses bisect_right()
# looks up in log(n) rather than (n) (uses binary search) but instead of finding exact matches
# looks for previous (left value) for country code in table

def hashToState(hash):
	# Search list with bisect()
	nmin = 0
	nmax = len(numberlist)-1
	# derp -  hack #1 from above

	# index = bisect_right(tup,iphash,nmin,nmax)
	index = bisect_right(numberlist,hash,nmin,nmax)
	return tup[index-1][1]
	
#handles the checkProxy class for threading
def handleResult(result):
#    print result[0], result[1]
    if result[1]:
        tested_proxies.append(result[0])

def waitTask(timeout):
#    print "timeout executed"
    sleep(timeout)


started = ctime()
socket.setdefaulttimeout(config.Timeout)
pool = ThreadPool(config.Threads)

# read the list of proxy IPs in proxyList
proxyList=[]
for filepath in config.fileList:
        f=open(filepath, 'r')
        fileContents = f.read()
        contentsList = fileContents.split(NEW_LINE)
        f.close()
        for line in contentsList:
            proxyList.append(line)
if config.unique :
    proxyList=UniqueList(proxyList).unique

if config.WPAD:
    #test for wpad overwrite
    if not config.quietMode :
        if os.path.isfile('wpad.dat') :
            answer=raw_input("It appears your wpad.dat file already exists!" + NEW_LINE + "Do you want to overwrite (Y/N)?: ")
            if answer.upper() not in ('Y','YE','YES') :
                print "User aborted command!"
                exit()

    f = open('wpad.dat', 'w')
    
    #write the wpad header
    for line in wpad.head:
        f.write(line)

# filter proxies by country before we even start.
if config.countryFilter: # test for filter on
  loadCountries() # load 'em 
  newList = [] # need a place to put by country
  for line in proxyList: # take each proxy
    if line: # little defensive programming here...
      ip, port = line.split(":") # split ip:port
      if config.countryCode:
        countryTest = hashToState(iphash(ip))
        countryTest = countryTest.rstrip()
        if countryTest == config.countryCode: # if country is eq
          newList.append(line)
  proxyList = newList # just replace it outright
        


n = open(config.outFile, 'w')

# test the proxy list and generate a new list consisting of working proxies
firstline = False
tested_proxies = []

#Create a new thread for each proxy to be checked
for line in proxyList:
    if line not in config.excludeServers :
        pool.queueTask(checkProxy, line, handleResult)

#This while loop is to account for an unknown bug in ThreadPool.py
i=0
while i < config.Threads:
    pool.queueTask(waitTask, config.Timeout + 2)
    i = i+1

pool.joinAll()

for item in tested_proxies:
    item=str(item)
    n.write(item + NEW_LINE)
    if config.WPAD:
        if not firstline:
            f.write('"' + item + '"')
            firstline = True
        else:
            f.write(',' + NEW_LINE + TAB + TAB + TAB + '"' + item + '"')

#write the wpad footer
if config.WPAD:
    for line in wpad.foot:
        f.write(line)

n.close()
if config.WPAD:
    f.close()
ended = ctime()
print "Process Started:", started
print "Process Ended:", ended
tsplit=str(ended).split(" ")[3].split(":")
ended=int(tsplit[0]) * 3600 + int(tsplit[1]) * 60 + int(tsplit[2])
tsplit=str(started).split(" ")[3].split(":")
started=int(tsplit[0]) * 3600 + int(tsplit[1]) * 60 + int(tsplit[2])
secs=ended-started
#Print the runtime in # hrs # mins # secs
print "Runtime:",secs/3600,"hrs",secs/60 - secs/3600*60,"mins",60*(secs%60)/100,"secs",NEW_LINE
print "Please wait..."
# if user force exits the program then force kill all threads
pool.joinAll(False,False)
exit(0)
