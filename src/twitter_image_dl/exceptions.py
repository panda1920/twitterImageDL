class DownloadErrorException(Exception):
    '''Raised when download operation fails for some reason'''

class FileOpenErrorException(Exception):
    '''Raised when failed to open file'''

class InvalidArgumentCountException(Exception):
    '''Raised when expected argument was not passed to this program'''

class PathNotExistException(Exception):
    '''Raised when path passed as argument does not exist'''

class APINotFound(Exception):
    '''Raised when API related options were not found'''

class SaveLocationNotExist(Exception):
    '''Raised when save location does not exist'''
