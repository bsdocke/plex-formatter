#This script formats media filenames for Plex recognition
#
#This script accepts either -d or -f as a flag.
#-d indicates tha the next argument will be a directory
#-f indicates that the next argument will be a file
#Next is the path, followed by an optional -tv or -movie flag
#Default is -movie
#-tv replaces "season" or "episode" in the filename with "S" or "E" respectively
#-movie does nothing yet
#
# Brandon Dockery
# 1/17/2015
import sys
import os
from os import path


if sys.argv[1] == "--help":
    print("valid usage is plex-formatter -d [directory path] or plex-formatter -f [file1] [file2]")
elif sys.argv[1] == "-d":
    filepath = sys.argv[2]
    files = [f for f in os.listdir(filepath) if path.isfile( filepath + "/" + f)]
    for filename in files:
        newFilename = filename.replace(" ", ".")
        newFilename = newFilename.replace("-", "")
        newFilename = newFilename.replace("..", ".")

        if sys.argv.length > 3 && sys.argv[3] == "-tv":
            newFilename = newFilename.replace("Season","S")
            newFilename = newFilename.replace("season","S")
            newFilename = newFilename.replace("Episode", "E")
            newFilename = newFilename.replace("episode", "E")
            
        os.rename(filepath + "/" + filename, filepath + "/" + newFilename)
