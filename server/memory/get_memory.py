import os
import signal
import sys
import time
import psutil
import resource
import json

sys.path.append(os.path.abspath('./'))
from settings import *

usr_settings = json.loads(sys.argv[1])
timeout = usr_settings['timeMemoryAnalysisTimeout']
input = usr_settings['timeMemoryAnalysisInput']['stdin']

f_input = open(MEMORY_INPUT_PATH, 'w')
f_input.write(input)
f_input.close()

error = False
isTimeout = False
test_pid = 0
sig_triggered = False


def timer_handler(signum, frame):
    global sig_triggered
    sig_triggered = True
    os.kill(test_pid, signal.SIGINT)


def memory_analysis():
    global error, test_pid, sig_triggered, isTimeout

    memory_result = "Memory Usage : "

    mem_out = open(MEMORY_RESULT_PATH, 'w')
    mem_out.write("init")
    mem_out.close()

    current_pid = pid = os.fork()

    if pid == 0:
        signal.signal(signal.SIGALRM, timer_handler)
        test_pid = pid2 = os.fork()

        if pid2 == 0:
            filepath = MEMORY_INPUT_PATH
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
        info = os.waitpid(test_pid, 0)
        exit_code = os.WEXITSTATUS(info[1])

        mem_out = open(MEMORY_RESULT_PATH, 'w')

        if sig_triggered:
            print("Timeout")
            mem_out.write("Timeout")
        elif exit_code != 0:
            mem_out.write("Error")

        mem_out.close()

    else:
        os.waitpid(current_pid, 0)

        info = resource.getrusage(resource.RUSAGE_CHILDREN)
        execution_memory = info.ru_maxrss / 1024
        execution_memory = str(round(execution_memory, 5))

        mem_out = open(MEMORY_RESULT_PATH, 'r')
        check = mem_out.read()
        mem_out.close()

        if check == "Timeout":
            isTimeout = True
            memory_result += "Timeout"
        elif check == "Error":
            error = True
            memory_result += "Error Occurred"
        elif check == "init":
            memory_result += "Error Occurred"
        else:
            memory_result += (str(execution_memory) + " MB")

        mem_out = open(MEMORY_RESULT_PATH, 'w')
        mem_out.write(memory_result)
        mem_out.close()


memory_analysis()
