import os
import sys
import json
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
class paraCounter:
    Over_count = 0.0
    Normal_count = 0.0
    p_count = 0.0
    
    def __init__(self,path):
        self.path = path
        self.func = ""
        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.find_param(tu.cursor)

    def find_param(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL):
            self.func = node.spelling
            self.Normal_count += 1.0
            self.p_count = 0.0
        
        if (node.kind == cindex.CursorKind.PARM_DECL):
            self.p_count += 1.0
            if(self.p_count > 3.0):
                self.Over_count += 1.0
                f_out = open(PARAMETER_RESULT_PATH,'w')
                f_out.write("OverParameter Function : " + self.func)
                f_out.close()
               
        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.find_param(child)
            else:
                continue
    
    def print_result(self):
        point = ((self.Normal_count-self.Over_count)/self.Normal_count) * 100 
        f_out = open(PARAMETER_RESULT_PATH,'w')
        f_out.write("PARAMETER POINT : " + str(point))
        f_out.close()


