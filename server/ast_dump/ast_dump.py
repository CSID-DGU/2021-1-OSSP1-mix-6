import sys
import json
from collections import OrderedDict
from clang import cindex

# libclang 파일 경로 바인딩
# 로컬 디버깅 경로
# cindex.Config.set_library_path("/usr/lib/llvm-11/lib/")
# 도커 빌드 경로
cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-7.so.1")

# 함수명과 파라미터 출력
class parameter:
    def __init__(self,path):
        self.path = path
        self.func = ""
        self.data = OrderedDict()

        index = cindex.Index.create(False)
        tu = index.parse(self.path)
        self.print_decl(tu.cursor)

    def print_json(self):
        with open("param.json","w") as make_file:
            json.dump(self.data, make_file, ensure_ascii=False, indent="\t")

    def print_decl(self,node):
        if (node.kind == cindex.CursorKind.FUNCTION_DECL):
            self.func = node.spelling
            self.data[self.func] = {}
            self.data[self.func]["type"] = node.type.spelling
            self.data[self.func]["parameter"] = {}
        
        if (node.kind == cindex.CursorKind.PARM_DECL):
            self.data[self.func]["parameter"][node.type.spelling] = node.spelling

        for child in node.get_children():
            if(str(self.path) == str(child.location.file)):
                self.print_decl(child)
            else:
                continue