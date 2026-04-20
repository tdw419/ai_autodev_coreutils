"""Carry forward -- session continuity gate for autonomous loops.

This package wraps the carry_forward module so it's importable
the same way as the original flat module.
"""

import sys
import os

# Import the actual module and re-export everything at package level
# This preserves the original API: import carry_forward; carry_forward.DB_PATH
from . import carry_forward as _cf

# Re-export all public names
_PUBLIC = [name for name in dir(_cf) if not name.startswith('_')]
_globals = globals()
for _name in _PUBLIC:
    _globals[_name] = getattr(_cf, _name)

# Ensure module-level attribute access works for mock.patch.object
# (the mock patches carry_forward.X, which needs to resolve to this package)
