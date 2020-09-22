from pathlib import Path
import shutil
import sys
import os
import logging

PROJECT_DIR = Path(__file__).resolve().parents[0]
TEST_WORK_DIR = PROJECT_DIR / 'testdata' / 'work'
SETTINGS_DIR = PROJECT_DIR / 'testdata' / 'settings'

sys.path.append(str(PROJECT_DIR / 'src'))

from twitter_image_dl.twitterimagedl import dlmedia
from twitter_image_dl.runtime_bindings import RuntimeBindings
from twitter_image_dl.log_setup import setup_logger

if os.getenv('IS_TEST', None) == 'True':
    shutil.copyfile(SETTINGS_DIR / 'settings.conf', TEST_WORK_DIR / 'settings.conf')
    work_dir = TEST_WORK_DIR
else:
    work_dir = Path(sys._MEIPASS).resolve().parents[0] / 'gui' # dir where gui exe is located at

setup_logger(work_dir, logging.DEBUG)
bindings = RuntimeBindings(work_dir)
dlmedia(bindings)
