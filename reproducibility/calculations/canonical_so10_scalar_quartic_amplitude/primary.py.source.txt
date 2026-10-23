"""S4A1 full reference eigenvalue route."""
import runpy,sys
from pathlib import Path
sys.argv=[str(Path(__file__).with_name('pilot.py')),'primary']
runpy.run_path(sys.argv[0],run_name='__main__')
