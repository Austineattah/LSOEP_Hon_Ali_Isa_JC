from importlib.machinery import SourceFileLoader as _SourceFileLoader
from pathlib import Path as _Path
import sys as _sys

# Preserve the existing panels.py API while panels becomes a package.
_SourceFileLoader(
    __name__, str(_Path(__file__).resolve().parent.parent / "panels.py")
).exec_module(_sys.modules[__name__])

del _SourceFileLoader, _Path, _sys
