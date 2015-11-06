# -*- coding: UTF-8 -*-

import sys
from fileTypeCounterClass import FileTypeCounter

#path = 'c:\\temp\\'
path = '/somelocation/'
fileExt = 'exe'

if __name__ == '__main__':

    if len(sys.argv) == 3:
        Search = FileTypeCounter(sys.argv[1], sys.argv[2])
    else:
        Search = FileTypeCounter(path, fileExt)

    Search.find()

    results = Search.getResults()

    print 'Found ', len(results), ' files:'

    for file, count in results.items():
        print 'File: ', file, ' Found entries:' , count
