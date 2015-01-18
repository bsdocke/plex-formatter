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
import re
import os
from os import path





def hasFilesFlag():
    try:
        sys.argv.index("-f")
        return True
    except ValueError:
        return False

def hasDirectoryFlag():
    try:
        sys.argv.index("-d")
        return True
    except ValueError:
        return False
    
def hasTVFlag():
    try:
        sys.argv.index("-tv")
        return True
    except ValueError:
        return False

def hasFlag(flag):
    try:
        sys.argv.index(flag)
        return True
    except ValueError:
        return False

def removeCommonDelimiters(filename):
    newFilename = filename.replace(" ", ".")
    newFilename = newFilename.replace("-", "")
    newFilename = newFilename.replace("..", ".")
    return newFilename

def cleanSeasonNaming(filename):
    seasonSearch = re.search(r'[Ss]eason(\.*)\d{1,2}',filename)
    if seasonSearch:
        seasonNumberSearch = re.search(r'\d+', seasonSearch.group())
        newFilename = re.sub(r'[Ss]eason(\.*)\d{1,2}(\.*)',"S" + seasonNumberSearch.group(), filename)
        return newFilename
    else:
        return filename

def cleanEpisodeNaming(filename):
    episodeSearch = re.search(r'[Ee]pisode(\.*)\d+',filename)
    if episodeSearch:
        episodeNumberSearch = re.search(r'\d+', episodeSearch.group())
        newFilename = re.sub(r'[Ee]pisode(\.*)\d+',"E" + episodeNumberSearch.group(), filename)
        return newFilename
    else:
        return filename

def cleanXDelimitedNaming(filename):
    searchObj = re.search(r'\d{1,2}x\d{1,2}', filename)
    if searchObj:
        tokens = str(searchObj.group()).split("x")
        newFilename = re.sub(r'\d{1,2}x\d{1,2}', "S" + tokens[0] + "E" + tokens[1], filename, 1)
        return newFilename
    else:
        return filename

def cleanTVConventions(filename):
    newFilename = cleanSeasonNaming(filename)
    newFilename = cleanEpisodeNaming(newFilename)
    newFilename = cleanXDelimitedNaming(newFilename)
    return newFilename

if hasFlag("--help"):
    print("valid usage is plex-formatter -d [directory path] or plex-formatter -f [file1] [file2]")
elif hasFlag("-d"):
    filepath = sys.argv[2]
    files = [f for f in os.listdir(filepath) if path.isfile( filepath + "/" + f)]
    for filename in files:
        newFilename = removeCommonDelimiters(filename)
        if hasTVFlag():
            newFilename = cleanTVConventions(newFilename)
            if hasFlag("--prepend"):
                prepInd = sys.argv.index("--prepend") + 1
                newFilename = sys.argv[prepInd] + newFilename
            print(newFilename)            
        os.rename(filepath + "/" + filename, filepath + "/" + newFilename)
elif hasFlag("-f"):
    i = sys.argv.index("-f") + 1
    while(i < len(sys.argv[i]) and path.isfile(sys.argv[i])):
        filenameTokens = sys.argv[i].split("\\")
        filename = filenameTokens[len(filenameTokens) -1]
        newFilename = removeCommonDelimiters(filename)
        if hasTVFlag():
            newFilename = cleanTVConventions(newFilename)
            if hasFlag("--prepend"):
                prepInd = sys.argv.index("--prepend") + 1
                newFilename = sys.argv[prepInd] + newFilename
            print(newFilename)
        filenameTokens[len(filenameTokens) -1] = newFilename
        finalName = ("\\").join(filenameTokens)
        os.rename(sys.argv[i], finalName)
        i+=1


