#Purpose
This project is a simple python script that renames all of the files in a directory, or a specific file, to a format that can be read by Plex.

Specifically, it replaces spaces and other delimiters with periods. It also turns "season" and "episode" into S and E respectively.
This is very much a work in progress, and so expect a lot of changes in the near future. Also expect a lot of bugs. Like a LOT of bugs.

The purpose of this project is twofold: 

1) I needed something to do mass renamings for me 
2) Get more familiar with Python

#Usage

python plex-formatter.py -d/-f filelistordirectorypath [-tv/movie] [--prepend value] [--remove-pattern pattern]

-d or -f are required. This flag indicates whether you will be providing a directory, in which case all files in the directory will be affected, or specific files
path to directory or list of files indicate target files
-tv or -movie is an optional flag to indicate which format to rename files in
    -tv looks for common episode naming conventions that are not compatible with Plex. It then tries to convert them to the S_E__ format if possible.
    -movie is the default configuration, and either removes common delimiters or converts them to periods. It is a subset of -tv
--prepend is an optional flag that prepends a given string to the files specified
--remove-pattern is an optional flag that removes substrings from a filename that match the given regex
