import sys, os
from eclaircie import *

force = sys.argv[-1] == "1"

run("/home/jiba/src/eclaircie/example_site/conf.py", force)

