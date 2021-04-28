import os
import sys
from settings import *

compile_error = False
runtime_error = False

f_output = os.open(OUTPUT_PATH, os.O_RDWR | os.O_CREAT)
f_log = os.open(COMPILE_LOG_PATH, os.O_RDWR | os.O_CREAT)

pid = os.fork()
if pid == 0:
    # compile c++ code
    fd = os.fdopen(f_log, "w")
    
    # clear contents
    open(COMPILE_LOG_PATH, 'w').close()
    
    os.dup2(fd.fileno(), sys.stderr.fileno())
    os.close(fd.fileno())
    os.execl(GPP_PATH, "g++", "-w", USR_CODE_PATH)
    
else:       
    # execute user code
    os.waitpid(pid, 0)
    
    if compile_error:
       os.exit(1234)
    
    fd = os.fdopen(f_output, "w")
    
    # clear contents
    open(OUTPUT_PATH, 'w').close()
    
    os.dup2(fd.fileno(), sys.stdout.fileno())
    os.close(fd.fileno())
    os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
    
