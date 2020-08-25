from pathlib import Path
import shutil
import sys
import os

PROJECT_DIR = Path(__file__).resolve().parents[0]
TEST_DIR = PROJECT_DIR / 'playground' / 'download'

sys.path.append(str(Path(__file__).parents[0] / 'src'))

from twitter_image_dl.twitterimagedl import dlmedia
from twitter_image_dl.runtime_bindings import RuntimeBindings

if os.getenv('IS_TEST', None) == 'True':
    shutil.copyfile(TEST_DIR / 'settings.conf.bak', TEST_DIR / 'settings.conf')
    bindings = RuntimeBindings(TEST_DIR)
else:
    GUI_PATH = Path(sys._MEIPASS).resolve().parents[0] / 'gui'
    bindings = RuntimeBindings(GUI_PATH)

dlmedia(bindings)
