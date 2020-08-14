import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str( PROJECT_DIR / 'src' ))
