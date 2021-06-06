import os
import sys
import time
from clang import cindex

sys.path.append(os.path.abspath('./'))
from settings import *

# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
#cindex.Config.set_library_path("/usr/lib/llvm-11/lib/")
#cindex.Config.set_library_path("C:\python39-64\Lib\site-packages\clang\native")

# 도커 빌드 경로
cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-7.so.1")
#파라미터 개수 체크
class Time:
    start = time.time()
    
    def __init__(self,path):
        self.path = path
        self.func = ""

    def print_time(self):
        execution_time = time.time() - self.start 
        f = open(TIME_RESULT_PATH, "w")
        f.write("EXECUTION TIME :" + execution_time)
        f.close()
        print("EXECUTION TIME : " + execution_time)
  


