import os, sys
sys.path.append(os.path.abspath('./'))
from settings import *

os.chdir(HOME_PATH + "complexity")
os.system("make")
os.system(COMPLEXITY_PATH + "complexity < " + USR_CODE_PATH)
