import os
import sys
import json
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
        print(node.displayname, end="")
        print("")
        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.traverse(child, i=i + 1)
            else:
                continue


# 결합도 분석
# 함수 내부에서 외부 클래스, 외부 함수, 재귀 사용할 때마다 결합도 1씩 증가
class Dependency:
    def __init__(self, path):
        self.path = path
        self.func_name_set = set()
        self.dependency_score = {}

        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.get_name_set(tu.cursor)

        for i in self.func_name_set:
            self.dependency_score[i] = 0

        self.get_score(tu.cursor)

    def save_result(self):
        high_dp = []
        func_str = ""
        for k, v in self.dependency_score.items():
            if v >= 5:
                high_dp.append((k, v))
                func_str += (k + ", ")

        total = len(self.dependency_score)
        bad = len(high_dp)

        dp_score = 100.0
        if total != 0:
            dp_score = (total - bad) / total * 100

        total_result = "Dependency Score: " + str(dp_score)
        bad_func = ""
        if bad > 0:
            bad_func = "\nHigh Coupling Functions : " + func_str

        result = total_result + bad_func

        f_out = open(DEPENDENCY_RESULT_PATH, 'w')
        f_out.write(result)
        f_out.close()

    def get_name_set(self, node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL
                or node.kind == cindex.CursorKind.CXX_METHOD):
            self.func_name_set.add(node.spelling)

        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.get_name_set(child)
            else:
                continue

    def get_score(self, node, func_name=None):
        _func_name = func_name
        if (node.kind == cindex.CursorKind.FUNCTION_DECL
                or node.kind == cindex.CursorKind.CXX_METHOD):
            _func_name = node.spelling

        if (node.kind == cindex.CursorKind.OVERLOADED_DECL_REF
                or node.kind == cindex.CursorKind.CALL_EXPR):
            if func_name in self.func_name_set:
                self.dependency_score[func_name] += 1

        for child in node.get_children():
            if str(self.path) == str(child.location.file):
                self.get_score(child, _func_name)
            else:
                continue
