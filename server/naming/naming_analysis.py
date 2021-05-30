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
    def __init__(self, path, settings):
        self.path = path

        self.var_pattern = re.compile(settings['namingRuleVariable'])
        self.func_pattern = re.compile(settings['namingRuleFunction'])
        self.class_pattern = re.compile(settings['namingRuleClass'])

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
        total = len(self.var_name_set) + len(self.func_name_set) + len(self.class_name_set)
        bad = len(self.var_unmatched) + len(self.func_unmatched) + len(self.class_unmatched)

        total_result = "Naming Score: " + str(total - bad) + '/' + str(total) + "\n"

        if bad > 0:
            bad_var = "  - variable : "
            bad_func = "  - function : "
            bad_class = "  - class : "

            for i in self.var_unmatched:
                bad_var += i + ", "
            for i in self.func_unmatched:
                bad_func += i + ", "
            for i in self.class_unmatched:
                bad_class += i + ", "

            bad_result = "- Unmatched Names\n" + bad_var + "\n" + bad_func + "\n" + bad_class
            total_result += bad_result

        f_out = open(NAMING_RESULT_PATH, 'w')
        f_out.write(total_result)
        f_out.close()

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
