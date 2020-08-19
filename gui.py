from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[0]
sys.path.append(str(PROJECT_DIR / 'src'))

from twitter_image_dl.gui.app import AppGUI
from twitter_image_dl.runtime_bindings import RuntimeBindings

bindings = RuntimeBindings(PROJECT_DIR / 'testdata' / 'settings')
app = AppGUI(bindings)
app.start()
