import os
import sys
import json
from clang import cindex

sys.path.append(os.path.abspath('./'))
from settings import *

# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
# cindex.Config.set_library_path("/usr/lib/llvm-11/lib/")
# cindex.Config.set_library_path("C:\python39-64\Lib\site-packages\clang\native")
# cindex.Config.set_library_path("/home/dw/.local/lib/python3.8/site-packages/clang/native")


# 도커 빌드 경로
cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-7.so.1")

# 중복 개수 체크
class duplication:
    def __init__(self, path):
        self.path = path
        self.func = ""
        index = cindex.Index.create(False)
        tu = index.parse(self.path)

        self.duplication_count = 0.0
        self.max_line = 0
        self.nindex = 0

        self.get_line_num(tu.cursor)
        self.linetup1 = [[] for i in range(self.max_line + 10)]

        self.traverse(tu.cursor)
        self.dup_count()
        # self.find_duplication(tu.cursor)

    def get_line_num(self, node):
        if node.location.line > self.max_line:
            self.max_line = node.location.line
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.get_line_num(child)
            else:
                continue

    def traverse(self, node, i=0):
        self.linetup1[node.location.line].append(node.spelling)
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.traverse(child, i=i + 1)
            else:
                continue

    def dup_count(self):
        self.linetup1 = [ele for ele in self.linetup1 if ele != []] # 빈 리스트 제거
        # print(self.linetup1)
        sz = len(self.linetup1)
        for i in range(sz - 1):
            for j in range(i + 1, sz):
                if self.linetup1[i] == self.linetup1[j]:
                    self.duplication_count += 1

    def print_result(self):
        point = 100.0
        print(self.duplication_count)
        if self.max_line != 0:
            point = max(0, point - self.duplication_count)

        f_out = open(DUPLICATION_RESULT_PATH, 'w')
        f_out.write("Duplication Score : " + str(point))
        f_out.close()

        f_total = open(TOTAL_SCORE, 'a')
        f_total.write(str(point) + '\n')
        f_total.close()

    """
    def find_duplication(self, node):
        if node.kind == cindex.CursorKind.FUNCTION_DECL:
            self.func = node.spelling

        if node.kind == cindex.CursorKind.PARM_DECL:
            self.duplication_count += 1.0
            if self.duplication_count:
                f_out = open(DUPLICATION_RESULT_PATH, 'w')
                f_out.write("Duplication : " + self.func)
                f_out.close()

        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.find_duplication(child)
            else:
                continue
    """
