import sys
import clang.cindex

clang.cindex.Config.set_library_file("/usr/lib/llvm-7/lib/libclang-11.so.1")

def print_decl(node):
    if (node.kind == clang.cindex.CursorKind.FUNCTION_DECL):
        print ("\nfunc : ",end=" ")
        print (node.spelling)
    
    if (node.kind == clang.cindex.CursorKind.PARM_DECL):
        print ("parm : ",end=" ")
        print (node.spelling,end=" , ")

    for child in node.get_children():
        if(str(sys.argv[1]) == str(child.location.file)):
            print_decl(child)
        else:
            continue

index = clang.cindex.Index.create(False)
tu = index.parse(sys.argv[1])
print_decl(tu.cursor)