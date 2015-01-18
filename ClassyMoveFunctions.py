#2.1
#GetVolumes has been revised
"""
FindPath has been revised
    - includes 'exit'/'quit' keyword and to check if path is file
    - screen clearing
    - takes string parameter to display currently set path
"""

import shutil
import os
import os.path
import pickle
import string
import subprocess
import time
from ctypes import windll

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
        for i in range(len(fileList)):      #iterate through directory and copy files
            try:
                if mode=='copied':
                    shutil.copy2(startpath+'/'+fileList[i],endpath)
                elif mode=='moved':
                    shutil.move(startpath+'/'+fileList[i],endpath)
                print( mode.capitalize()+' '+startpath+'/'+fileList[i] )
            except:
                print( 'Error! '+startpath+'/'+fileList[i]+' not '+mode+'!' )
                response = 'One or more files not '+mode
    else:
        try:
            if mode=='copied':
                shutil.copy2(startpath,endpath)
            elif mode=='moved':
                shutil.move(startpath,endpath)
            print( mode.capitalize()+' '+startpath+' to '+endpath )
        except:
            print( 'Error! '+startpath+'/'+' not '+mode+'!' )
            response = 'One or more files not '+mode 
    return response
    
"""
Function to present user with a way to select a directory path

@current - a string to show the current set path
"""
def FindPath(current): 
    os.system('cls')
    print( "Current "+current )
    print
    skip = 0
    ShowVolumes()
    print
    startpath = ''
    while startpath in ['',':/']:
        startpath = raw_input("Drive Label: ").upper()+':/'
        if startpath == ':/':
            choice = raw_input("Do you want to set the path as blank? (y/n)")   
            if choice == 'y':                                                       #will set path as blank and exit
                startpath = ''
                break
    if startpath.lower().strip(':/') in ['exit','quit']:
            skip = 1;
    print 
    while startpath not in [':/','']  and skip == 0:
        os.system('cls')
        print( "Current "+current )
        print( "Path being set: "+startpath )
        print
        for i in range(len(os.listdir(startpath))):
                print( os.listdir(startpath)[i] )
        if len(os.listdir(startpath))==0:
            break
        else:
            print
            path = raw_input("path (press Enter to mark current directory as path): ")
            print
            
            if path in ['exit','quit']:
                check = raw_input("Do you want to terminate the directory search process?(y/n)")
                if check.lower() == 'y':
                    skip = 1;
                    break
                else:
                    pass

            if path not in os.listdir(startpath) and path!='':
                print
                print( "That is not an existing directory path!" )
                UserChoice = raw_input("Do you want to create this directory?(y/n)")
                if UserChoice.lower() == 'y':
                    os.mkdir(startpath+path)
                    startpath += path
                    break
                elif UserChoice.lower()== 'n':
                    continue
                continue
            elif os.path.isfile(startpath+path) or len(os.listdir(startpath+path))==0:
                startpath+=path
                break
            elif path in ['']:
                if startpath[-1]=='/' and len(startpath)>3:
                    startpath=startpath[:-1]
                break
            else:
                path+='/'
                startpath+=path
    if startpath == ':/':
        startpath = ''
    os.system('cls')
    if skip == 0:
        print( 'Path: '+startpath )
        print
        return startpath
    else:
        print( 'Path definition process terminated' )
        return None

"""
Gets the date of the file and formats the date string

@path - String - the path of the file to get date of
"""
def GetDate(path):                                  
    thetime = time.gmtime(os.path.getmtime(path)) #CURRENTLY SET TO MODIFICATION DATE
    dateYr = str(thetime.tm_year)[-2:]
    if thetime.tm_mon < 10:
        dateMon = '0'+str(thetime.tm_mon)
    else:
        dateMon = str(thetime.tm_mon)

    if thetime.tm_mday<10:
        dateDay = '0'+str(thetime.tm_mday)
    else:
        dateDay = str(thetime.tm_mday)
    dateString = dateYr+'-'+dateMon+'-'+dateDay
    return dateString

"""
Get the directory path that the user manually types in

@pathType - String - user's input path
"""
def GetManualPath(pathType): #pathType needs to be a string
    while 1==1:
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
Gets the storage devices that are plugged into the computer
"""
def GetVolumes():
    drives = []                                                 #list of all volumes
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    driveList = []                                              #list of usable drive types
    for drive in drives:                                        #Discovers drive types
        if not drive: continue
        try:
            typeIndex = windll.kernel32.GetDriveTypeW(u"%s:\\"%drive)
            if typeIndex not in [1,5,6]:
                driveList.append(drive)
        except:
            pass
        
    driveDict = []                                              #list of drive letters + names
    for i in range(len(driveList)):
        char = 0; c=0
        driveString = subprocess.check_output("VOL "+driveList[i]+": ",shell=True).strip(' ').split('\r\n')
        if 'no label' in driveString[0]:
            driveString[0] =' '
        else:
            for j in range(len(driveString[0])):
                if driveString[0][-j]==' ':
                    driveString[0] = driveString[0][-j+1:]
                    break
        driveDict.append([driveList[i][0],driveString[0]])
    return driveDict

"""
The main function of MoveIt. Will copy/move the specified directory files into their
determined destinations

@mode - String - whether to copy or move files
@sort - String - How the files should be sorted into sub-directories in their destination
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
            print( "SD card is not plugged in!" )
	
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
Presents user with a list of the storage devices connected to the computer
"""
def ShowVolumes():
    print( "Searching for Volumes..." )
    VolumeList = GetVolumes()
    for i in range(len(VolumeList)):
        print( VolumeList[i][0]+": "+VolumeList[i][1] )
