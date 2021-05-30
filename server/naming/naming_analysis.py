import os
import sys
import json
import re
from clang import cindex
sys.path.append(os.path.abspath('./'))
# from settings import *


# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
# cindex.Config.set_library_path("/usr/lib/llvm-11/lib")
cindex.Config.set_library_path("/home/dw/.local/lib/python3.8/site-packages/clang/native")

# 도커 빌드 경로
# cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-7.so.1")

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

# 결합도 분석
# 함수 내부에서 외부 클래스, 외부 함수, 재귀 사용할 때마다 결합도 1씩 증가
class Naming:
    def __init__(self, path):
        self.path = path

        lower_camel_case = re.compile('^[a-z]+(?:[A-Z][a-z]+)*$')
        pascal_case = re.compile('^[A-Z][a-z]+(?:[A-Z][a-z]+)*$')
        snake_case = re.compile('([A-Z]*_?[A-Z]*)*')

        self.var_pattern = snake_case
        self.func_pattern = lower_camel_case
        self.class_pattern = pascal_case

        self.var_name_set = set()
        self.func_name_set = set()
        self.class_name_set = set()

        self.var_unmatched = []
        self.func_unmatched = []
        self.class_unmatched = []

        index = cindex.Index.create(False)
        tu = index.parse(self.path)

        self.get_name_set(tu.cursor)
        self.func_name_set.remove('main')

        self.matching()

    def save_result(self):

        print("Var")
        print(self.var_name_set)
        print("Func")
        print(self.func_name_set)
        print("Class")
        print(self.class_name_set)

        print("unmatched var func class")
        print(self.var_unmatched)
        print(self.func_unmatched)
        print(self.class_unmatched)

        """high_dp = []
        func_str = ""
        for k, v in self.dependency_score.items():
            if v >= 5:
                high_dp.append((k, v))
                func_str += (k + ", ")

        total = len(self.dependency_score)
        bad = len(high_dp)

        total_result = "Dependecny Score: " + str(total - bad) + '/' + str(total)
        bad_func = ""
        if bad > 0:
            bad_func = "\nHigh Coupling Functions : " + func_str

        result = total_result + bad_func

        f_out = open(NAMING_RESULT_PATH, 'w')
        f_out.write(result)
        f_out.close()"""

    def get_name_set(self, node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL
                or node.kind == cindex.CursorKind.CXX_METHOD):
            self.func_name_set.add(node.spelling)

        if node.kind == cindex.CursorKind.CLASS_DECL:
            self.class_name_set.add(node.spelling)

        if node.kind == cindex.CursorKind.VAR_DECL:
            self.var_name_set.add(node.spelling)

        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.get_name_set(child)
            else:
                continue

    def matching(self):
        for s in self.var_name_set:
            m = self.var_pattern.match(s)
            if m is None:
                self.var_unmatched.append(s)

        for s in self.func_name_set:
            m = self.func_pattern.match(s)
            if m is None:
                self.func_unmatched.append(s)

        for s in self.class_name_set:
            m = self.class_pattern.match(s)
            if m is None:
                self.class_unmatched.append(s)

