from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[0] / 'src'))

from twitter_image_dl.twitterimagedl import dlmedia
from twitter_image_dl.runtime_bindings import RuntimeBindings

bindings = RuntimeBindings(Path(sys._MEIPASS))
dlmedia(bindings)
