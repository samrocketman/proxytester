import urllib2, socket, sys
from lib.ThreadPool import *
from lib.SwitchParser import *
from lib.UniqueList import UniqueList
from time import sleep
from time import ctime

# If the proxy takes longer than 3 seconds to respond then it's too slow for broadband connections
# Dialup may need 5-10 seconds or longer
# set value to 1 for highest performance proxies (this will drastically decrease the amount of available proxies)
# set value to 3 for average performance proxies
# set value to 5 or more for slower proxies
# TIMEOUT is in seconds

TIMEOUT=3

# Enter URL which the proxies will attempt to connect to
# This can be any URL
# If you are attempting to access a particular restricted URL then use that
RESTRICTED_URL='http://www.google.com'

#Specify the number of threads (do not change unless you know what you're doing)
THREADS=4















#No need to edit beyond this point

#Create a new thread for each proxy to be checked
# the status will be True if the proxy is good for use!

def checkProxy(pip):
    status=-1
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req = urllib2.Request(RESTRICTED_URL)
        sock = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        print "Bad Proxy", pip
        status = False
    except Exception, detail:
        print "ERROR:", detail
        print "Bad Proxy", pip
        status = False
    if status == -1:
        print pip, "is working"
        status = True
    return (pip, status)

#handles the checkProxy class for threading
def handleResult(result):
#    print result[0], result[1]
    if result[1]:
        tested_proxies.append(result[0])

def waitTask(timeout):
#    print "timeout executed"
    sleep(timeout)

    

#Old threading method which hit max threads and threw errors.  plus bandwidth could not handle the unlimited amount of threads.
#class checkProxy(Thread):
#    def __init__(self,pip):
#        Thread.__init__(self)
#        self.pip = pip
#        self.status = None
#    def run(self):
#        try:
#            proxy_handler = urllib2.ProxyHandler({'http': self.pip})
#            opener = urllib2.build_opener(proxy_handler)
#            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#            urllib2.install_opener(opener)        
#            req = urllib2.Request(RESTRICTED_URL)
#            sock = urllib2.urlopen(req)
#        except urllib2.HTTPError, e:
#            print e
#            #print 'Error code: ', e.code
#            #print "Bad Proxy", self.pip
#            self.status = False
#        except Exception, detail:
#            print detail
#            #print "ERROR:", detail
#            #print "Bad Proxy", self.pip
#            self.status = False
#        if self.status == None:
#            print self.pip, "is working"
#            self.status = True

started = ctime()
socket.setdefaulttimeout(TIMEOUT)
pool = ThreadPool(THREADS)

TAB = "\t"
NEW_LINE = "\n"

# read the list of proxy IPs in proxyList
#proxyList = ['221.214.27.253:808'] # there are two sample proxy ip
f = open('proxylist.txt','r')
fileContents = f.read()
proxyList = fileContents.split(NEW_LINE)
f.close()


f = open('wpad.dat', 'w')
n = open('new_list.txt', 'w')
#write the wpad header
h = open('includes/wpad-head.js')
fileContents = h.read()
f.write(fileContents)
h.close()

# test the proxy list and generate a new list consisting of working proxies
firstline = False
tested_proxies = []
for line in proxyList:
    pool.queueTask(checkProxy, line, handleResult)

#This while loop is to account for an unknown bug in ThreadPool.py
i=0
while i < THREADS:
    pool.queueTask(waitTask, TIMEOUT + 2)
    i = i+1

pool.joinAll()

for item in tested_proxies:
    item=str(item)
    n.write(item + NEW_LINE)
    if not firstline:
        f.write('"' + item + '"')
        firstline = True
    else:
        f.write(',' + NEW_LINE + TAB + TAB + TAB + '"' + item + '"')
#        n.write(item + NEW_LINE)
#        if not firstline :
#            f.write('"' + item + '"')
#            firstline = True
#        else :
#            f.write(',' + NEW_LINE + TAB + TAB + TAB + '"' + item + '"')

#write the wpad footer
h = open('includes/wpad-foot.js')
fileContents = h.read()
f.write(fileContents)
h.close()

n.close()
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