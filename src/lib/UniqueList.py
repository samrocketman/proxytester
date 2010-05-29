'''
    Created Dec 3, 2009
    Compare lists and only append unique values
    Author: Sam Gleske
'''

class UniqueList:
    unique = []
    def __init__(self, someList = []):
        unique = []
        for line in someList:
            if line not in unique:
                if line != "" or line != None:
                    unique.append(line)
        self.unique = unique