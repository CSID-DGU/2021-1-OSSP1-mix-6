from naming_analysis import *
import json
sys.path.append(os.path.abspath('./'))
from settings import *

usr_settings = json.loads(sys.argv[1])
file_path = USR_CODE_PATH
# file_path = "main.cpp"
nm = Naming(file_path, usr_settings)
nm.save_result()
