#2.1
#GetVolumes has been revised
"""
FindPath has been revised
    - includes 'exit'/'quit' keyword and to check if path is file
    - screen clearing
    - takes string parameter to display currently set path
"""

import hashlib
import shutil
import os
import os.path
import pickle
import time

"""
Function to copy or move files from one directory to its destination

@mode - Mode sets whether moving or copying, allowed inputs: 'copied','moved'
@startpath - Directory to start in
@endpath - Directory to end in
"""
def CopyAndMove(mode,startpath,endpath):
    response = 'success'
    if os.path.isdir(startpath):            #startpath is a directory
        fileList = os.listdir(startpath)
        if not os.path.exists(endpath):     #endpath does not exist (create directory)
            os.mkdir(endpath)
            print( "CREATED DIRECTORY: "+endpath+'\n' )
    else:
        fileList = [startpath]

    for i in range(len(fileList)):      #iterate through directory and copy files
        start = startpath+'/'+fileList[i]
        try:
            if mode=='copied':
                shutil.copy2(start,endpath)
            elif mode=='moved':
                shutil.move(start,endpath)
            print( mode.capitalize()+' '+start )
        except:
            print( 'Error! '+start+' not '+mode+'!' )
            response = 'One or more files not '+mode
    return response

"""
Gets the date of the file and formats the date string

@path - String - the path of the file to get date of
"""
def GetDate(path):
    thetime = time.gmtime(os.path.getmtime(path)) #CURRENTLY SET TO MODIFICATION DATE
    dateYr = str(thetime.tm_year)[-2:]
    dateMon = str(thetime.tm_mon)
    dateDay = str(thetime.tm_mday)
    if thetime.tm_mon < 10:
        dateMon = '0'+dateMon
    if thetime.tm_mday<10:
        dateDay = '0'+dateDay
    dateString = dateYr+'-'+dateMon+'-'+dateDay
    return dateString

"""
Get the directory path that the user manually types in

@pathType - String - user's input path
"""
def GetManualPath(pathType): #pathType needs to be a string
    while True:
        path = raw_input(pathType+" path: ")
        if os.path.exists(path):
            break
        else:
            print( "That is not an existing directory path!" )
            UserChoice = raw_input("Do you want to create this directory?(y/n)")
            if UserChoice.lower() == 'y':
                os.mkdir(path)
            elif UserChoice.lower()== 'n':
                break
    return path

"""
The main function of MoveIt. Will copy/move the specified directory files into their
determined destinations

@mode - String - whether to copy or move files
@sort - String - How the files should be sorted into sub-directories in their destination
    format: *1/0 for primary dest* *1/0 for backup* *string for type* *optional: folder name*
    ex: '11date' = sort by date subfolders in primary & backup
    ex: '10one test' = sort by subfolder "test" in only primary
@source - String - the source path name
@primary - String - the primary destination path name
@backup - String - the backup destination path name
"""
def go ( mode, sort, source, primary, backup ):
    skip = 0
    response = "success"

    if backup == None and mode in [ 'copy2', 'move2' ]:
        print( "Back-Up destination path has not been defined!" )
        skip = 1

    if skip == 0:
        #SD Card is plugged in
        if os.path.exists( source ):
            #List files in directory
            sourceFiles = os.listdir( source )

            total = len( sourceFiles )
            #Number of times the transfer loop needs to execute
            task = 1
            if '2' in mode:
                total *= 2
                task = 2
            itemsdone = 0; success = 0; error = 0
            percent = ( float( itemsdone ) / float( total ) ) * 100

            keyword = "copied"
            if mode == "move1":
                keyword = "moved"

            Goprimary = primary
            try:
                Gobackup = backup
            except:
                pass

            #Only copy/move to primary
            if task == 1:
                base = Goprimary
            #Copy/move to both, start with backup
            elif task == 2:
                base = Gobackup

            for t in range( task ):
                subfolder = False
                #Second time on file transfer loop, move on to primary
                if task == 2 and t == 1:
                    base = Goprimary
                    #Switch keyword
                    if mode == "move2":
                        keyword = "moved"

                suffix = ''
                for item in sourceFiles:
                    Gosource = source + "/" + item


                    if task == 1 and sort[ t ] == '1':
                        subfolder = True
                    elif task == 2:
                        if t == 0 and sort[ 1 ] == '1':
                            subfolder = True
                        elif t == 1 and sort[ 0 ] == '1':
                            subfolder = True

                    #Current task loop requires files to be placed in subfolder
                    if subfolder:
                        if 'one' in sort:
                            folderName = sort[ sort.find( ' ' ) + 1: ]
                            suffix = "/" + folderName
                        elif 'date' in sort:
                            suffix = "/" + GetDate( Gosource )
                        #Create sub-directories if needed
                        if not os.path.exists( base + suffix ) and not os.path.isdir( base + suffix ):
                            os.mkdir( base + suffix )
                            print( "Directory: " + ( base + suffix ) + " created\n" )

                    #Does not transfer file if file already exists in destination
                    if os.path.exists( base + suffix + "/" + item ):
                        os.system( 'cls' )
                        print( base + suffix + " already exists! File not transferred" )
                        response = "One or more files not transferred"
                        error += 1

                    #object encountered is a directory
                    elif os.path.isdir( Gosource ):
                        try:
                            shutil.copytree( Gosource, base + suffix + "/" + item )
                            print( keyword.capitalize() + ": " + Gosource )
                            print( "To: " + ( base + suffix ) )
                            success += 1
                        except:
                            response = "One or more files not transferred"
                            error += 1

                    else:
                        try:
                            if "copy" in mode or ( mode == "move2" and t == 0 ):
                                    shutil.copy2( Gosource, base + suffix )
                            elif mode == "move1" or ( mode == "move2" and t == 1 ):
                                    shutil.move( Gosource, base + suffix )
                            os.system( "cls" )
                            print( keyword.capitalize() + ": " + Gosource )
                            print( "To: " + ( base + suffix ) )
                            success += 1

                        except:
                            print( "Error! " + Gosource + "/ not " + keyword + " to " + ( base + suffix ) + "!" )
                            response = "One or more files not transferred"
                            error += 1

                    itemsdone += 1
                    percent = (float(itemsdone)/float(total))*100
                    print
                    if success != 0:
                        print( str( success ) + "/" + str( total ) + " file(s) transferred" )
                    if error != 0:
                        print( str( error ) + " file(s) not transferred" )
                    print( "Overall progress: " + str( int( percent ) ) + "%\n" )
            print( response )
        else:
            print( "Source directory does not exist!" )

"""
Saves the user's MoveIt settings in a settings file

@fileName - String - the name of the settings file
@pathlist - list of the GUI settings, will be saved into file
"""
def Save(fileName,pathlist):
    pathFile = file(fileName,'wb')
    pickle.dump(pathlist,pathFile)
    print( "Settings saved" )


"""
Hash source and destination files to verify integrity

http://pythoncentral.io/hashing-files-with-python/

startpath - String - filepath of source file
endpath - String - filepath of destination file
"""
def verify_filehash(startpath, endpath):
    BLOCKSIZE = 65536
    source_hash = hashlib.md5()
    with open(startpath, 'rb') as source:
        buffer = source.read(BLOCKSIZE)
        while len(buffer) > 0:
            source_hash.update(buffer)
            buffer = source.read(BLOCKSIZE)
    # source_hash.hexdigest()
    buffer = b'' #clear buffer

    destination_hash = hashlib.md5()
    with open(endpath, 'rb') as destination:
        buffer = destination.read(BLOCKSIZE)
        while len(buffer) > 0:
            destination_hash.update(buffer)
            buffer = source.read(BLOCKSIZE)
    # destination_hash.hexdigest()

    if (source_hash.hexdigest() == destination_hash.hexdigest()):
        return True
    return False
