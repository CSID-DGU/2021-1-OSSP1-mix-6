import sys
import json
from collections import OrderedDict
from clang import cindex

# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
# cindex.Config.set_library_path("/usr/lib/llvm-11/lib")
cindex.Config.set_library_path("/home/dw/.local/lib/python3.8/site-packages/clang/native")
# 도커 빌드 경로
# cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-7.so.1")

# ast 전체 출력
class ast:
    def __init__(self,path):
        self.path = path
        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.traverse(tu.cursor)

    def traverse(self,node, i=0):
        print('\t' * i,end="")
        print(node.kind, end="")
        print(" : ",end="")
        print(node.displayname,end="")
        print("")
        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.traverse(child, i=i+1)
            else:
                continue

# 함수명과 파라미터 출력 -> param.json
class parameter:
    def __init__(self,path):
        self.path = path
        self.func = ""
        self.data = OrderedDict()

        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.set_param(tu.cursor)

    def print_json(self):
        with open("result.json","w") as make_file:
            json.dump(self.data, make_file, ensure_ascii=False, indent="\t")

    def set_param(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL):
            self.func = node.spelling
            self.data[self.func] = {}
            self.data[self.func]["type"] = node.type.spelling
            self.data[self.func]["parameter"] = {}
        
        if (node.kind == cindex.CursorKind.PARM_DECL):
            self.data[self.func]["parameter"][node.type.spelling] = node.spelling

        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.set_param(child)
            else:
                continue

# 모든 선언의 타입과 네이밍 출력 -> decl.json
class declaration:
    def __init__(self,path):
        self.path = path
        self.line = 0
        self.data = OrderedDict()

        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.set_decl(tu.cursor)

    def print_json(self):
        with open("decl.json","w") as make_file:
            json.dump(self.data, make_file, ensure_ascii=False, indent="\t")

    def set_decl(self,node):
        if (node.kind.is_declaration()):
            self.line += 1
            idx = "decl" + str(self.line)
            self.data[idx] = {}
            self.data[idx]["type"] = node.type.spelling
            self.data[idx]["name"] = node.spelling

        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.set_decl(child)
            else:
                continue