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
    newFilename = newFilename.replace("_", ".")
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


def getIndexOfFlagValue(flag):
    return sys.argv.index(flag) + 1

def getIndexOfFirstFile():
    return getIndexOfFlagValue("-f")

def getIndexOfDirectory():
    return getIndexOfFlagValue("-d")

def getIndexOfPrependValue():
    return getIndexOfFlagValue("--prepend")

def getIndexOfRemoveValue():
    return getIndexOfFlagValue("--remove-pattern")

def prependValue(baseString):
    prepInd = getIndexOfPrependValue()
    return sys.argv[prepInd] + baseString

def removePattern(baseString):
    removeInd = getIndexOfRemoveValue()
    return re.sub(r'' + sys.argv[removeInd], '', baseString)

def isIndexAValidFilepath(i):
    return i < len(sys.argv[i]) and path.isfile(sys.argv[i])

def handleTVConversions(filename):
    newFilename = removeCommonDelimiters(filename)
    if hasTVFlag():
        newFilename = cleanTVConventions(newFilename)
        
    return newFilename

def processIndividualFileAtIndex(index):
    filenameTokens = splitFilePathIntoTokens(i)
    filenameTokens[-1] = handleTVConversions(filenameTokens[-1])
    
    if hasFlag("--prepend"):
            filenameTokens[-1] = prependValue(filenameTokens[-1])
    if hasFlag("--remove-pattern"):
            filenameTokens[-1] = removePattern(filenameTokens[-1])
    finalName = ("\\").join(filenameTokens)
        
    os.rename(sys.argv[i], finalName)
    print(filenameTokens[-1])

def processListOfFiles():
    i = getIndexOfFirstFile()
    while(isIndexAValidFilepath(i)):
        processIndividualFileAtIndex(i)
        i+=1

def processFilesInDirectory():
    filepath = sys.argv[getIndexOfDirectory()]
    files = [f for f in os.listdir(filepath) if path.isfile( filepath + "/" + f)]
    for filename in files:
        newFilename = handleTVConversions(filename)
        if hasFlag("--prepend"):
            newFilename = prependValue(newFilename)
        if hasFlag("--remove-pattern"):
            newFilename = removePattern(newFilename)
        os.rename(filepath + "/" + filename, filepath + "/" + newFilename)
        print(newFilename)
        
def splitFilePathIntoTokens(index):
    return sys.argv[index].split("\\")


def main():
    if hasFlag("--help"):
        print("valid usage is plex-formatter -d [directory path] or plex-formatter -f [file1] [file2]")
    elif hasFlag("-d"):
        processFilesInDirectory()
    elif hasFlag("-f"):
        processListOfFiles()


main()
