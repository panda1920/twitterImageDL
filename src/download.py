import urllib.request
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import exceptions

def downloadMedia(urls, saveLocation):
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(download, url, createDownloadFilePath(url, saveLocation) )
            for url in urls
        ]

        for future in futures:
            future.result(timeout=600)
    
def download(url, dst):
    if Path(dst).exists():
        return
    try:
        with urllib.request.urlopen(url) as response, open(dst, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except:
        raise exceptions.DownloadErrorException(f'Failed to download from {url}')

def createDownloadFilePath(url, saveLocation):
    lastslashIdx = url.rfind('/')
    filename = url[lastslashIdx + 1:]

    return str( Path(saveLocation, filename) )