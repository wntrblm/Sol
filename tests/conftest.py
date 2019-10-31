import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
STUBS = os.path.join(HERE, "stubs")
LIB = os.path.join(ROOT, "lib")

# Insert import stubs directory into sys.path.
sys.path.insert(1, STUBS)

# Insert libs into sys.path
for path in os.listdir(LIB):
    sys.path.insert(1, os.path.join(LIB, path))
