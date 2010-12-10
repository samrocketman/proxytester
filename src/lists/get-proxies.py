#!/usr/bin/env python
'''
    Created Dec 9, 2010.
    Downloads a current list of anonymous proxies from Mr. Hinky Dink's proxy list.
    Use proxytester to test them.
    Author: Sam Gleske
'''
import urllib, re

def do_page(url):
    f = urllib.urlopen(url)
    html = f.read()
    #grab the full list of proxies (any type).
    pattern = r'<tr bgcolor="#[f8][f8]ff88".*\n<td>(.*)</td>\r\n<td>(.*)</td>\r\n<td>(.*)</td>'
    proxies = re.findall(pattern, html)
    return proxies

if __name__ == '__main__':
    #looking for High Anonymous and Anonymous proxies
    hits = []
    print "Fetching " + 'http://www.mrhinkydink.com/proxies.htm'
    hits.extend(do_page('http://www.mrhinkydink.com/proxies.htm'))
    for i in range(2, 16):
        url = 'http://www.mrhinkydink.com/proxies%d.htm' % i
        print "Fetching " + url
        hits.extend(do_page(url))
    print "Generating Proxy List..."
    fh = open('proxylists.txt', 'wb')
    for hit in hits:
        if 'Anonymous' in hit or 'High&nbsp;Anon' in hit :
            fh.write('%s:%s\n' % (hit[0], hit[1]) )
            # fh.write('%s:%s\t%s\n' % hit )
    fh.close()