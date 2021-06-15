from server.duplication.duplication import duplication
from duplication import *
sys.path.append(os.path.abspath('./'))
from settings import *


file_path = USR_CODE_PATH
# file_path = "main.cpp"
duplication_num = duplication(file_path)
duplication_num.print_result()
