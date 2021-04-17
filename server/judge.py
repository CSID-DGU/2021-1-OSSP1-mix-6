import os
import sys

f_out = os.open('/app/output.txt', os.O_RDWR | os.O_CREAT)

pid = os.fork()
if pid == 0:
    os.execl("/usr/bin/g++", "g++", "/app/usr_code.cpp")
else:
    os.waitpid(pid, 0)
    fd = os.fdopen(f_out, "w")
    open('/app/output.txt', 'w').close()
    os.dup2(fd.fileno(), sys.stdout.fileno())
    os.close(fd.fileno())
    os.execl("/app/a.out", "/app/a.out")
