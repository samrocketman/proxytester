Created by Sam Gleske (sam.mxracer@gmail.com)
Copyright (c) 2009 Proxy Tester Project, Sam Gleske
Licensed under the MIT License (see command line options for viewing)
Project website:
http://sourceforge.net/projects/proxytest
http://www.pages.drexel.edu/~sag47/
http://www.gleske.net/

Need help?  Check out the wiki...
http://sourceforge.net/apps/mediawiki/proxytest/
You'll find all the information you need about proxytester and more.

Still need help?  Ask in the forums...
http://sourceforge.net/projects/proxytest/forums/



---- INSTRUCTIONS ----
Go to a well known website and obtain a list of proxy servers such as 
http://www.mrhinkydink.com/proxies.htm
Get your list of anonymous proxies and put them in proxylist.txt.
A sample proxylist.txt is provided.

proxylist.txt should have the following format
server_name:port
and/or
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