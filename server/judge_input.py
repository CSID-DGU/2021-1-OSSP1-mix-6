import os
import sys
from settings import *

print("start input judge")
error = 0
iter = 1

pid = os.fork()

if pid == 0:
    for i in range(iter):
    	filepath = INPUT_DIR_PATH + "input1.txt"
    	f_in = os.open(filepath, os.O_RDWR | os.O_CREAT)
    	fd = os.fdopen(f_in, "w")
    	
    	stdin_origin = sys.stdin

    	os.dup2(fd.fileno(), sys.stdin.fileno())
    	os.close(fd.fileno())
    	os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
else:
    for i in range(iter):
    	info = os.waitpid(pid, 0)
    	exit_code = os.WEXITSTATUS(info[1])
    	if exit_code != 0:
    	    error += 1

# print("Error num : ")
# print(error)

