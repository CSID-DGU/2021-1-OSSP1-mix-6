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

#중복 개수 체크
class duplication:
    duplication_count = 0.0
    linetup1 = ()
    nindex = 0

    def __init__(self,path):
        self.path = path
        self.func = ""
        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.find_duplication(tu.cursor)

    def find_duplication(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL):
            self.func = node.spelling
        
        if (node.kind == cindex.CursorKind.PARM_DECL):
            self.duplication_count += 1.0
            if(self.duplication_count):
                f_out = open(DUPLICATION_RESULT_PATH,'w')
                f_out.write("Duplication : " + self.func)
                f_out.close()
               
        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.find_duplication(child)
            else:
                continue
            
    def traverse(self, node, i=0):
        self.linetup1[self.nindex] += node.spelling
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.traverse(child, i=i + 1)
            else:
                continue


    def print_result(self):
        point = 100.0
        if self.duplication_count != 0:
            point = point - self.duplication_count
        
        f_out = open(DUPLICATION_RESULT_PATH,'w')
        f_out.write("Duplication Score : " + str(point))
        f_out.close()

        f_total = open(TOTAL_SCORE, 'a')
        f_total.write(str(point) + '\n')
        f_total.close()
