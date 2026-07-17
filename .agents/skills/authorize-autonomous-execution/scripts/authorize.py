#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[4]
raise SystemExit(subprocess.call([sys.executable, str(root / "tools" / "devflow.py"), "authorize", *sys.argv[1:]], cwd=root))
