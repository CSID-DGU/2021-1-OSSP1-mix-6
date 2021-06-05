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

# ast 전체 출력
class ast:
    def __init__(self, path):
        self.path = path
        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.traverse(tu.cursor)

    def traverse(self, node, i=0):
        print('\t' * i, end="")
        print(node.kind, end="")
        print(" : ", end="")
        print(node.displayname, end="")
        print("")
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.traverse(child, i=i + 1)
            else:
                continue