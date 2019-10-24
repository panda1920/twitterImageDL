import urllib.request
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import exceptions

def downloadImages(urls, username, saveLocation):
    createUserDirectory(username, saveLocation)
        
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(download, url, createDownloadFilePath(url, username, saveLocation) )
            for url in urls
        ]

        for future in futures:
            future.result(timeout=2)
    
def download(url, dst):
    if Path(dst).exists():
        return
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