import os
import re

class FileTypeCounter:
    def __init__(self, path, fileExt):
        self.path   = path

        #if self.path[-1] != '/':
        #    self.path += '/'

        #self.path = self.path.replace('/', '\\')
        self.searched = {}
        self.fileExt = fileExt
        self.count = 0

    def find(self):
        for root, dirs, files in os.walk( self.path ):
            for file in files:
                if re.match(r'.*?\.'+self.fileExt+'$', file) is not None:
                    self.searched[root + file] = self.count + 1

    def getResults(self):
        return self.searched
