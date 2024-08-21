import os
import random
import lasio
try:
    from Las_handler.LasEncoder import LasEncoder
    from Las_handler.Checker import LASchecker
except ModuleNotFoundError:
    from LasEncoder import LasEncoder
    from Checker import LASchecker

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

# Function to generate a LAS file with issues
def generate_las_file(file_path, issues):
    las = lasio.LASFile()
    
    if "missing_necessary_sections" in issues:
        sections_to_remove = random.sample(necessary_sections, random.randint(1, len(necessary_sections) - 1))
        for section in sections_to_remove:
            if section in las.sections:
                del las.sections[section]
    
    for section in necessary_sections:
        if section in las.sections:
            if "missing_necessary_mnemonics" in issues:
                mnemonics_to_remove = random.sample(necessary_mnemonics[section], random.randint(1, len(necessary_mnemonics[section])))
                for mnemonic in mnemonics_to_remove:
                    for item in las.sections[section]:
                        if item.mnemonic == mnemonic:
                            las.sections[section].remove(item)
                            break
    
    if "other_problems" in issues:
        # Add some random data or misconfigurations
        las.append_curve("RAND", [random.random() for _ in range(100)], unit="RAND")
    
    las.write(file_path)

# Generate 200 LAS files with different issues
for i in range(200):
    file_path = os.path.join(output_dir, f'file_{i+1:03d}.las')
    selected_issues = random.sample(issues, random.randint(1, len(issues)))
    generate_las_file(file_path, selected_issues)

print(f"Generated 200 LAS files with various issues in the directory: {output_dir}")