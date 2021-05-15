import os
import sys
import shutil
from settings import *

compile_error = False
runtime_error = False

f_output = os.open(OUTPUT_PATH, os.O_RDWR | os.O_CREAT)
f_log = os.open(COMPILE_LOG_PATH, os.O_RDWR | os.O_CREAT)
shutil.copy(USR_CODE_PATH,COMPLEXITY_PATH)

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
        
    ############ 분석 모듈 실행 부분 ############

    # 입력 제어
    pid_judge_input = os.fork()
    if pid_judge_input == 0:
    	os.execl(PYTHON_PATH, "python3", JUDGE_INPUT_PATH)
    os.waitpid(pid_judge_input, 0)

    # 복잡성 분석
    pid_complex = os.fork()
    if pid_complex == 0:
        os.execl(PYTHON_PATH, "python3", SCANNER_PATH)
    os.waitpid(pid_complex, 0)

    # 단순 실행 파트
    # fd = os.fdopen(f_output, "w")

    ## 텍스트 파일 내용 초기화
    # open(OUTPUT_PATH, 'w').close()

    # os.dup2(fd.fileno(), sys.stdout.fileno())
    # os.close(fd.fileno())
    # os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)