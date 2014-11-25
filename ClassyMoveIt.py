"""
"ClassyMoveIt"
Author: Eric Su

File Transfer utility with GUI
Based off of SDMover

pathList['sort'] (subfolder) in format:
    -'10date', '11one (subfolder)'
"""
from Tkinter import *
import shutil
import os
import os.path
import pickle
import shutil
import string
import subprocess
import time
import tkFileDialog
import tkFont
import tkMessageBox
from ClassyMoveFunctions import *

"""
Tool/Menu bar of GUI
"""
class AppMenu(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.widgets()

    """
    Toolbar menu labels
    """
    def widgets(self):
        menubar = Menu(root)

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command (label = 'Save Settings', command = self.save)
        filemenu.add_command (label = 'Exit', command = self.kill)
        menubar.add_cascade(label = 'File', menu = filemenu)
        menubar.add_command(label = 'Settings', command = self.showSettings)

        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = 'Help', command = self.showHelp)
        helpmenu.add_command(label = 'About...', command = self.showAbout)
        menubar.add_cascade(label = 'Help', menu = helpmenu)

        root.config(menu=menubar)

    """
    Close program
    """
    def kill(self):
        self.checkList = pickle.load(file('SDpathfile.db','r'))
        if self.checkList != pathList:
            if tkMessageBox.askyesno("Wait!", "Are you sure you want to exit without saving settings?"):
                root.destroy()
        else:
            root.destroy()
    
    """
    Save paths and any settings by dumping into .db file
    """
    def save(self):
        pathList['Source'] = browse.sourcebox.get()
        pathList['Primary'] = browse.primarybox.get()
        pathList['Backup'] = browse.backupbox.get()
        pickle.dump(pathList, file('SDpathfile.db','wb'))
        tkMessageBox.showinfo("Saved", "Settings have been saved.")
    
    """
    Display "About" window with info about program
    """
    def showAbout(self):
        about = Toplevel()
        about.title("About...")
        about_exit = Button(about, text = "OK", command = about.destroy)
        about_exit.pack()
    
    """
    Display "Help" window for program
    """
    def showHelp(self):
        helpWin = Toplevel()
        helpWin.title("Help")
        help_exit = Button(helpWin, text = "OK", command = helpWin.destroy)
        help_exit.pack()
    
    """
    Display "Settings" window
    """ 
    def showSettings(self):
        settings = Toplevel()
        settings.title("Settings")
        settings_exit = Button(settings, text = "OK", command = settings.destroy)
        settings_exit.pack()

"""
GUI section with directory selection boxes (pathboxes)
"""
class Browse(Frame):
    def __init__(self,master, paths):
        self.paths = paths
        Frame.__init__(self,master)
        self.grid(row = 0, column = 0, sticky = W, columnspan = 3)
        self.widgets()

    """
    The pathboxes and buttons 
    """
    def widgets(self):
        self.sourcebox = Pathbox(root, "Source", 0)
        self.primarybox = Pathbox(root, "Primary", 1)
        
        swap = Button(root, text = "^ SWAP v", command = self.swapPaths)
        swap.grid(row = 2, column = 1)
        
        self.backupbox = Pathbox(root, "Backup", 3)

        self.sourcebox.insert(0,self.paths['Source'])
        self.primarybox.insert(0,self.paths['Primary'])
        self.backupbox.insert(0,self.paths['Backup'])
    
    """
    Function to swap values between `primary` and `backup` pathboxes
    """
    def swapPaths(self):
        primarytemp = self.paths['Primary']
        self.paths['Primary'] = self.paths['Backup']
        self.paths['Backup'] = primarytemp
        
        self.primarybox.update(self.paths['Primary'])
        self.backupbox.update(self.paths['Backup'])

"""
Big green "GO" button to run MoveIt functions
"""      
class GoButton:
    def __init__(self,root):
        gb = Button(root, text = "GO!",
                    bg="lime green", height = 5,
                    width = 70, command = self.check)
        gb.grid(row = 4, column = 0, rowspan = 4,
                columnspan = 3, pady = 20, padx = 10)
                
        if '' not in [ browse.sourcebox.get(), browse.primarybox.get() ]:
            if '2' in pathList[ 'Mode' ]:
                if browse.backupbox.get() != '':
                    gb.focus_set()
            else:
                gb.focus_set()
        gb.bind( '<Return>', self.keyPress )
    
    """
    Check that all required information has been defined.
    Step 1 in kick-off, will pass off to `go(self)` if all clear
    """
    def check( self ):
        if '' in [ browse.sourcebox.get(), browse.primarybox.get() ]:
            tkMessageBox.showerror( "Error", "A required path is undefined" )
        
        elif '2' in pathList[ 'Mode' ] and browse.backupbox.get() == '':
            tkMessageBox.showerror( "Error", "A required path is undefined" )
        
        elif 'one' in pathList[ 'sort' ] and sort.onesortbox.get() == '':
            tkMessageBox.showerror( "Error", "The sub-folder is undefined!" )
        
        else:
            pathList[ 'Source' ] = browse.sourcebox.get()
            pathList[ 'Primary' ] = browse.primarybox.get()
            pathList[ 'Backup' ] = browse.backupbox.get()
            self.go()
    
    """
    Check that the destination paths exist and kick off "Go()" to run MoveIt function.
    Step 2 in kick-off, will pass of to `go()` in MoveItFunctions
    """
    def go(self):
        if not os.path.exists( pathList[ 'Source' ] ):
            tkMessageBox.showerror( "Error", "The source path is not available or does not exist!" )
        
        elif len( os.listdir( pathList[ 'Source' ] ) ) == 0:
			tkMessageBox.showerror( "Error", "The source directory is empty!" )
            
        elif not os.path.exists( pathList[ 'Primary' ] ):
            tkMessageBox.showerror( "Error", "The primary path is not available or does not exist!" )
            
        elif not os.path.exists( pathList[ 'Backup' ] ) and '2' in pathList[ 'Mode' ]:
            tkMessageBox.showerror( "Error", "The back-up path is not available or does not exist!" )
            
        else:
            #*****Status Window (buggy) *****
            #statusWindow = Status() 
            #statusWindow.statusUpdates( pathList[ 'Mode' ], pathList[ 'sort' ], pathList[ 'Source' ], pathList[ 'Primary' ], pathList[ 'Backup' ] )
            #statusWindow = Status( pathList[ 'Mode' ], pathList[ 'sort' ], pathList[ 'Source' ], pathList[ 'Primary' ], pathList[ 'Backup' ] )
            #*****Console updates*****
            if 'one' in pathList['sort']:
                if pathList['sort'][6:] != sort.onesortbox.get(): #rewrite 'sort' if subfolder is different
                    pathList['sort'] = pathList['sort'][ :5]+' '+sort.onesortbox.get()
            go( pathList[ 'Mode' ], pathList[ 'sort' ], pathList[ 'Source' ], pathList[ 'Primary' ], pathList[ 'Backup' ] )
            #statusWindow = Status( pathList[ 'Mode' ], pathList[ 'sort' ], pathList[ 'Source' ], pathList[ 'Primary' ], pathList[ 'Backup' ] )
            
    #Allows kick-off by key-press rather than just mouse click
    def keyPress(self, event):
        self.check()

"""
Mode selection GUI section
"""
class ModeSelect(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self,master,text = "Mode")
        self.grid(row = 0, column = 3, rowspan = 4, padx = 10, sticky = W)
        self.widgets()

    """
    The checkboxes and widgets of mode selection
    """
    def widgets(self):
        self.modevar = StringVar()
        self.modevar.set(pathList['Mode'])
        
        copy1 = Radiobutton(self, text = "Copy to Primary", variable = self.modevar, value = "copy1", command = self.update)
        copy2 = Radiobutton(self, text = "Copy to Primary and Back-Up", variable = self.modevar, value = "copy2", command = self.update)
        move1 = Radiobutton(self, text = "Move to Primary", variable = self.modevar, value = "move1", command = self.update)
        move2 = Radiobutton(self, text = "Move to Primary, copy to Back-Up", variable = self.modevar, value = "move2", command = self.update)

        copy1.pack(anchor = W)
        copy2.pack(anchor = W)
        move1.pack(anchor = W)
        move2.pack(anchor = W)
    
    """
    Update the "mode" setting
    """
    def update(self):
        pathList['Mode'] = self.modevar.get()
        browse.backupbox.updateState()

"""
Individual directory path box (define and display directory path)
"""
class Pathbox:
    def __init__(self, root, var, row):
        self.row = row
        self.var = var
        Label( root, text = str( self.var ) + ': ' ).grid(row = self.row, column = 0, sticky = W, padx = 10)
        self.box = Entry(root, width = 60)
        self.box.grid(row = self.row, column = 1)

        browse = Button(root, text = 'Browse...', command = self.gobrowse)
        browse.grid(row = self.row, column = 2, padx = 5)
    
    """
    Return the contents of the pathbox
    """
    def get(self):
        return self.box.get()

    """
    Run directory selection tool
    """
    def gobrowse(self):
        getdirectory = tkFileDialog.askdirectory(title = 'Select Directory', initialdir = self.box.get())
        if getdirectory != '':
            self.update( getdirectory )
            pathList[ self.var ] = getdirectory

    """
    Insert value into pathbox
    """
    def insert(self, index, info):
        self.box.insert(index,info)

    """
    Update the contents of the pathbox
    """
    def update(self,info):
        if self.box.cget('state') != 'NORMAL': #Enable textbox for edit if disabled
            tempConfigVar = self.box.cget('state')
            self.box.config(state = NORMAL)
            
        if self.box.get() != info and info != None:
            self.box.delete(0,END)
            self.box.insert(0,info)
            try: #reinstate original state of box if previously disabled
                self.box.config(state = tempConfigVar)
            except:
                pass
    
    """
    Update the state of the pathbox (active/inactive)
    """       
    def updateState(self):
        if '1' in mode.modevar.get():
            self.box.config(state = 'readonly', readonlybackground = 'grey')
        else:
            self.box.config(state = NORMAL)
            """
            if self.box.get() == '':
                self.box.config( bg = 'red' )
            else:
                self.box.config( bg = 'white' )
            """

"""
New window to display MoveIt progress/updates
"""
class Status: #status window
    def __init__(self):
        self.window = Toplevel()
        self.window.title("File Transfer in Progress...")
        #self.window.config( background = '' )
        #self.window.minsize(width = 640, height = 200)
        
        #self.line2 and self.line5 should stay blank
        self.text = Label( self.window, text = " ", anchor = W, justify = LEFT )
        self.text.grid( row = 0 )
        
        self.statusUpdates( pathList[ 'Mode' ], pathList[ 'sort' ], pathList[ 'Source' ], pathList[ 'Primary' ], pathList[ 'Backup' ] )
        """
        self.text = Text( self.window, relief = FLAT, height = 13 )
        self.text.insert( INSERT, "File Transfer in Progress\n")
        self.text.grid()
        """
    
    """
    Provide status updates to display progress/issues
    """
    def statusUpdates( self, mode, sort, source, primary, backup ):
        skip = 0
        response = "success"
        
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
            #Copy/Move to both, start with backup
            elif task == 2:
                base = Gobackup
            
            for t in range( task ):
                #Boolean if files are place in a subfolder
                subfolder = False
                #Second time on file transfer loop, move on to primary destination
                if task == 2 and t == 1:
                    base = Goprimary
                    #Switch keyword
                    if mode == "move2":
                        keyword = "moved"
                
                suffix = ''
                for item in sourceFiles:
                    root.update_idletasks()
                    line0 = '\n'; line1 = '\n'; line3 = '\n'; line4 = '\n'; line6 = '\n'; line7 = '\n'
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
                            #self.text.insert( END, "Directory: " + ( base + suffix ) + " created\n" )
                            #self.line6.config( text = "Directory: " + ( base + suffix ) + " created" )
                            line6 = "Directory: " + ( base + suffix ) + " created\n"
                    
                    #Does not transfer file if file already exists in destination
                    if os.path.exists( base + suffix + "/" + item ):
                        #**Clear window**
                        #self.text.insert( END, base + suffix + " already exists! File not transferred" + "\n" )
                        #self.line6.config( text = base + suffix + " already exists! File not transferred" )
                        line6 = base + suffix + " already exists! File not transferred\n" 
                        response = "One or more files not transferred"
                        error += 1
                    
                    #object encountered is a directory
                    elif os.path.isdir( Gosource ):
                        try:
                            shutil.copytree( Gosource, base + suffix + "/" + item )
                            """
                            self.text.insert( END, keyword.capitalize() + ": " + Gosource + "\n" )
                            self.text.insert( END, "To: " + ( base + suffix ) + "\n" )
                            
                            self.line0.config( text = keyword.capitalize() + ": " + Gosource )
                            self.line1.config( text = "To: " + ( base + suffix ) )
                            """
                            line0 = keyword.capitalize() + ": " + Gosource + '\n'
                            line1 = "To: " + ( base + suffix ) + '\n'
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
                            #**Clear window**
                            """
                            self.text.insert( END, keyword.capitalize() + ": " + Gosource + "\n" )
                            self.text.insert( END, "To: " + ( base + suffix ) + "\n" )
                            
                            self.line0.config( text = keyword.capitalize() + ": " + Gosource )
                            self.line1.config( text = "To: " + ( base + suffix ) )
                            """
                            line0 = keyword.capitalize() + ": " + Gosource + '\n'
                            line1 = "To: " + ( base + suffix ) + '\n'
                            success += 1
                        
                        except:
                            #self.text.insert( END, "Error! " + Gosource + "/ not " + keyword + " to " + ( base + suffix ) + "!\n" )
                            #self.line6.config( text = "Error! " + Gosource + "/ not " + keyword + " to " + ( base + suffix ) + "!" )
                            line6 = "Error! " + Gosource + "/ not " + keyword + " to " + ( base + suffix ) + "!\n"
                            response = "One or more files not transferred"
                            error += 1
                    
                    itemsdone += 1
                    percent = ( float( itemsdone ) / float( total ) ) * 100
                    #self.text.insert( END, "\n" )
                    if success != 0:
                        #self.text.insert( END, str( success ) + "/" + str( total ) + " file(s) transferred\n" )
                        #self.line3.config( text = str( success ) + "/" + str( total ) + " file(s) transferred" )
                        line3 = str( success ) + "/" + str( total ) + " file(s) transferred\n" 
                    if error != 0:
                        #self.text.insert( END, str( error ) + " files(s) not transferred\n" )
                        #self.line7.config( text = str( error ) + " files(s) not transferred" )
                        line7 = str( error ) + " files(s) not transferred\n"
                    #self.text.insert( END, "Overall progress: " + str( int( percent ) ) + "%\n" )
                    #self.line4.config( text = "Overall progress: " + str( int( percent ) ) + "%" )
                    line4 = "Overall progress: " + str( int( percent ) ) + "%\n"
                    self.text.config( text = line0 + line1 + '\n' + line3 + line4 + '\n' + line6 + line7 )
                    root.update_idletasks()
            #self.text.insert( END, response + "\n" )
            self.text.config( text = response )
            
"""
GUI section to select subfolders to move files to
"""
class SubfolderSelect(LabelFrame):
    def __init__(self,master):
        LabelFrame.__init__(self, master, text = "Sub-Folder")
        self.grid (row = 4, column = 3, rowspan = 4, padx = 10, pady = 10, sticky = W)
        self.widgets()
        
    """
    Widgets for subfolder selection
    """
    def widgets(self):
        self.pplacement = IntVar()
        self.bplacement = IntVar()
        self.sortvar = StringVar()
        
        self.primarycheck = Checkbutton(self, text = "Primary Dest.", variable = self.pplacement, command = self.update)
        self.backupcheck = Checkbutton(self, text = "Back-Up Dest.", variable = self.bplacement, command = self.update)
        if pathList['sort'][0] == '1':
            self.primarycheck.select()
        if pathList['sort'][1] == '1':
            self.backupcheck.select()
        self.datesort = Radiobutton(self, text = "By Date", variable = self.sortvar, value = "date", command = self.update)
        self.onesort = Radiobutton(self, text = "User Specified: ", variable = self.sortvar, value = 'one', command = self.update)
        self.onesortbox = Entry(self)
        
        if 'one' in pathList['sort']:
            self.sortvar.set('one')
            self.onesortbox.insert(0, pathList['sort'][ pathList['sort'].index(' ') + 1: ]) #insert subfolder name
            pathList['sort'] = pathList['sort'][ :pathList['sort'].index(' ') ] #clear out subfolder name in variable to avoid constant appending
        else:
            self.sortvar.set('date')

        self.primarycheck.grid(row = 0, column = 0, sticky = W)
        self.backupcheck.grid(row = 0, column = 1, sticky = W)
        self.datesort.grid(row = 1, column = 0, sticky = W)
        self.onesort.grid(row = 2, column = 0, sticky = W)
        self.onesortbox.grid(row = 2, column = 1, padx = 5, sticky = E)

    """
    Update settings to save subfolder
    """
    def update(self):
        pathList['sort'] = str(self.pplacement.get())+str(self.bplacement.get())+str(self.sortvar.get())
        #return True

##############################################################################################

root = Tk()
root.title("Classy MoveIt")
root.resizable( 0, 0 ) #Fixed window size

try: #load settings
    pathFile = file('SDpathfile.db','r')
    pathList = pickle.load(pathFile)
except:
    pathList = {'Mode':'copy1','dig':'n','sort':'00date','Source':'','Primary':'','Backup':'','sub':''}
    #save()

appmenu = AppMenu(root)
browse = Browse(root, pathList)
gobutton = GoButton(root)
mode = ModeSelect(root)
sort = SubfolderSelect(root)

root.mainloop()
