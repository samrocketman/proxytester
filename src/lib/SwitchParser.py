'''
    Created Dec 4, 2009
    Parses command line switches and takes appropriate action
    Author: Sam Gleske
'''
import re,sys,os.path
from sys import exit

class SwitchParser:
    outFile = None
    fileList = []
    excludeFile = None
    excludeServers = []
    WPAD = False
    Threads = 1
    quietMode = False
    restrictedURL = "http://www.google.com/"
    responseFile = None
    Response = None
    simulateConnect = False
    unique = False
    Timeout = 3
    NEW_LINE = "\n"
    TAB = "\t"
    #Regular Expressions for validation
    URL_EXPRESSION = "^(http:)"
    
        # LIST OF ARGUMENTS:
        # -e exclude list
        # -get restricted url to test
        # -mt to turn on multithreading
        # -o output file for the new proxy list
        # -q for suppressing prompts
        # -response for testing against a file from get
        # -sim simulate a working proxy list without connecting to the net
        # -t http timeout for proxy servers
        # -u generate a unique proxy server list with no duplicates
        # -w generate a wpad.dat file
        
    SWITCHES = ["E","GET","MT","O","Q","RESPONSE","SIM","T","U","W"]
    def __init__(self, commandLineArguments):
        arguments = []
        if len(commandLineArguments) <= 1:
            self.syntaxErr()
        
        """Clean the arguments up"""
        #the first argument is always the file name which we don't want so always exclude the first argument
        firstarg = 0
        for argument in commandLineArguments:
            if firstarg == 0:
                firstarg = firstarg + 1
                continue
            firstarg = firstarg + 1
            
            if argument != "" :
                argument = argument.strip()
            if argument != "":
                arguments.append(argument)
        
        """Check for documentation requests"""
        if "/?" in arguments or "--help" in arguments or "-help" in arguments :
            self.showhelp()
        elif "--license" in arguments or "-license" in arguments:
            self.showLicense()
        
        """Now look at all of the arguments to see if any match"""
        new_list=[]
        for i in range(len(arguments)):
            argument = arguments[i]
            
            if argument.find("-",0,1)  > -1:
                switch = argument.upper()[1:len(argument)]
                if self.SWITCHES.count(switch) > 0 :
                    if self.SWITCHES[0] == switch : #-e exclude list
                        try:
                            self.excludeFile = arguments[i+1] #The next argument is a file
                        except:
                            print "Possible missing argument."
                            self.syntaxErr()
                        if not os.path.isfile(self.excludeFile) :
                            print "Eclude file (-E) must exist!"
                            self.syntaxErr()
                        f=open(self.excludeFile, 'r')
                        fileContents = f.read()
                        contentsList = fileContents.split(self.NEW_LINE)
                        f.close()
                        for line in contentsList:
                            self.excludeServers.append(line)
                    if self.SWITCHES[1] == switch : #-get restricted url to test
                        try:
                            argument = arguments[i+1] #The next argument is an internet link
                        except:
                            print "Possible missing argument."
                            self.syntaxErr()
                        p = re.compile(self.URL_EXPRESSION)
                        if p.match(argument) == None :
                            print "Restricted URL (-get) must be followed by a http: link."
                            self.syntaxErr()
                        else:
                            self.restrictedURL = argument
                    if self.SWITCHES[2] == switch : #-mt to turn on multithreading
                        self.Threads=4
                    if self.SWITCHES[3] == switch : #-o output file for the new proxy list
                        try:
                            self.outFile = arguments[i+1] #The next argument is a file
                        except:
                            print "Possible missing argument."
                            self.syntaxErr()
                    if self.SWITCHES[4] == switch : #-q for suppressing prompts
                        self.quietMode = True
                    if self.SWITCHES[5] == switch : #-response for testing against a file from get
                        try:
                            self.responseFile = arguments[i+1] #The next argument is a file
                        except:
                            print "Possible missing argument."
                            self.syntaxErr()
                        if not os.path.isfile(self.responseFile) :
                            print "Response file (-RESPONSE) must exist!"
                            self.syntaxErr()
                        f = open(self.responseFile,'r')
                        fileContents = f.read()
                        fileContents = fileContents.strip('\r')
                        self.Response = fileContents.split(self.NEW_LINE)
                        f.close()
                    if self.SWITCHES[6] == switch : #-sim simulate a working proxy list without connecting to the net
                        self.simulateConnect=True
                    if self.SWITCHES[7] == switch : #-t http timeout for proxy servers
                        try:
                            argument=arguments[i+1] #following argument must be a number
                        except:
                            print "Possible missing argument."
                            self.syntaxErr()
                        p=re.compile("^([0-9]+)")
                        if p.match(argument) == None :
                            print "Timeout (-t) must be followed by a number."
                            self.syntaxErr()
                        else :
                            try :
                                argument=int(argument)
                            except :
                                print "Timeout argument must be an integer"
                                self.syntaxErr()
                            self.Timeout=argument
                    if self.SWITCHES[8] == switch : #-u generate a unique proxy server list with no duplicates
                        self.unique = True
                    if self.SWITCHES[9] == switch : #-w generate a wpad.dat file
                        self.WPAD = True
                else :
                    print "Invalid argument!"
                    self.syntaxErr()
            else :
                if argument != self.outFile and argument != self.restrictedURL and argument != str(self.Timeout) and argument != self.responseFile and argument != self.excludeFile:
                    new_list.append(argument)
        self.fileList = new_list
        # if self.outFile == None :
            # print "Output file not selected!"
            # self.syntaxErr()
    
    def showhelp(self) :
        print "Proxy Tester and WPAD.dat Generator v0.7"
        print "Proxy Tester takes a proxy list as input and then tests the addresses to       "
        print "ensure that they are still available for use. This program can also generate a "
        print "wpad.dat file which can be used by browsers. The wpad.dat file uses the working"
        print "list of proxies and each time the browser makes a request it will select a     "
        print "random proxy which makes the user virtually impossible to track."
        print ""
        print "Command Format:"
        print "PROXYTESTER [-GET url] [-MT] [-Q] [-T timeout] [-U] [-W] [-O outFile] fileList"
        print "PROXYTESTER [-SIM] [-RESPONSE inFile] [-E inFile] fileList"
        print ""
        print "  fileList" + self.TAB +      "1 or more file paths to a proxy list."
        print ""
        print "  /?" + self.TAB + self.TAB + "Shows this help dialog.  Also -help and --help work.         "
        print "  -GET" + self.TAB + self.TAB+"Specify a link to test the proxy server against.             "
        print self.TAB + self.TAB +          "If -GET url is not specified then this will get Google.com.  "
        print "  -E" + self.TAB + self.TAB + "Proxy list of proxy servers to exclude from testing. They    "
        print self.TAB + self.TAB +          "will be excluded if they're in this list even if they work.  "
        print "  inFile" + self.TAB +        "File path to plain text file to be read."
        print "  -license" + self.TAB +      "Display the MIT License. Also --license works."
        print "  -MT" + self.TAB + self.TAB+ "Multi-Threading support to process proxy lists faster.       "
        print "  -O" + self.TAB + self.TAB + "Outputs a proxy list of working proxies based on given       "
        print self.TAB + self.TAB +          "options."
        print "  outFile" + self.TAB +       "File path where output is written to a plain text file.      "
        print "  -Q" + self.TAB + self.TAB + "Suppress all overwrite prompts.                              "
        print "  -RESPONSE" + self.TAB +     "Read and compare the server response with the input file to  "
        print self.TAB + self.TAB +          "ensure the proxy server is working and not just showing any  "
        print self.TAB + self.TAB +          "HTML page."
        print "  -SIM" + self.TAB+ self.TAB+ "Simulate a working proxy without connecting to the internet. "
        print "  -T" + self.TAB + self.TAB + "Manually set the HTTP timeout for proxy servers.             "
        print "  timeout" + self.TAB +       "Timeout number in seconds. The shorter the timeout the faster"
        print self.TAB + self.TAB +          "the proxies must be to respond.                              "
        print self.TAB + self.TAB +          "    1 - or lower for high performance proxies                "
        print self.TAB + self.TAB +          "    3 - average performance proxies                          "
        print self.TAB + self.TAB +          "    5 - or more for slower proxies                           "
        print self.TAB + self.TAB +          "    Default is 3. Any range in between numbers work.         "
        print "  -U" + self.TAB + self.TAB + "Creates a unique list of proxy servers with no duplicates.   "
        print "  url" + self.TAB + self.TAB +"Internet URL to test for retrieval by the proxy server. This "
        print self.TAB + self.TAB +          "This is usually a restricted URL that is being blocked.      "
        print self.TAB + self.TAB +          "If -GET url is not specified then this will get Google.com.  "
        print "  -W" + self.TAB + self.TAB + "Generates a wpad.dat file.                                   "
        print ""
        print "Proxy list:"
        print "  A proxy list is a plain text file. In the proxy list each new line must      "
        print "  contain a single server with the following format.                           "
        print "  server:port"
        print ""
        print "Command examples:"
        print "  Test proxy servers and generate a new list (Minimum arguments):              "
        print self.TAB +           "proxytester -o new_proxy_list.txt proxylist1.txt                       "
        print "  Test proxy servers, generate a new list, and excluding testing some servers: "
        print self.TAB +           "proxytester proxylist1.txt -e exclude.txt -o new_proxy_list.txt        "
        print "  Test proxy servers against a response to ensure that they really work:       "
        print self.TAB +           "proxytester -get http://www.example.com/proxytest.html -response proxyt"
        print self.TAB +           "est.html -o new_proxy_list.txt proxylist1.txt"
        print "  Generate a wpad.dat file from a proxy list without testing proxies:          "
        print self.TAB +           "proxytester -sim -w proxylist1.txt                                     "
        print "  Generate excludes file from working proxies and non-working proxies:         "
        print self.TAB +           "proxytester -mt -u -o new_list.txt proxylist1.txt                      "
        print self.TAB +           "proxytester -mt -sim -e new_list.txt -o exclude.txt proxylist1.txt     "
        print ""
        print "The -RESPONSE switch is normally used with the -GET switch but not always.     "
        print "Sometimes a user wishes to test if the proxy is truly a transparent proxy so   "
        print "the -RESPONSE switch was devised to ensure this.  Just create your own dummy   "
        print "html page and upload it to your own web server.  Then call that page using the "
        print "-GET switch and check it against a local copy of the same html page using the  "
        print "-RESPONSE switch. This is the best method for testing anonymous proxies!       "
        print ""
        print "Options don't have to be in any particular order as long as the command format "
        print "is followed. Refer to the Command Format to see what switches are followed by  "
        print "arguments."
        print ""
        print "Created by Sam Gleske (sam.mxracer@gmail.com)"
        print "Copyright (c) 2009 Proxy Tester Project, Sam Gleske"
        print "Licensed under the MIT License (see command line options for viewing)"
        print "Project website:"
        print "http://sourceforge.net/projects/proxytest"
        exit()
    def syntaxErr(self) :
        print "The syntax of the command is incorrect.  Try COMMAND /? or COMMAND --license."
        exit()
    def showLicense(self) :
        print 'MIT Open Source License'
        print ''
        print 'Copyright (c) 2009 Proxy Tester Project, Sam Gleske'
        print ''
        print 'Permission is hereby granted, free of charge, to any person obtaining a copy   '
        print 'of this software and associated documentation files (the "Software"), to deal  '
        print 'in the Software without restriction, including without limitation the rights   '
        print 'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      '
        print 'copies of the Software, and to permit persons to whom the Software is          '
        print 'furnished to do so, subject to the following conditions:'
        print ''
        print 'The above copyright notice and this permission notice shall be included in     '
        print 'all copies or substantial portions of the Software.                            '
        print ''
        print 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     '
        print 'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       '
        print 'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    '
        print 'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         '
        print 'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  '
        print 'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN      '
        print 'THE SOFTWARE.'
        exit()
