from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.init_db import initialize_db

if __name__ == '__main__':
    initialize_db()
