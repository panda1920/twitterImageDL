class DownloadErrorException(Exception):
    '''Raised when download operation fails for some reason'''

class FileOpenErrorException(Exception):
    '''Raised when failed to open file'''

class InvalidArgumentCountException(Exception):
    '''Raised when expected argument was not passed to this program'''

class PathNotExistException(Exception):
    '''Raised when path passed as argument does not exist'''