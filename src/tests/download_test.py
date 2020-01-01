from pathlib import Path
import shutil
import sys
import os.path

import pytest
    
PROJECT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_DIR / 'src'
TEST_DL_LOCATION = PROJECT_DIR / 'testdata' / 'download'
TESTIMAGE_LOCATION = PROJECT_DIR / 'testdata' / 'images'

sys.path.append(str( SRC_DIR ))

import exceptions
from download import download, createDownloadFilePath, downloadMedia

@pytest.fixture(scope='function')
def cleanupTestDL():
    for f in TEST_DL_LOCATION.iterdir():
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)

def test_downloadLocalImage(cleanupTestDL):
    fileToDL = Path(TESTIMAGE_LOCATION, 'dog1.jpg').as_uri()
    downloadedFile = TEST_DL_LOCATION / 'dog1.jpg'

    download( str(fileToDL), str(downloadedFile) )
    assert downloadedFile.exists()

def test_downloadLocalNonExistantImage(cleanupTestDL):
    fileToDL = Path(TESTIMAGE_LOCATION, 'NON_EXISTANT_FILE').as_uri()
    downloadedFile = TEST_DL_LOCATION / 'dog1.jpg'

    with pytest.raises(exceptions.DownloadErrorException):
        download( str(fileToDL), str(downloadedFile) )

def test_downloadOnlineImage(cleanupTestDL):
    fileToDL = r'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12234558/Chinook-On-White-03.jpg'
    downloadedFile = TEST_DL_LOCATION / 'onlinedog.jpg'

    download( str(fileToDL), str(downloadedFile) )
    assert downloadedFile.exists()

def test_downloadOnlineNonExistantImage(cleanupTestDL):
    fileToDL = r'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12234558/FOO.jpg'
    downloadedFile = TEST_DL_LOCATION / 'onlinedog.jpg'

    with pytest.raises(exceptions.DownloadErrorException):
        download( str(fileToDL), str(downloadedFile) )

def test_createDownloadFilePath(cleanupTestDL):
    saveLocation = str(TEST_DL_LOCATION)
    fileToDL = r'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12234558/Chinook-On-White-03.jpg'
    filepath = TEST_DL_LOCATION / 'Chinook-On-White-03.jpg'

    assert createDownloadFilePath(fileToDL, saveLocation) == str(filepath)

def test_downloadImagesDownloadsImage(cleanupTestDL):
    saveLocation = str(TEST_DL_LOCATION)
    fileToDL = r'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12234558/Chinook-On-White-03.jpg'
    filepath = TEST_DL_LOCATION / 'Chinook-On-White-03.jpg'

    downloadMedia([fileToDL], saveLocation)
    assert filepath.exists()

def test_downloadImagesOfExistingFileDoesNothing(cleanupTestDL):
    saveLocation = str(TEST_DL_LOCATION)
    fileToDL = str( Path(TESTIMAGE_LOCATION, 'dog1.jpg').as_uri() )
    filepath = TEST_DL_LOCATION  / 'dog1.jpg'

    downloadMedia([fileToDL], saveLocation)

    modTime1 = os.path.getmtime(filepath)
    downloadMedia([fileToDL], saveLocation)
    modTime2 = os.path.getmtime(filepath)

    assert modTime1 == modTime2