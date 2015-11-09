# -*- coding: UTF-8 -*-

import sys
from searcherClass import Searcher

def showMenu():
        print 'Usage phpPackageFinder arg1 arg2 arg3 arg4'
        print '     arg1 = path to directory to search'
        print '     arg2 = search string'
        print '     arg3 = file extension'
        print '     arg4 = hit count only, meaning only show number of hits of the search string in the file (True or False)'
        print ' '
        print 'Example: phpPackageFinder /home/somename/Documents/ testQuery txt True'
        print ' '
        print 'For the query string, use a single quote for a multiple word phrase.'

def performSearch(searchObj):
    print 'Search started...'
    Search.find()

    results = Search.getResults()

    print 'Found ', len(results), ' files:'

    print 'Search ended.'

    for file, count in results.items():
        #after search @Package, then conduct another search using the filename
        #to get the version number of the Package
        with open(file, 'r') as searchfile:
            for line in searchfile:
                if search in line:
                    print line
                if version in line:
                    print line




#path = 'c:\\temp\\'
path = '/someName/Users/'
search = 'security'
fileExt = 'txt'
hitOnly = True
noVars = True

if __name__ == '__main__':

    if len(sys.argv) != 5 and noVars == False:
        showMenu()
    elif len(sys.argv) == 5:
        Search = Searcher(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        performSearch(Search)
    else:
        Search = Searcher(path, search, fileExt, hitOnly)
        performSearch(Search)



