"""S4A1 parent Hessian reconstruction and physical SVD/Schur route."""
import runpy,sys
from pathlib import Path
sys.argv=[str(Path(__file__).with_name('pilot.py')),'replay']
runpy.run_path(sys.argv[0],run_name='__main__')
