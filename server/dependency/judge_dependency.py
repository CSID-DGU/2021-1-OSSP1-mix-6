from ast_dump import *

file_path = "../usr_code.cpp"
# file_path = "main.cpp"
param = parameter(file_path)
param.print_json()

decl = declaration(file_path)
decl.print_json()

# tree = ast(file_path)