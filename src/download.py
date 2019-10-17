import urllib.request
import shutil
from pathlib import Path

import exceptions

def downloadImages(urls, username, saveLocation):
    createUserDirectory(username, saveLocation)

    for url in urls:
        downloadFilePath = createDownloadFilePath(url, username, saveLocation)
        if not Path(downloadFilePath).exists():
            download(url, downloadFilePath)
    
def download(url, dst):
    try:
        with urllib.request.urlopen(url) as response, open(dst, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except:
        raise exceptions.DownloadErrorException(f'Failed to download from {url}')

def createUserDirectory(username, saveLocation):
    dirToCreate = createUserDirectoryPath(username, saveLocation)
    if not dirToCreate.exists():
        dirToCreate.mkdir()

def createUserDirectoryPath(username, saveLocation):
    return Path(saveLocation, username)

def createDownloadFilePath(url, username, saveLocation):
    lastslashIdx = url.rfind('/')
    filename = url[lastslashIdx + 1:]

    return str( createUserDirectoryPath(username, saveLocation) / filename )