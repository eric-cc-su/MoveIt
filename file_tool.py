#Author = eric-cc-su
#Tool created to manipulate files and directories

import shutil
import os
import os.path
import re
import time

"""
Function to specifically re-date files in format MM-DD-YY_####

@sourcepath - path of directory or file to rename
@mode - "replace" or "add" refers to how to rename files
"""
def redate(sourcepath, mode):
    if mode not in ['add','replace']:
        return "Not a proper mode"

    delimiter = '\\'
    if delimiter not in sourcepath and '/' in sourcepath:
        delimiter = '/'

    parent = prefix = sourcepath
    if os.path.isfile(sourcepath):
        parent = os.path.abspath(os.path.join(parent, os.pardir))
    parent = parent[ parent.rfind(delimiter) + 1: ]
    file_list = [ sourcepath[ sourcepath.rfind(delimiter) + 1: ] ]

    date_values = parent.split('-')
    date_string = date_values[1] + '-' + date_values[2] + '-' + date_values[0]

    if os.path.isdir(sourcepath):
        file_list = os.listdir(sourcepath)

    elif os.path.isfile(sourcepath):
        prefix = sourcepath[ :sourcepath.rfind(delimiter) ]

    else:
        print( "Bad path: " + sourcepath )
        return False

    for file in file_list:
        if file[:8] != date_string:
            suffix = date_string + '_' + file
            if mode == 'replace' and file[8] == '_':
                suffix = date_string + file[8:]
            os.rename( prefix + '\\' + file, prefix + '\\' + suffix )

    return True

"""
Scan directory tree and count all files

@path - path of directory to scan
"""
def scan_directory(path):
    file_count = 0
    if not os.path.isdir(path):
        return "Not a directory"

    dir_contents = os.listdir(path)
    for item in dir_contents:
        item_path = path + '\\' + item
        if os.path.isdir( item_path ):
            file_count += scan_directory( item_path )
        elif os.path.isfile( item_path ):
            file_count += 1
            print( item )

    return file_count


"""
Check if file name follows date format
File name should be in form: MM-DD-YY_filename
"""
def validate_date_string(file_name):
     date_string = re.compile('\d\d-\d\d-\d\d_')
     validate = re.match( date_string, file_name )
     if validate:
         return True
     return False

"""
Rename all of the files within a file tree to the date format specified
"""
def rename_tree_files(path):
    for dirpath, dirnames, filenames in os.walk(path):
        parent = dirpath[ dirpath.rfind('\\') + 1: ]
        date_values = parent.split('-')

        if len(date_values) == 3:
            date_string = date_values[1] + '-' + date_values[2] + '-' + date_values[0]

            #print( date_string + ": " )
            for file in filenames:
                mode = "replace"
                if len( file ) < 8 or not validate_date_string(file):
                    mode = "add"

                if not redate( dirpath + '\\' + file, mode ):
                    raise Exception("Failed to rename file")

#print( redate('C:\\Users\\sue3\\Documents\\MoveTest\\15-01-14', 'replace') )
#print( "\nFile count: " + str(scan_directory('C:\\Users\\sue3\\Documents\\MoveTest')) )
#print( redate('C:\\Users\\sue3\\Documents\\MoveTest\\15-01-14\\01-14-11_cc-wallpaper-desktop.png', 'replace'))

#print( validate_date_string('02-02-22_file') )
#rename_tree_files('C:\\Users\\sue3\\Documents\\MoveTest')