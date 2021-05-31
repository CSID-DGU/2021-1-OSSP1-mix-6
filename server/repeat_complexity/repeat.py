import os
import sys
import re
from clang import cindex

sys.path.append(os.path.abspath('./'))
from settings import *


# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
# cindex.Config.set_library_path("/usr/lib/llvm-11/lib")
# cindex.Config.set_library_path("/home/dw/.local/lib/python3.8/site-packages/clang/native")


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
        print(node.displayname, end=" ")
        print(node.location.line, end="")
        print("")
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.traverse(child, i=i + 1)
            else:
                continue
class Repeat:
    def __init__(self, path):
        self.path = path
        self.repeat = 0
        self.idx = 0
        self.over_repeat = 0
        self.item = 0
        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.get_loop(tu.cursor)
        self.get_over_repeat()
    
    def get_over_repeat(self):
        print("over_reapet : ",self.over_repeat)
        print("num_of_item : ",self.item)
        f = open("repeat_result.txt", "w")
        f.write("Repeat Comlexity Score : " + str(self.over_repeat) + "/" + str(self.item))

    def get_loop(self, node, i=0):
        if(node.kind == cindex.CursorKind.FOR_STMT 
            or node.kind == cindex.CursorKind.WHILE_STMT
            or node.kind == cindex.CursorKind.IF_STMT
            or node.kind == cindex.CursorKind.CASE_STMT):
            if(self.repeat == 0):
                self.repeat = 1
                self.item += 1
                self.idx = i
            else:
                self.repeat += 1
            print('\t' * i, end="")
            print("loop in : ",end="")
            print(node.kind,end="")
            print(node.location.line)
            for child in node.get_children():
                if str(self.path) == str(child.location.file):
                    self.get_loop(child, i=i + 1)
                else:
                    continue
            print('\t' * i, end="")
            print("loop out ",end="")
            print(node.location.line,end=" ")
            print("repeat : ",self.repeat)
            if(self.idx == i):
                if(self.repeat > 4):
                    self.over_repeat += 1
                self.repeat = 0
        else:
            for child in node.get_children():
                if str(self.path) == str(child.location.file):
                    self.get_loop(child, i=i + 1)
                else:
                    continue
            