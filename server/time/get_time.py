import os
import signal
import sys
import time
import json
sys.path.append(os.path.abspath('./'))
from settings import *

usr_settings = json.loads(sys.argv[1])
timeout = usr_settings['timeMemoryAnalysisTimeout']
input = usr_settings['timeMemoryAnalysisInput']['stdin']

f_out = open(TIME_INPUT_PATH, 'w')
f_out.write(input)
f_out.close()

error = False
isTimeout = False
current_pid = 0
sig_triggered = False


def timer_handler(signum, frame):
    global sig_triggered
    sig_triggered = True
    os.kill(current_pid, signal.SIGINT)


def time_analysis():
    global error, current_pid, sig_triggered

    signal.signal(signal.SIGALRM, timer_handler)
    current_pid = pid = os.fork()
    start = time.time()
    if pid == 0:
        filepath = TIME_INPUT_PATH
        f_in = os.open(filepath, os.O_RDWR | os.O_CREAT)
        fd = os.fdopen(f_in, "w")

        stdin_origin = sys.stdin
        os.dup2(fd.fileno(), sys.stdin.fileno())
        os.close(fd.fileno())

        # 출력 음소거
        stdout_origin = sys.stdout
        devnull = os.open(os.devnull, os.O_WRONLY)
        fd_null = os.fdopen(devnull, "w")
        os.dup2(fd_null.fileno(), sys.stdout.fileno())
        os.close(fd_null.fileno())

        os.execl(OBJ_FILE_PATH, OBJ_FILE_PATH)

    signal.alarm(timeout)
    info = os.waitpid(current_pid, 0)

    execution_time = time.time() - start
    execution_time = round(execution_time, 6)

    exit_code = os.WEXITSTATUS(info[1])

    time_result = "Time Analysis : "
    if sig_triggered:
        isTimeout = True
        time_result += "Timeout"
    else:
        if exit_code != 0:
            error = True
            time_result += "Error Occurred"
        else:
            time_result += (str(execution_time) + " sec")

    f_out = open(TIME_RESULT_PATH, 'w')
    f_out.write(time_result)
    f_out.close()


time_analysis()
