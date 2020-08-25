from pathlib import Path
import shutil
import sys

PROJECT_DIR = Path(__file__).resolve().parents[0]
TEST_DIR = PROJECT_DIR / 'playground' / 'download'
sys.path.append(str(PROJECT_DIR / 'src'))

from twitter_image_dl.gui.app import AppGUI
from twitter_image_dl.runtime_bindings import RuntimeBindings

# copy setting for test
shutil.copyfile(TEST_DIR / 'settings.conf.bak', TEST_DIR / 'settings.conf')

bindings = RuntimeBindings(TEST_DIR)
app = AppGUI(bindings)
app.start()
