Created by Sam Gleske (sam.mxracer@gmail.com)
http://www.pages.drexel.edu/~sag47/
http://www.gleske.net/

---- WARNINGS AND INFO ----
DO NOT, I repeat, DO NOT log into web portals where financial or personal 
information is at risk using an anonymous/3rd party proxy.  It is possible 
that an anonymous proxy is set up to record all traffic and to mine 
usernames and passwords for websites.  Monitoring insecure authentication 
or cookies are just a few of many methods to achieve this.  I have set up 
some rules which will help minimize the effect of this but it is still 
recommended to disable this proxy whenever handling such information.  
This is not a flaw of this software or wpad.dat but more the nature of 
an anonymous proxy.

Public Proxies and the Law
According to to U.S. law, 18 U.S.C. § 1030 (Fraud and Related Activity in 
Connection with Computers) applies only when anyone who knowingly accesses 
a computer without authorization or has knowingly exceeds his authorized 
access on that computer. Because an opened proxy, by default, allows 
connections and use of the service by anyone in the WWW, its administrator 
has essentially authorized everyone to use the proxy.  Therefore browsing 
the web, via anonymous proxies, is not illegal.  This includes making a
set of open proxy lists public.

This software is geared towards advanced end users and security 
professionals.  By using this software you agree to the license.




---- PREREQUISITES ----
You should be comfortable installing and configuring software.

You should have a decent understanding of the internet and networks in 
general.

You should know what a proxy is.  If you don't know then read about it:
http://compnetworking.about.com/cs/proxyservers/a/proxyservers.htm

Python must be installed and correctly configured
Python 2.6 is recommended

On Windows you must add the directory where python.exe is located to your 
PATH environment variable...
1. Right click on My Computer and select properties
2. In Vista/7 click Advanced Settings
   In XP Select Advanced tab
3. Click Environment Variables
4. Under user variables click New... if PATH/Path does not exist
5. Varable name=PATH
6. Variable value=C:\Python26\
NOTE: if there are other directories you must separate them with a 
semicolon (;)
For example Variable value=C:\dir1\;C:\dir2\; and so on




---- INSTRUCTIONS ----
Go to a well known website and obtain a list of proxy servers such as 
http://www.samair.ru/proxy/
Get your list of anonymous proxies and put them in proxylist.txt.
A sample proxylist.txt is provided.
DO NOT delete proxylist.txt or else you won't be able to generate a 
wpad.dat file.

proxylist.txt should have the following format
server_name:port
server_ip:port

Windows:
proxytester.exe /? to view additional help documentation and usage
python proxytester.py /?

Linux:
./proxytester.py /?
to view additional help documentation and usage.

Mac/Other:
python proxytester.py /?
to view additional help documentation and usage.

I recommend that you run the Python script 5 or so times consecutively 
because some proxy servers only allow a limited number of connections so 
running the script multiple times helps to weed out those servers.  This 
increases the reliability of the proxy servers you are using and you 
won't ever get a connection timeout!




---- SOFTWARE RECOMMENDATION ----
Firefox                      http://www.getfirefox.com/
FoxyProxy Firefox Addon      http://foxyproxy.mozdev.org/

FoxyProxy howto:
1. Go to Tools > Add-ons > Extensions
2. Scroll down to FoxyProxy, click it, then click Options
3. Click Add New Proxy
4. Under Proxy Details select Automatic proxy configuration
5. Click the "..." and open your generated wpad.dat file
6. Click Test to ensure it works properly
7. Under General give it a name (like Random Proxy) and choose a pretty
   color
8. Click ok to save the proxy




---- FAQ/MISC HELP SECTION ----
What is wpad.dat?
wpad.dat is a Web Proxy Automatic Detection (WPAD) file.  Your browser 
selects a proxy based on the pre-defined rules specified in the wpad.dat 
file.  The language is JavaScript for wpad.dat.

What does the generated wpad.dat file do?
If you haven't changed anything it should:
1. Check the URL you're about to visit.  If it is part of the exclusion 
   rules then it will create a direct connection rather than a proxy.
2. If it will proxy then it will randomly choose a proxy server from the 
   list provided.
Every time you click a link your IP address will change as far as the web 
server is concerned there are many different computers connecting for 
different pages even though it is just you (If the server or protocol 
isn't in the pre-defined exclusion rules).

Pros/Cons of proxying using my wpad.dat method?
Pros:
Your IP address is constantly changing from the perspective of the web 
server making you impossible to track. There are pre-defined rules which 
help to protect your information if you accidently forget to turn off 
this proxy method while browsing websites where financial or personal 
information are at risk.

Cons:
Your browsing speed is slightly diminished because you are visiting 
websites via a proxy.
Your browsing habits and information are not guarunteed to be protected from the anonymous proxy.