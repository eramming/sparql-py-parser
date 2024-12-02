import os
import sys
 
# Add folder to path
(parent_folder_path, _) = os.path.split(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
