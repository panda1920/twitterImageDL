import sys
from pathlib import Path

import exceptions

def parseArgument():
    checkArgLength(sys.argv)

    _, usersListPath, saveLocation, historyPath, *args = sys.argv

    checkPathExist(usersListPath)
    checkPathExist(saveLocation)

    return {
        'usersListPath': usersListPath,
        'saveLocation': saveLocation,
        'historyPath': historyPath,
    }

def checkArgLength(args):
    if len(args) < 4:
        raise exceptions.InvalidArgumentCountException('Please provide 3 arguments to this script.\nUsage: parseArgument.py <path_to_userslistfile> <path_to_saveLoation> <path_to_historyFile>')

def checkPathExist(path):
    if not Path(path).exists():
        raise exceptions.PathNotExistException(f'Path {path} does not exist')