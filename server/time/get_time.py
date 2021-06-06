from time import *
sys.path.append(os.path.abspath('./'))
from settings import *

file_path = USR_CODE_PATH
get_time = Time(file_path)
get_time.print_result()