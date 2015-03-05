#!/usr/bin/env python3
#
# Author = eric-cc-su
# Tool created to manipulate files and directories
# Requires Python 3 due to stupid nature of input() functions between 2 & 3

import os
import os.path
import re
import sys

clear_console = 'clear'

if 'win' in str(sys.platform):
    clear_console = 'cls'

#return proper delimiter based on pathname given
def check_delimiter(path):
    delimiter = '/'
    if '/' not in path and '\\' in path:
        delimiter = '\\'
    return delimiter

"""
Function to specifically re-date files in format MM-DD-YY_####

@sourcepath - path of directory or file to rename
@mode - "replace" or "add" refers to how to rename files
"""


def redate(sourcepath, mode):
    if mode not in ['add', 'replace']:
        return "Not a proper mode"

    delimiter = check_delimiter(sourcepath)

    parent = prefix = sourcepath
    if os.path.isfile(sourcepath):
        parent = os.path.abspath(os.path.join(parent, os.pardir))
    parent = parent[parent.rfind(delimiter) + 1:]
    file_list = [sourcepath[sourcepath.rfind(delimiter) + 1:]]

    date_values = parent.split('-')
    try:
        date_string = date_values[1] + '-' + date_values[2] + '-' + \
                      date_values[0]
    except:
        print("Bad path: " + sourcepath)
        return False

    if os.path.isdir(sourcepath):
        file_list = os.listdir(sourcepath)

    elif os.path.isfile(sourcepath):
        prefix = sourcepath[:sourcepath.rfind(delimiter)]

    else:
        print("Bad path: " + sourcepath)
        return False

    for file in file_list:
        if file[:8] != date_string:
            suffix = date_string + '_' + file
            if mode == 'replace' and file[8] == '_':
                suffix = date_string + file[8:]
            os.rename(prefix + delimiter + file, prefix + delimiter + suffix)

    return True


"""
Scan directory tree and count all files

@path - path of directory to scan
"""


def scan_directory(path):
    file_count = 0
    if not os.path.isdir(path):
        return "Not a directory"

    delimiter = check_delimiter(path)

    dir_contents = os.listdir(path)
    for item in dir_contents:
        item_path = path + delimiter + item
        if os.path.isdir(item_path):
            file_count += scan_directory(item_path)
        elif os.path.isfile(item_path):
            file_count += 1
            print(item)

    return file_count


"""
Check if file name follows date format
File name should be in form: MM-DD-YY_filename
"""


def validate_date_string(file_name):
    date_string = re.compile('\d\d-\d\d-\d\d_')
    validate = re.match(date_string, file_name)
    if validate:
        return True
    return False


#Rename all of the files within a file tree to the date format specified above

def rename_tree_files(path):
    delimiter = check_delimiter(path)

    for dirpath, dirnames, filenames in os.walk(path):
        parent = dirpath[dirpath.rfind(delimiter) + 1:]
        date_values = parent.split('-')

        if len(date_values) == 3:
            for file in filenames:
                mode_input = "replace"
                if len(file) < 8 or not validate_date_string(file):
                    mode_input = "add"

                if not redate(dirpath + delimiter + file, mode_input):
                    raise Exception("Failed to rename file")
    return True


# print( redate('C:\\Users\\sue3\\Documents\\MoveTest\\15-01-14', 'replace') )
#print("\nFile count: " + str(scan_directory('/home/eric/Documents/MoveTest')))
#print(redate('/home/eric/Documents/MoveTest', 'replace'))

#print( validate_date_string('02-02-22_file') )
#print( rename_tree_files('/home/eric/Documents/MoveTest') )

sourcepath = ''
mode = 'replace'

while True:
    os.system(clear_console)
    print('******************************************************************')
    print('*                            File Tool                           *')
    print('*                            Eric Su                             *')
    print('*                            %s' % str(sys.platform))
    print('*                                                                *')
    print('* 1. Define source path/file name                                *')
    print('* 2. Scan directory                                              *')
    print('* 3. Validate file name                                          *')
    print('* 4. View source path                                            *')
    print('*                                                                *')
    print('* 8. Rename files in valid tree                                  *')
    print('* 9. Rename single directory/file                                *')
    print('* 0. Exit                                                        *')
    print('******************************************************************')

    user = str(input('Input: '))
    if user == '1':
        sourcepath = str(input('Please input source path or file name: '))

    elif user == '2':
        print(scan_directory(sourcepath))
        input('Press any key to continue...')

    elif user == '3':
        print(validate_date_string(sourcepath))
        input('Press any key to continue...')

    elif user == '4':
        print(sourcepath)
        input('Press any key to continue...')

    elif user == '8':
        os.system(clear_console)
        while True:
            verify = input('This will search through the entire file tree and '
                           'rename every file to fit date format. Are you sure'
                           ' you want to continue?(y/n) ')
            if verify == 'y':
                print(rename_tree_files(sourcepath))
                input('Press any key to continue...')
                break
            elif verify == 'n':
                break

    elif user == '9':
        print(redate(sourcepath, mode))
        input('Press any key to continue...')

    elif user == '0' or user == 'exit':
        break