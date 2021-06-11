import os
import signal
import sys
import json
sys.path.append(os.path.abspath('./'))
from settings import *

total = 0
error = 0
current_pid = 0
sig_triggered = False

input_num = 5
input_string = 5

usr_settings = json.loads(sys.argv[1])
timeout = usr_settings['inputTimeout']
input_type = usr_settings['inputType']


def timer_handler(signum, frame):
    global sig_triggered
    sig_triggered = True
    os.kill(current_pid, signal.SIGINT)


def test_input(type_str, iter):
    global total, error, current_pid, sig_triggered
    pid_list = []

    for i in range(iter):
        total += 1
        signal.signal(signal.SIGALRM, timer_handler)
        pid = os.fork()
        pid_list.append(pid)

        if pid == 0:
            filepath = INPUT_DIR_PATH + "input" + type_str + str(i) + ".txt"
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
        current_pid = pid_list[i]
        signal.alarm(timeout)
        info = os.waitpid(current_pid, 0)
        exit_code = os.WEXITSTATUS(info[1])

        if sig_triggered:
            error += 1
            sig_triggered = False
        else:
            if exit_code != 0:
                error += 1


if input_type == 'all':
    test_input("_num", input_num)
    test_input("_string", input_string)
elif input_type == 'number':
    test_input("_num", input_num)
elif input_type == 'string':
    test_input("_string", input_string)


input_score = 100.0
if total != 0:
    input_score = (total - error) / total  * 100

error_result = "Input Test Success : " + str(input_score)
# print(error_result)
f_out = open(INPUT_TEST_RESULT, 'w')
f_out.write(error_result)
f_out.close()

f_total = open(TOTAL_SCORE, 'a')
f_total.write(str(input_score) + '\n')
f_total.close()
