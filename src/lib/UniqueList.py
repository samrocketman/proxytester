#Compare two lists and only append unique values
#from json.decoder import uni
import sys, os.path

NEW_LINE="\n"

# if UniqueList.py is launched from the command line and not used as a library
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

class UniqueList:
    unique = []
    def __init__(self, someList = []):
        if len(someList) == 0:
            return False
        unique = []
        for line in someList:
            if line not in unique:
                if line != "" or line != None:
                    unique.append(line)
        self.unique = unique

# if UniqueList.py is launched from the command line and not used as a library
if __name__ == "__main__":
    files=SwitchParser(sys.argv)
    files.fileList=UniqueList(files.fileList).unique
    #test to make sure all files exist
    if os.path.isfile(files.outFile) :
        answer=raw_input("It appears your outFile already exists!" + NEW_LINE + "Do you want to overwrite (Y/N)?: ")
        if answer.upper() not in ('Y','YE','YES') :
            print "User aborted command!"
            exit()
    for filename in files.fileList:
        if not os.path.isfile(filename):
            print "All files in you fileList must exist!"
            print files.arg_error
            exit()
        elif filename == files.outFile:
            print "One of your fileList files are the same as your outFile"
            print files.arg_error

    someList = []
    for filepath in files.fileList:
        f=open(filepath, 'r')
        fileContents = f.read()
        contentsList = fileContents.split(NEW_LINE)
        f.close()
        for line in contentsList:
            someList.append(line)
        
    f=open(files.outFile,'w')
    someList=UniqueList(someList).unique
    for line in someList:
        if line != "":
            f.write(line + NEW_LINE)
    f.close()
    print "Done."