import os, sys
sys.path.append(os.path.abspath('./'))
from settings import *

os.chdir(COMPLEXITY_PATH)
os.system(COMPLEXITY_PATH + "complexity < " + USR_CODE_PATH)
