import os
import sys
from settings import *

compile_error = False
runtime_error = False

f_output = os.open(OUTPUT_PATH, os.O_RDWR | os.O_CREAT)
f_log = os.open(COMPILE_LOG_PATH, os.O_RDWR | os.O_CREAT)

pid = os.fork()
if pid == 0:
    # C++ 코드 컴파일 단계
    fd = os.fdopen(f_log, "w")

    ## 텍스트 파일 내용 초기화
    open(COMPILE_LOG_PATH, 'w').close()

    os.dup2(fd.fileno(), sys.stderr.fileno())
    os.close(fd.fileno())
    os.execl(GPP_PATH, "g++", "-w", USR_CODE_PATH)

else:
    # 컴파일 후 실행 단계
    os.waitpid(pid, 0)

    compile_error = os.stat(COMPILE_LOG_PATH).st_size != 0

    if compile_error:
        sys.exit(111)

    fd = os.fdopen(f_output, "w")

    ## 텍스트 파일 내용 초기화
    open(OUTPUT_PATH, 'w').close()

    os.dup2(fd.fileno(), sys.stdout.fileno())
    os.close(fd.fileno())
    os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
