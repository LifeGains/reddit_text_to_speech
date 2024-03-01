import sys
import os
sys.path.append(r'C:\Users\kevin\Google Drive\My Drive\Github\Repos\generate_requirements_txt')
import generate_requirements_txt

output_file = os.getcwd() + "\\requirements.txt"
print(output_file)
generate_requirements_txt.generate_requirements(output_file)
