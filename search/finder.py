# -*- coding: UTF-8 -*-

import sys
import csv
import os.path
from searcherClass import Searcher

def showMenu():
        print('Usage phpPackageFinder arg1 arg2 arg3 arg4')
        print('     arg1 = path to directory to search')
        print('     arg2 = search string')
        print('     arg3 = file extension')
        print('     arg4 = hit count only, meaning only show number of hits of the search string in the file (True or False)')
        print(' ')
        print('Example: phpPackageFinder /home/somename/Documents/ testQuery txt True')
        print(' ')
        print('For the query string, use a single quote for a multiple word phrase.')

#path = 'c:\\temp\\'
path = '/someName/Users/'
search = 'security'
fileExt = 'txt'
hitOnly = True
noVars = False
searchForVersion = False
my_list = []
fieldNames = ['file','fine','fineno']

def csv_dict_writer(csv_file,csv_columns,dict_data):
    try:
        data_file = open(csv_file, 'w', newline='')
        obj = csv.DictWriter(data_file, fieldnames=fieldNames)
        obj.writeheader()
        data_file.close()

        csv_file = open(csv_file,'w',newline='')
        obj = csv.writer(csv_file)

        for data in dict_data:
            obj.writerow(data)

    except IOError as strerror:
        print("I/O error: {1}".format(strerror))
    except:
        print("Error: {1}".format(Exception))
    finally:
        csv_file.close()

    return

def performSearch(searchObj):
    print('Search started...')
    Search.find()
    version = '@version'
    
    results = Search.getResults()

    print('Found ', len(results), ' files:')

    print('Search ended.')

    my_list.append(fieldNames)
    
    for file, count in results.items():
        #after search @Package, then conduct another search using the filename
        #to get the version number of the Package
        counter = 0
        if os.path.exists(path):
            try:
                with open(file, 'r') as searchfile:
                    for line in searchfile:
                        counter = counter + 1
                        if search in line:
                            #print('File:', file, 'Line:', line, 'Line No:', counter)
                            #inner_dict=[file.translate(None, '\t\n;'), line.translate(None,'\t\n;'), counter]
                            inner_dict=[file, line, str(counter)]
                            my_list.append(inner_dict)
                            #my_list.append(line)
                        if searchForVersion == True and version in line:
                            print('File:', file, 'Line:', line, 'Line No:', counter)
            except FileNotFoundError:
                print("Unable to find file",file)
            finally:
                print("Moving on to next file.")
    
    print(my_list)
    csv_dict_writer('dict_output.csv',fieldNames,my_list)

#print 'File: ', file, ' Found entries:' , count


if __name__ == '__main__':

    print('Number of args: ', len(sys.argv))
    if len(sys.argv) < 3:
        showMenu()
    #elif len(sys.argv) == 6:
    else:
        print('Inside sys.argv...')
        path = sys.argv[1]
        search = sys.argv[2]
        fileExt = sys.argv[3]
        if len(sys.argv) > 4:
            hitOnly = sys.argv[4]
        else:
            hitOnly = False
        #hitOnly = sys.argv[4]
        searchForVersion = True #sys.argv[5]
        Search = Searcher(path, search, fileExt, hitOnly)
        performSearch(Search)
    #else:
    #    print('Inside else...')
    #    Search = Searcher(path, search, fileExt, hitOnly)
    #    performSearch(Search)



