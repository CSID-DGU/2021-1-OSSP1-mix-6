import os
import sys
import shutil
import json
from settings import *

compile_error = False
runtime_error = False
usr_settings = json.loads(sys.argv[1])

f_output = os.open(OUTPUT_PATH, os.O_RDWR | os.O_CREAT)
f_log = os.open(COMPILE_LOG_PATH, os.O_RDWR | os.O_CREAT)
shutil.copy(USR_CODE_PATH, COMPLEXITY_PATH)

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
    # 사용자 설정 필요시 매개변수로 sys.argv[1] 전달
    # 총 결과 파일 초기화
    f_total = open(TOTAL_SCORE, 'w')
    f_total.close()

    # 입력 제어
    if usr_settings['inputAnalysisEnable']:
        pid_judge_input = os.fork()
        if pid_judge_input == 0:
            os.execl(PYTHON_PATH, "python3", JUDGE_INPUT_PATH, sys.argv[1])
        os.waitpid(pid_judge_input, 0)

    # 순환복잡도 분석
    if usr_settings['complexityAnalysisEnable']:
        pid_complex = os.fork()
        if pid_complex == 0:
            os.execl(PYTHON_PATH, "python3", SCANNER_PATH)
        os.waitpid(pid_complex, 0)

    # 의존성 분석
    if usr_settings['dependenceAnalysisEnable']:
        pid_complex = os.fork()
        if pid_complex == 0:
            os.execl(PYTHON_PATH, "python3", DEPENDENCY_JUDGE_PATH)
        os.waitpid(pid_complex, 0)

    # 매개변수 분석
    if usr_settings['parameterAnalysisEnable']:
        pid_complex = os.fork()
        if pid_complex == 0:
            os.execl(PYTHON_PATH, "python3", GET_PARAMETER)
        os.waitpid(pid_complex, 0)

    # 네이밍 분석
    if usr_settings['namingAnalysisEnable']:
        pid_complex = os.fork()
        if pid_complex == 0:
            os.execl(PYTHON_PATH, "python3", NAMING_JUDGE_PATH, sys.argv[1])
        os.waitpid(pid_complex, 0)

    # 중첩복잡도 분석
    if usr_settings['duplicationAnalysisEnable']:
        pid_repeat = os.fork()
        if pid_repeat == 0:
            os.execl(PYTHON_PATH, "python3", REPEAT_JUDGE_PATH)
        os.waitpid(pid_repeat, 0)
    
    # 실행시간 측정
    if usr_settings['timeMemoryAnalysisEnable']:
        pid_time = os.fork()
        if pid_time == 0:
            os.execl(PYTHON_PATH, "python3", GET_TIME, sys.argv[1])
        os.waitpid(pid_time, 0)

    # 메모리 측정
    if usr_settings['timeMemoryAnalysisEnable']:
        pid_memory = os.fork()
        if pid_memory == 0:
            os.execl(PYTHON_PATH, "python3", GET_MEMORY, sys.argv[1])
        os.waitpid(pid_memory, 0)

    # 코드중복 분석
    if usr_settings['duplicationCodeAnalysisEnable']:
        pid_complex = os.fork()
        if pid_complex == 0:
            os.execl(PYTHON_PATH, "python3", GET_DUPLICATION_PATH)
        os.waitpid(pid_complex, 0)

    # 단순 실행 파트
    # fd = os.fdopen(f_output, "w")

    ## 텍스트 파일 내용 초기화
    # open(OUTPUT_PATH, 'w').close()

    # os.dup2(fd.fileno(), sys.stdout.fileno())
    # os.close(fd.fileno())
    # os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)
