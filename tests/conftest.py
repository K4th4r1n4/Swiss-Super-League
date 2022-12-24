import inspect
import os
import sys

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
sys.path.insert(0, os.path.dirname(current_dir))
