from ast_dump import *

file_path = "../usr_code.cpp"
# file_path = "main.cpp"
dp = Dependency(file_path)
dp.save_result()
