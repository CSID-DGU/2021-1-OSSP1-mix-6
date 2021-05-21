import os
import sys
sys.path.append(os.path.abspath('./'))
from settings import *

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
        # print("Input"+str(i)+" : " + open(filepath, 'r').read())
        # 텍스트 파일을 입력으로
        os.dup2(fd.fileno(), sys.stdin.fileno())
        os.close(fd.fileno())
        
        # 출력 음소거
        stdout_origin = sys.stdout
        devnull = os.open(os.devnull, os.O_WRONLY)
        fd_null = os.fdopen(devnull, "w")
        os.dup2(fd_null.fileno(), sys.stdout.fileno())
        os.close(fd_null.fileno())

        os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)

for i in range(iter):
    info = os.waitpid(pid_list[i], 0)
    exit_code = os.WEXITSTATUS(info[1])
    if exit_code != 0:
        error += 1

error_result = "Input Test Success : " +  str(iter - error)+'/'+str(iter)
# print(error_result)
f_out = open(INPUT_TEST_RESULT, 'w')
f_out.write(error_result)
f_out.close()


