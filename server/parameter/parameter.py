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
        #self.f_over = open("result2.txt",'w')
        #self.over = ""
        self.find_param(tu.cursor)

    def find_param(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL or
            node.kind == cindex.CursorKind.CXX_METHOD or 
            node.kind == cindex.CursorKind.CONSTRUCTOR):

            self.func = node.spelling
            self.Normal_count += 1.0
            self.p_count = 0.0
        
        for child in node.get_children():
                if (child.kind == cindex.CursorKind.PARM_DECL):
                    self.p_count += 1.0
                    if(self.p_count > 3.0):
                        self.Over_count += 1.0
                        # f_out = open(PARAMETER_RESULT_PATH,'w')
                        #self.over += "\nOverParameter Function : " + self.func
                        break

               
        else:
            for child in node.get_children():
                if(str(self.path) == str(child.location.file)):
                    self.find_param(child)
                else:
                    continue
    
    def print_result(self):
        #self.over += "\n" + str(self.Normal_count) + "\n" + str(self.Over_count)
        #self.f_over.write(self.over)
        point = 100.0
        if self.Normal_count != 0:
            point = ((self.Normal_count-self.Over_count)/self.Normal_count) * 100
            point = round(point,2)
        f_out = open(PARAMETER_RESULT_PATH,'w')
        #f_out = open("result.txt",'w')
        f_out.write("Parameter Score : " + str(point))
        f_out.close()

        f_total = open(TOTAL_SCORE, 'a')
        f_total.write(str(point) + '\n')
        f_total.close()



