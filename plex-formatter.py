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
    try:
        return sys.argv.index(flag) + 1
    except:
        return -1

def getIndexOfFirstFile():
    return getIndexOfFlagValue("-f")

def getIndexOfDirectory():
    if(getIndexOfFlagValue("-d") >= 0):
        return getIndexOfFlagValue("-d")
    else:
        return getIndexOfFlagValue("-dr")

def getIndexOfPrependValue():
    return getIndexOfFlagValue("--prepend")

def getIndexOfRemoveValue():
    return getIndexOfFlagValue("--remove-pattern")

def getIndexOfSubPattern():
    return getIndexOfFlagValue("--sub")

def prependValue(baseString):
    prepInd = getIndexOfPrependValue()
    return sys.argv[prepInd] + baseString

def removePattern(baseString):
    removeInd = getIndexOfRemoveValue()
    return re.sub(r'' + sys.argv[removeInd], '', baseString)

def replacePattern(baseString):
    patternInd = getIndexOfSubPattern()
    return re.sub(r'' + sys.argv[patternInd], sys.argv[patternInd + 1],baseString)

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
    if hasFlag("--sub"):
            filenameTokens[-1] = replacePattern(filenameTokens[-1])
    finalName = ("\\").join(filenameTokens)
        
    os.rename(sys.argv[i], finalName)
    print(filenameTokens[-1])

def processListOfFiles():
    i = getIndexOfFirstFile()
    while(isIndexAValidFilepath(i)):
        processIndividualFileAtIndex(i)
        i+=1

def processFilesInDirectory(directory):
    filepath = directory
    if hasFlag("-dr"):
        print("has dr")
        dirs = [d for d in os.listdir(filepath) if path.isdir(filepath + "\\" + d)]
        for dirname in dirs:
            print(filepath + "\\" + dirname)
            processFilesInDirectory(filepath + "\\" + dirname)
    files = [f for f in os.listdir(filepath) if path.isfile( filepath + "/" + f)]
    for filename in files:
        newFilename = handleTVConversions(filename)
        if hasFlag("--prepend"):
            newFilename = prependValue(newFilename)
        if hasFlag("--remove-pattern"):
            newFilename = removePattern(newFilename)
        if hasFlag("--sub"):
            newFilename = replacePattern(newFilename)
        if hasFlag("--name-for-folder"):
            filetype = newFilename.split(".")[-1]
            newFilename = filepath.split("\\")[-1] + "." + filetype
        os.rename(filepath + "/" + filename, filepath + "/" + newFilename)
        print(newFilename)
        
def splitFilePathIntoTokens(index):
    return sys.argv[index].split("\\")


def main():
    if hasFlag("--help"):
        print("valid usage is plex-formatter -d [directory path] or plex-formatter -f [file1] [file2]")
    elif hasFlag("-d") or hasFlag("-dr"):
        processFilesInDirectory(sys.argv[getIndexOfDirectory()])
    elif hasFlag("-f"):
        processListOfFiles()


main()
