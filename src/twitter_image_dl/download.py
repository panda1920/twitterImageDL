import logging
import urllib.request
import shutil
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import twitter_image_dl.exceptions as exceptions

logger = logging.getLogger(__name__)

def downloadMedia(urls, saveLocation):
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(download, url, createDownloadFilePath(url, saveLocation) )
            for url in urls
        ]

        for future in futures:
            future.result(timeout=600)
    
def download(url, dst):
    logger.info('Started downloading from %s', url)
    
    if Path(dst).exists():
        return
    try:
        with urllib.request.urlopen(url) as response, open(dst, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        logger.exception('Failed to download from %s', url)
        raise exceptions.DownloadErrorException(f'Failed to download from {url}')

    logger.info('Finished downloading %s', url)

def createDownloadFilePath(url, saveLocation):
    logger.info('Creating save location %s', str(saveLocation))

    lastslashIdx = url.rfind('/')
    filename = url[lastslashIdx + 1:]

    return str( Path(saveLocation, filename) )
