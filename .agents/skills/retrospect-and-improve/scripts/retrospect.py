#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
raise SystemExit(subprocess.call([sys.executable, str(root / "tools" / "devflow.py"), "session-retrospective", *sys.argv[1:]], cwd=root))
