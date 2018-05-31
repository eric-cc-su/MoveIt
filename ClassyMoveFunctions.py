import shutil
import os
import os.path
import pickle
import time


def copy_and_move(mode, startpath, endpath):
    """
        Function to copy or move files from one directory to its destination

        :param mode: Whether moving or copying. Either 'copied' or 'moved'
        :param startpath: Directory to start in
        :param endpath: Directory to end in

        :type mode: string
        :type startpath: string
        :type endpath: string
    """
    response = 'success'
    # startpath is a directory
    if os.path.isdir(startpath):
        fileList = os.listdir(startpath)
        # endpath does not exist (create directory)
        if not os.path.exists(endpath):
            os.mkdir(endpath)
            print("CREATED DIRECTORY: " + endpath + '\n')
    else:
        fileList = [startpath]

    # iterate through directory and copy files
    for i in range(len(fileList)):
        try:
            if mode == 'copied':
                shutil.copy2(startpath + '/' + fileList[i], endpath)
            elif mode == 'moved':
                shutil.move(startpath + '/' + fileList[i], endpath)
            print(mode.capitalize() + ' ' + startpath + '/' + fileList[i])
        except:
            print('Error! {}/{} not {}!'.format(startpath, fileList[i], mode))
            response = 'One or more files not ' + mode
    return response


def get_date(path):
    """
        Gets the date of the file and formats the date string

        :param path: the path of the file to get date of

        :type path: string
    """
    # CURRENTLY SET TO MODIFICATION DATE
    thetime = time.gmtime(os.path.getmtime(path))
    dateYr = str(thetime.tm_year)[-2:]
    dateMon = str(thetime.tm_mon)
    dateDay = str(thetime.tm_mday)
    if thetime.tm_mon < 10:
        dateMon = '0' + dateMon
    if thetime.tm_mday < 10:
        dateDay = '0' + dateDay
    dateString = dateYr + '-' + dateMon + '-' + dateDay
    return dateString


def get_manual_path(pathType):
    """
        Get the directory path that the user manually types in

        :param pathType: user's input path

        :type pathType: string
    """
    while True:
        path = raw_input(pathType + " path: ")
        if os.path.exists(path):
            break
        else:
            print("That is not an existing directory path!")
            UserChoice = raw_input(
                "Do you want to create this directory?(y/n)")
            if UserChoice.lower() == 'y':
                os.mkdir(path)
            elif UserChoice.lower() == 'n':
                break
    return path


def go(mode, sort, source, primary, backup):
    """
        The main function of MoveIt. Will copy/move the specified
        directory files into their determined destinations

        :param mode: whether to copy or move files
        :param sort: How the files should be sorted into sub-directories in
            their destination.
            format: *1/0 for primary dest* *1/0 for backup* *string for type* *optional: folder name*
            ex: '11date' = sort by date subfolders in primary & backup
            ex: '10one test' = sort by subfolder "test" in only primary
        :param source: the source path name
        :param primary: the primary destination path name
        :param backup: the backup destination path name

        :type mode: string
        :type sort: string
        :type source: string
        :type primary: string
        :type backup: string
    """
    skip = 0
    response = "success"

    if backup is None and mode in ['copy2', 'move2']:
        print("Back-Up destination path has not been defined!")
        skip = 1

    if skip == 0:
        # SD Card is plugged in
        if os.path.exists(source):
            # List files in directory
            sourceFiles = os.listdir(source)

            total = len(sourceFiles)
            # Number of times the transfer loop needs to execute
            task = 1
            if '2' in mode:
                total *= 2
                task = 2
            itemsdone = 0
            success = 0
            error = 0
            percent = (float(itemsdone)/float(total))*100

            keyword = "copied"
            if mode == "move1":
                keyword = "moved"

            Goprimary = primary
            try:
                Gobackup = backup
            except:
                pass

            # Only copy/move to primary
            if task == 1:
                base = Goprimary
            # Copy/move to both, start with backup
            elif task == 2:
                base = Gobackup

            for t in range(task):
                subfolder = False
                # Second time on file transfer loop, move on to primary
                if task == 2 and t == 1:
                    base = Goprimary
                    # Switch keyword
                    if mode == "move2":
                        keyword = "moved"

                suffix = ''
                for item in sourceFiles:
                    Gosource = source + "/" + item

                    if task == 1 and sort[t] == '1':
                        subfolder = True
                    elif task == 2:
                        if t == 0 and sort[1] == '1':
                            subfolder = True
                        elif t == 1 and sort[0] == '1':
                            subfolder = True

                    # Current task loop requires files to be placed
                    # in subfolder
                    if subfolder:
                        if 'one' in sort:
                            folderName = sort[sort.find(' ') + 1:]
                            suffix = "/" + folderName
                        elif 'date' in sort:
                            suffix = "/" + get_date(Gosource)
                        # Create sub-directories if needed
                        if (not os.path.exists(base + suffix) and
                            not os.path.isdir(base + suffix)):
                                os.mkdir(base + suffix)
                                print("Directory: {} created\n".format(
                                    base + suffix))

                    # Does not transfer file if file already
                    # exists in destination
                    if os.path.exists(base + suffix + "/" + item):
                        os.system('cls')
                        print("{} already exists! File not transferred".format(
                            base + suffix))
                        response = "One or more files not transferred"
                        error += 1

                    # object encountered is a directory
                    elif os.path.isdir(Gosource):
                        try:
                            shutil.copytree(
                                Gosource,
                                "{}/{}".format(base + suffix, item)
                            )
                            print("{}: {}".format(
                                keyword.capitalize(),
                                Gosource)
                            )
                            print("To: {}".format(base + suffix))
                            success += 1
                        except:
                            response = "One or more files not transferred"
                            error += 1

                    else:
                        try:
                            if "copy" in mode or (mode == "move2" and t == 0):
                                    shutil.copy2(Gosource, base + suffix)
                            elif (mode == "move1" or
                                    (mode == "move2" and t == 1)):
                                        shutil.move(Gosource, base + suffix)
                            os.system("cls")
                            print(keyword.capitalize() + ": " + Gosource)
                            print("To: " + (base + suffix))
                            success += 1

                        except:
                            print("Error! {}/ not {} to {}!".format(
                                Gosource,
                                keyword,
                                base+suffix
                            ))
                            response = "One or more files not transferred"
                            error += 1

                    itemsdone += 1
                    percent = (float(itemsdone)/float(total))*100
                    print
                    if success != 0:
                        print("%d/%d file(s) transferred" % (success, total))
                    if error != 0:
                        print("{} file(s) not transferred".format(error))
                    print("Overall progress: {}%\n".format(int(percent)))
            print(response)
        else:
            print("Source directory does not exist!")


def save(fileName, pathlist):
    """
        Saves the user's MoveIt settings in a settings file

        :param fileName: the name of the settings file
        :param pathlist: list of the GUI settings, will be saved into file

        :type fileName: string
        :type pathlist: list
    """
    pathFile = file(fileName, 'wb')
    pickle.dump(pathlist, pathFile)
    print("Settings saved")
