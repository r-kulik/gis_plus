import chardet
import os


class LasEncoder:
    def __init__(self, file_name, dir_name):
        self.file_name = file_name
        self.dir_name = dir_name
        self.name = f"{self.dir_name}/{self.file_name}"
        
    def get_encoding(self):
        with open(self.name, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            return encoding
        
    def update_encoding(self):
        with open(self.name, 'rb') as input_file:
            file_bytes = input_file.read()

        decoded_string = file_bytes.decode(self.get_encoding())
        decoded_string = decoded_string.replace('\n', '')
        
        save_dir = "Encoded"
        os.makedirs(save_dir, exist_ok=True)

        with open(f"{save_dir}/{self.file_name}", 'w', encoding='utf-8') as output_file:
            output_file.write(decoded_string)
        
        
