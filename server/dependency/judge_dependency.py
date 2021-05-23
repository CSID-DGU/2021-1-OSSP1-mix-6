from ast_dump import *
sys.path.append(os.path.abspath('./'))
from settings import *


file_path = USR_CODE_PATH
# file_path = "main.cpp"
dp = Dependency(file_path)
dp.save_result()
