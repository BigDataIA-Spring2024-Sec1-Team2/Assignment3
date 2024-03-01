
from utility import Utility
import os

Utility.upload_text_files_to_s3_root(os.getcwd()+"/output_data")
print('yolo')