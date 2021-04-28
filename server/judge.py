import os
import sys
from settings import *

f_out = os.open(OUTPUT_PATH, os.O_RDWR | os.O_CREAT)

pid = os.fork()
if pid == 0:
    os.execl(GPP_PATH, "g++", USR_CODE_PATH)
else:
    os.waitpid(pid, 0)
    fd = os.fdopen(f_out, "w")
    # clear contents
    open(OUTPUT_PATH, 'w').close()
    
    os.dup2(fd.fileno(), sys.stdout.fileno())
    os.close(fd.fileno())
    os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
