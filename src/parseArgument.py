import sys
from pathlib import Path

import exceptions

def parseArgument():
    checkArgLength(sys.argv)

    _, usersListPath, saveLocation, *args = sys.argv

    checkPathExist(usersListPath)
    checkPathExist(saveLocation)

    return {
        'usersListPath': usersListPath,
        'saveLocation': saveLocation,
    }

def checkArgLength(args):
    if len(args) < 3:
        raise exceptions.InvalidArgumentCountException('Please provide 2 arguments to this script.\nUsage: parseArgument.py <path_to_userslistfile> <path_to_savedownloadedfiles>')

def checkPathExist(path):
    if not Path(path).exists():
        raise exceptions.PathNotExistException(f'Path {path} does not exist')