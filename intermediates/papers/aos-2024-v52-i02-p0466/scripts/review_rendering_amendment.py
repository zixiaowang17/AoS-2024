"""Check the recorded source-backed rendering amendment."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT.parents[1]/"scripts/review_rendering_amendment.py"),ROOT.name],check=True)
