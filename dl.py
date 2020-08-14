from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[0] / 'src'))

from twitter_image_dl.twitterimagedl import dlmedia

dlmedia()
