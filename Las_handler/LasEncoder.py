import chardet
import os
import hashlib


class LasEncoder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.dir_name = "temp_files"
        self.name = f"{self.dir_name}/{self.file_name}"
        
    def get_encoding(self):
        with open(self.name, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data[:10000])
            encoding = result['encoding']
            return encoding
        
    def space_clear(self, save_name):
        with open(f"{self.dir_name}/{save_name}.las", 'r', encoding='utf-8') as file:
            raw_data = file.read()
        with open(f"{self.dir_name}/{save_name}.las", 'w', encoding='utf-8') as file:
            data = raw_data.replace('\n\n', '\n')
            file.write(data)
        
    def update_encoding(self):
        with open(self.name, 'rb') as input_file:
            file_bytes = input_file.read()

        decoded_string = file_bytes.decode(self.get_encoding())
        #decoded_string = decoded_string.replace('\n', '')
        
        save_dir = "temp_files"
        save_name = hashlib.md5(self.file_name.encode("utf-8")).hexdigest()
        

        with open(f"{self.dir_name}/{save_name}.las", 'w', encoding='utf-8') as output_file:
            output_file.write(decoded_string)
            
        self.space_clear(save_name)
        
            
        return f"{save_name}.las"
    
    
        
        
