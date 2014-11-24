MoveIt
======

Personal project with Python to create a small app to sort and move photo files from an SD card to permanent directories

**Started locally as "SDMover", below includes original documentation**

SDMover 0.1.6
Eric Su

REQUIRED FILES: MoveFunctions.py, SDpathfile.db

Copy/Move files from SD card to different directories
'Mode' - Defines if files are copied and where
'dig' - Auto-Dig on or off (searches through directories until an empty one or one with more than one file/folder is found)
'sort' - Will move files into subfolders (currently only with 'date' function)

0.1.2 
- Consolidate all copying, moving and statuses into 'go' function
- SWAP - switch primary destination and backup to only transfer to secondary destination
- 'source','primary','backup' keywords to set paths
- removes spaces in inputs

0.1.3 
- SUB-FOLDER - create subfolder to dump files in destinations, user defined name
-'sort' keyword will be in format 'one(both(12)/primary(1)/backup(2)) (folder name)'

0.1.4 
- Reformat 'go' function
- Dynamic text updates during file transfers
- Clears menu during file transfer, shows simplified, dynamic text
- 'clear' to clear out all saved paths
- Displays subfolder name if declared in 'sort' (currently shows blank bc temporary)
- 'settings' shows all settings, including disabled features

0.1.5
- Status updates include (items done)/(total items), # of files not transferred
- Check if path exists before transferring file
- Directory selection commands revised to accomodate None return from FindPath()
  - FindPath() revised to allow 'exit'/'quit' command to terminate dir selection
- Directory selection is screen clearing

0.1.6 
- Compatibility added to copy/move nested directories
