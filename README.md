#Purpose
This project is a simple python script that renames all of the files in a directory, or a specific file, to a format that can be read by Plex.

Specifically, it replaces spaces and other delimiters with periods. It also turns "season" and "episode" into S and E respectively.
This is very much a work in progress, and so expect a lot of changes in the near future. Also expect a lot of bugs. Like a LOT of bugs.

The purpose of this project is twofold: 

1) I needed something to do mass renamings for me 
2) Get more familiar with Python

#Usage

python plex-formatter.py -d/-f [path to directory/ file1 file2 file3 ...] [-tv/-movie]

-d or -f are required. This flag indicates whether you will be providing a directory, in which case all files in the directory will be affected, or specific files
path to directory or list of files indicate target files
-tv or -movie is an optional flag to indicate which format to rename files in
