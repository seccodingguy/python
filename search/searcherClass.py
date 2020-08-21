import os
import re

class Searcher:
    def __init__(self, path, query, fileExt, hitOnly):
        self.path   = path

        if self.path[-1] != '/':
            self.path += '/'
        print(self.path)
        #self.path = self.path.replace('/', '\\')
        self.query  = query
        self.searched = {}
        self.fileExt = fileExt
        self.hitOnly = hitOnly

    def find(self):
        print("Inside searcher.find...")
        for root, dirs, files in os.walk( self.path ):
            for file in files:
                if re.match(r'.*?\.'+self.fileExt+'$', file) is not None:
                    #if root[-1] != '\\':
                    #    root += '\\'

                    if self.hitOnly:
                    #This is to do a simple hit count for the query
                        try:
                            f = open(root + '/' + file, 'rt')
                            txt = f.read()
                            f.close()
                            count = len( re.findall( self.query, txt ) )
                            if count > 0:
                                self.searched[root + '/' + file] = count
                        except IOError:
                            print('Error: can\'t find file or read data: ',root + '/' + file)
                        except:
                            print('Error: Unable to continue with Hit Only processing for file ',root+ '/' +file)
                    else:
                        try:
                            with open(root+ '/' +file, 'r') as searchfile:
                                for line in searchfile:
                                    if self.query in line:
                                        self.searched[root + file] = line
                        except IOError:
                            print('Error: can\'t find file or read data: ',root+ '/' +file)
                        except:
                            print('Error: Unable to continue with Line Search processing for file ',root+file)

    def getResults(self):
        return self.searched
