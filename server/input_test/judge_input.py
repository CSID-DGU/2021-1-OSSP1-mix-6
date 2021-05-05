import os
import sys
sys.path.append(os.path.abspath('./'))
from settings import *

print("start input judge")
error = 0
iter = 3

pid_list = []
for i in range(iter):
    pid = os.fork()
    pid_list.append(pid)
    if pid == 0:
        filepath = INPUT_DIR_PATH + "input"+str(i)+".txt"
        f_in = os.open(filepath, os.O_RDWR | os.O_CREAT)
        fd = os.fdopen(f_in, "w")
    	
        stdin_origin = sys.stdin
        print("Input"+str(i)+" : " + open(filepath, 'r').read())
        os.dup2(fd.fileno(), sys.stdin.fileno())
        os.close(fd.fileno())
        os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)

for i in range(iter):
    info = os.waitpid(pid_list[i], 0)
    exit_code = os.WEXITSTATUS(info[1])
    if exit_code != 0:
        error += 1
'''
pid = os.fork()
    
if pid == 0:
    for i in range(iter):
        filepath = INPUT_DIR_PATH + "input"+str(i)+".txt"
        f_in = os.open(filepath, os.O_RDWR | os.O_CREAT)
        fd = os.fdopen(f_in, "w")
    	
        stdin_origin = sys.stdin
        print("Input"+str(i)+" : " + open(filepath, 'r').read())
        os.dup2(fd.fileno(), sys.stdin.fileno())
        os.close(fd.fileno())
        os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
else:
    for i in range(iter):
        info = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(info[1])
        if exit_code != 0:
            error += 1
'''
# print("Error num : ")
# print(error)

