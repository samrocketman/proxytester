class SwitchParser:
    arg_error="UniqueList.py [-o outFile] fileList\nWhere outFile is a file path and fileList is 1 or more file paths for input."
    outFile = None
    fileList = []
    """ -o outFileName """
    SWITCHES = ["O"]
    def __init__(self, commandLineArguments):
        arguments = []
        if len(commandLineArguments) == 1:
            print "Error! No file arguments!"
            print self.arg_error
            exit()
        
        """Clean the arguments up"""
        for argument in commandLineArguments:
            if argument != "" :
                argument = argument.strip()
            if argument != "" and argument != "UniqueList.py":
                arguments.append(argument)
        
        """Now look at all of the arguments to see if any match"""
        new_list=[]
        for i in range(len(arguments)):
            argument = arguments[i]
            
            #display help documentation
            if "/?" in argument :
                self.showhelp()
            elif "--help" in argument :
                self.showhelp()
            elif "-help" in argument :
                self.showhelp()
            
            if argument.find("-",0,1)  > -1 and self.outFile == None:
                switch = argument.upper()[1:2]
                if self.SWITCHES.count(switch) > 0 :
                    if self.SWITCHES[0] == switch: #The next argument is a file
                        self.outFile = arguments[i+1]
                else:
                    print "Invalid argument!"
                    print self.arg_error
                    exit()
            elif argument.find("-",0,1)  > -1:
                print ""
                exit()
            else:
                if argument != self.outFile:
                    new_list.append(argument)
        self.fileList = new_list
        if self.outFile == None:
            print "Output file not selected!"
            print self.arg_error
            exit()
    
    def showhelp(self):
        print "Proxy Tester takes a proxy list as input and then tests the addresses to       "
        print "ensure that they are still available for use. This program can also generate a "
        print "wpad.dat file which can be used by browsers. The wpad.dat file uses the working"
        print "list of proxies and each time the browser makes a request it will select a     "
        print "random proxy which makes the user virtually impossible to track."
        print ""
        print "PROXYTESTER [-MT] [-U] [-W] [-GET url] [-T timeout] [-O outFile] fileList"
        print ""
        print "  fileList" + self.TAB +      "1 or more file paths to files containing a proxy list. In the"
        print self.TAB + self.TAB +          "proxy list each new line must contain a single server with   "
        print self.TAB + self.TAB +          "the following format..."
        print self.TAB + self.TAB +          "server:port"
        print ""
        print "  /?" + self.TAB + self.TAB + "Shows this help dialog.  Also -help and --help work."
        print "  -GET" + self.TAB + self.TAB+"Specify a link to test the proxy server against."
        print self.TAB + self.TAB +          "If -GET url is not specified then this will get Google.com."
        print "  -MT" + self.TAB + self.TAB+ "Multi-Threading support to process proxy lists faster."
        print "  -T" + self.TAB + self.TAB + ""
        print "  timeout" + self.TAB +       "Timeout number in seconds. The shorter the timeout the faster"
        print self.TAB + self.TAB +          "the proxies must be to respond."
        print self.TAB + self.TAB +          "    1 - or lower for high performance proxies"
        print self.TAB + self.TAB +          "    3 - average performance proxies"
        print self.TAB + self.TAB +          "    5 - or more for slower proxies"
        print self.TAB + self.TAB +          "    Default is 3. Any range in between numbers work."
        print "  -U" + self.TAB + self.TAB + "Creates a unique list of proxy servers with no duplicates.   "
        print "  url" + self.TAB + self.TAB +"Internet URL to test for retrieval by the proxy server. This "
        print self.TAB + self.TAB +          "This is usually a restricted URL that is being blocked."
        print self.TAB + self.TAB +          "If -GET url is not specified then this will get Google.com."
        print "  -W" + self.TAB + self.TAB + "Generates a wpad.dat file."
        print ""
        print "Created by Sam Gleske (sam.mxracer@gmail.com)"
        print "Copyright (c) 2009 Proxy Tester Project, Sam Gleske"
        print "Licensed under the MIT License (see command line options for viewing)"
        print "Project website:"
        print "http://sourceforge.net/projects/proxytest"
        exit()
    def syntaxErr(self):
        print "The syntax of the command is incorrect.  Try COMMAND /?."
        exit()
    def showLicense(self):
        print "MIT Open Source License"
        print ""
        print "Copyright (c) 2009 Proxy Tester Project, Sam Gleske"
        print ""
        print "Permission is hereby granted, free of charge, to any person obtaining a copy   "
        print "of this software and associated documentation files (the \"Software\"), to deal  "
        print "in the Software without restriction, including without limitation the rights   "
        print "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      "
        print "copies of the Software, and to permit persons to whom the Software is          "
        print "furnished to do so, subject to the following conditions:"
        print ""
        print "The above copyright notice and this permission notice shall be included in"
        print "all copies or substantial portions of the Software."
        print ""
        print "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     "
        print "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       "
        print "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    "
        print "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         "
        print "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  "
        print "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN      "
        print "THE SOFTWARE."
        