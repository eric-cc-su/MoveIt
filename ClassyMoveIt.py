"""
"ClassyMoveIt"
Author: Eric Su

File Transfer utility with GUI
Based off of SDMover

pathList['sort'] (subfolder) in format:
    -'10date', '11one (subfolder)'
"""
from Tkinter import *
import os
import os.path
import pickle
import tkFileDialog
import tkMessageBox
from ClassyMoveFunctions import *


class AppMenu(Frame):
    """ Tool/Menu bar of GUI """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.widgets()

    def widgets(self):
        """ Toolbar menu labels """
        menubar = Menu(root)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save Settings', command=self.save)
        filemenu.add_command(label='Exit', command=self.kill)
        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_command(label='Settings', command=self.show_settings)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Help', command=self.show_help)
        helpmenu.add_command(label='About...', command=self.show_about)
        menubar.add_cascade(label='Help', menu=helpmenu)

        root.config(menu=menubar)

    def kill(self):
        """ Close program """
        self.checkList = pickle.load(file('SDpathfile.db', 'r'))
        if self.checkList != pathList:
            if tkMessageBox.askyesno("Wait!",
                "Are you sure you want to exit without saving settings?"):
                root.destroy()
        else:
            root.destroy()

    def save(self):
        """ Save paths and any settings by dumping into .db file """
        pathList['Source'] = browse.sourcebox.get()
        pathList['Primary'] = browse.primarybox.get()
        pathList['Backup'] = browse.backupbox.get()
        pickle.dump(pathList, file('SDpathfile.db', 'wb'))
        tkMessageBox.showinfo("Saved", "Settings have been saved.")

    def show_about(self):
        """ Display "About" window with info about program """
        about = Toplevel()
        about.title("About...")
        about_exit = Button(about, text="OK", command=about.destroy)
        about_exit.pack()

    def show_help(self):
        """ Display "Help" window for program """
        helpWin = Toplevel()
        helpWin.title("Help")
        help_exit = Button(helpWin, text="OK", command=helpWin.destroy)
        help_exit.pack()

    def show_settings(self):
        """ Display "Settings" window """
        settings = Toplevel()
        settings.title("Settings")
        settings_exit = Button(settings, text="OK", command=settings.destroy)
        settings_exit.pack()


class Browse(Frame):
    """ GUI section with directory selection boxes (pathboxes) """
    def __init__(self, master, paths):
        self.paths = paths
        Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky=W, columnspan=3)
        self.widgets()

    def widgets(self):
        """ The pathboxes and buttons """
        self.sourcebox = Pathbox(root, "Source", 0)
        self.primarybox = Pathbox(root, "Primary", 1)

        swap = Button(root, text="^ SWAP v", command=self.swapPaths)
        swap.grid(row=2, column=1)

        self.backupbox = Pathbox(root, "Backup", 3)

        self.sourcebox.insert(0, self.paths['Source'])
        self.primarybox.insert(0, self.paths['Primary'])
        self.backupbox.insert(0, self.paths['Backup'])

    def swapPaths(self):
        """ Function to swap values between primary and backup pathboxes """
        primarytemp = self.paths['Primary']
        self.paths['Primary'] = self.paths['Backup']
        self.paths['Backup'] = primarytemp

        self.primarybox.update(self.paths['Primary'])
        self.backupbox.update(self.paths['Backup'])

class GoButton:
    """ Big green "GO" button to run MoveIt functions """
    def __init__(self, root):
        gb = Button(
            root,
            text="GO!",
            bg="lime green",
            height=5,
            width=70,
            command=self.check
        )
        gb.grid(
            row=4,
            column=0,
            rowspan=4,
            columnspan=3,
            pady=20,
            padx=10
        )

        if '' not in [browse.sourcebox.get(), browse.primarybox.get()]:
            if '2' in pathList['Mode']:
                if browse.backupbox.get() != '':
                    gb.focus_set()
            else:
                gb.focus_set()
        gb.bind('<Return>', self.keyPress)

    def check(self):
        """
            Check that all required information has been defined.
            Step 1 in kick-off, will pass off to `go(self)` if all clear
        """
        if '' in [browse.sourcebox.get(), browse.primarybox.get()]:
            tkMessageBox.showerror("Error", "A required path is undefined")

        elif '2' in pathList['Mode'] and browse.backupbox.get() == '':
            tkMessageBox.showerror("Error", "A required path is undefined")

        elif 'one' in pathList['sort'] and sort.onesortbox.get() == '':
            tkMessageBox.showerror("Error", "The sub-folder is undefined!")

        else:
            pathList['Source'] = browse.sourcebox.get()
            pathList['Primary'] = browse.primarybox.get()
            pathList['Backup'] = browse.backupbox.get()
            self.go()

    def go(self):
        """
            Check that the destination paths exist and kick off "Go()" to
            run MoveIt function. Step 2 in kick-off, will pass of
            to `go()` in MoveItFunctions
        """
        if not os.path.exists(pathList['Source']):
            tkMessageBox.showerror("Error",
                "The source path is not available or does not exist!")

        elif len(os.listdir(pathList['Source'])) == 0:
            tkMessageBox.showerror("Error",
                "The source directory is empty!")

        elif not os.path.exists(pathList['Primary']):
            tkMessageBox.showerror("Error",
                "The primary path is not available or does not exist!")

        elif not os.path.exists(pathList['Backup']) and '2' in pathList['Mode']:
            tkMessageBox.showerror("Error",
                "The back-up path is not available or does not exist!")

        else:
            # *****Status Window (buggy) *****
            # statusWindow = Status()
            # statusWindow.statusUpdates(
            #     pathList['Mode'],
            #     pathList['sort'],
            #     pathList['Source'],
            #     pathList['Primary'],
            #     pathList['Backup']
            # )
            # statusWindow = Status(
            #     pathList['Mode'],
            #     pathList['sort'],
            #     pathList['Source'],
            #     pathList['Primary'],
            #     pathList['Backup']
            # )
            # *****Console updates*****
            if 'one' in pathList['sort']:
                # rewrite 'sort' if subfolder is different
                if pathList['sort'][6:] != sort.onesortbox.get():
                    pathList['sort'] = pathList['sort'][ :5]+' '+sort.onesortbox.get()
            go(
                pathList['Mode'],
                pathList['sort'],
                pathList['Source'],
                pathList['Primary'],
                pathList['Backup']
            )
            # statusWindow = Status(
            #     pathList['Mode'],
            #     pathList['sort'],
            #     pathList['Source'],
            #     pathList['Primary'],
            #     pathList['Backup']
            # )

    def keyPress(self, event):
        """ Allows kick-off by key-press rather than just mouse click """
        self.check()


class ModeSelect(LabelFrame):
    """ Mode selection GUI section """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Mode")
        self.grid(row=0, column=3, rowspan=4, padx=10, sticky=W)
        self.widgets()

    def widgets(self):
        """ The checkboxes and widgets of mode selection """
        self.modevar = StringVar()
        self.modevar.set(pathList['Mode'])

        copy1 = Radiobutton(self, text="Copy to Primary",
            variable=self.modevar, value="copy1", command=self.update)
        copy2 = Radiobutton(self, text="Copy to Primary and Back-Up",
            variable=self.modevar, value="copy2", command=self.update)
        move1 = Radiobutton(self, text="Move to Primary",
            variable=self.modevar, value="move1", command=self.update)
        move2 = Radiobutton(self, text="Move to Primary, copy to Back-Up",
            variable=self.modevar, value="move2", command=self.update)

        copy1.pack(anchor=W)
        copy2.pack(anchor=W)
        move1.pack(anchor=W)
        move2.pack(anchor=W)

    def update(self):
        """ Update the "mode" setting """
        pathList['Mode'] = self.modevar.get()
        browse.backupbox.updateState()


class Pathbox:
    """ Individual directory path box (define and display directory path) """
    def __init__(self, root, var, row):
        self.row = row
        self.var = var
        Label(root, text=str(self.var) + ': ').grid(
            row=self.row,
            column=0,
            sticky=W,
            padx=10
        )
        self.box = Entry(root, width=60)
        self.box.grid(row=self.row, column=1)

        browse = Button(root, text='Browse...', command=self.gobrowse)
        browse.grid(row=self.row, column=2, padx=5)

    def get(self):
        """ Return the contents of the pathbox """
        return self.box.get()

    def gobrowse(self):
        """ Run directory selection tool """
        getdirectory = tkFileDialog.askdirectory(
            title='Select Directory',
            initialdir=self.box.get()
        )
        if getdirectory != '':
            self.update(getdirectory)
            pathList[self.var] = getdirectory

    def insert(self, index, info):
        """ Insert value into pathbox """
        self.box.insert(index, info)

    def update(self, info):
        """ Update the contents of the pathbox """
        # Enable textbox for edit if disabled
        if self.box.cget('state') != 'NORMAL':
            tempConfigVar = self.box.cget('state')
            self.box.config(state=NORMAL)

        if self.box.get() != info and info != None:
            self.box.delete(0, END)
            self.box.insert(0, info)
            # reinstate original state of box if previously disabled
            try:
                self.box.config(state=tempConfigVar)
            except:
                pass

    def updateState(self):
        """ Update the state of the pathbox (active/inactive) """
        if '1' in mode.modevar.get():
            self.box.config(state='readonly', readonlybackground='grey')
        else:
            self.box.config(state=NORMAL)
            """
            if self.box.get() == '':
                self.box.config( bg='red' )
            else:
                self.box.config( bg='white' )
            """


class SubfolderSelect(LabelFrame):
    """ GUI section to select subfolders to move files to """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Sub-Folder")
        self.grid(row=4, column=3, rowspan=4, padx=10, pady=10, sticky=W)
        self.widgets()

    def widgets(self):
        """ Widgets for subfolder selection """
        self.pplacement = IntVar()
        self.bplacement = IntVar()
        self.sortvar = StringVar()

        self.primarycheck = Checkbutton(
            self,
            text="Primary Dest.",
            variable=self.pplacement,
            command=self.update
        )
        self.backupcheck = Checkbutton(
            self,
            text="Back-Up Dest.",
            variable=self.bplacement,
            command=self.update
        )
        if pathList['sort'][0] == '1':
            self.primarycheck.select()
        if pathList['sort'][1] == '1':
            self.backupcheck.select()
        self.datesort = Radiobutton(
            self,
            text="By Date",
            variable=self.sortvar,
            value="date",
            command=self.update
        )
        self.onesort = Radiobutton(
            self,
            text="User Specified: ",
            variable=self.sortvar,
            value='one',
            command=self.update
        )
        self.onesortbox = Entry(self)

        if 'one' in pathList['sort']:
            self.sortvar.set('one')
            # insert subfolder name
            self.onesortbox.insert(0,
                pathList['sort'][pathList['sort'].index(' ') + 1:])
            # clear out subfolder name in variable to avoid constant appending
            pathList['sort'] = pathList['sort'][:pathList['sort'].index(' ')]
        else:
            self.sortvar.set('date')

        self.primarycheck.grid(row=0, column=0, sticky=W)
        self.backupcheck.grid(row=0, column=1, sticky=W)
        self.datesort.grid(row=1, column=0, sticky=W)
        self.onesort.grid(row=2, column=0, sticky=W)
        self.onesortbox.grid(row=2, column=1, padx=5, sticky=E)

    def update(self):
        """ Update settings to save subfolder """
        pathList['sort'] = str(self.pplacement.get())+str(self.bplacement.get())+str(self.sortvar.get())
        # return True


###############################################################################

root = Tk()
root.title("Classy MoveIt")
root.resizable(0, 0)  # Fixed window size

# load settings
try:
    pathFile = file('SDpathfile.db', 'r')
    pathList = pickle.load(pathFile)
except:
    pathList = {
        'Mode': 'copy1',
        'dig': 'n',
        'sort': '00date',
        'Source': '',
        'Primary': '',
        'Backup': '',
        'sub': ''
    }
    # save()

appmenu = AppMenu(root)
browse = Browse(root, pathList)
gobutton = GoButton(root)
mode = ModeSelect(root)
sort = SubfolderSelect(root)

root.mainloop()
