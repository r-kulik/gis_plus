import os
import os
import random
import lasio
try:
    from Las_handler.LasEncoder import LasEncoder
    from Las_handler.Checker import LASchecker
except ModuleNotFoundError:
    from LasEncoder import LasEncoder
    from Checker import LASchecker

import os
import random
import lasio

# Define the directory to save the LAS files
output_dir = 'generated_las_files'
os.makedirs(output_dir, exist_ok=True)

# Define the possible issues
issues = [
    "missing_necessary_sections",
    "missing_necessary_mnemonics",
    "other_problems"
]

# Define necessary sections and mnemonics
necessary_sections = ["Version", "Well", "Curves", "Parameter", "Other"]
necessary_mnemonics = {
    "Version": ["VERS", "WRAP"],
    "Well": ["STRT", "STOP", "STEP", "NULL", "COMP", "WELL", "FLD", "LOC", "SRVC"],
    "Curves": ["DEPT", "GR", "ILD"],
    "Parameter": [],
    "Other": []
}

# Function to generate a LAS file content with issues
def generate_las_content(issues):
    content = ""
    
    if "missing_necessary_sections" in issues:
        sections_to_remove = random.sample(necessary_sections, random.randint(1, len(necessary_sections) - 1))
    else:
        sections_to_remove = []
    
    for section in necessary_sections:
        if section not in sections_to_remove:
            content += f"~{section} \n"
            if "missing_necessary_mnemonics" in issues and section in necessary_mnemonics:
                mnemonics_to_remove = random.sample(necessary_mnemonics[section], random.randint(0, len(necessary_mnemonics[section])))
            else:
                mnemonics_to_remove = []
            
            for mnemonic in necessary_mnemonics[section]:
                if mnemonic not in mnemonics_to_remove:
                    content += f"{mnemonic}. . : Description\n"
    
    if "other_problems" in issues:
        # Add some random data or misconfigurations
        content += "~Other\n"
        content += "RAND.RAND : Random Data\n"
    
    return content

# Generate 200 LAS files with different issues
for i in range(200):
    file_path = os.path.join(output_dir, f'file_{i+1:03d}.las')
    selected_issues = random.sample(issues, random.randint(1, len(issues)))
    las_content = generate_las_content(selected_issues)
    
    with open(file_path, 'w') as f:
        f.write(las_content)

print(f"Generated 200 LAS files with various issues in the directory: {output_dir}")