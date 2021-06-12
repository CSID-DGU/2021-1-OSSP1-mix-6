from duplication import *
sys.path.append(os.path.abspath('./'))
from settings import *


file_path = USR_CODE_PATH
# file_path = "main.cpp"
para_count = paraCounter(file_path)
para_count.print_result()
