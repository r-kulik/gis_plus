import json

class JsonController:
    def __init__(self):
        with open("Json/eng_com.json", 'r') as json_file:
            self.eng_com = json.load(json_file)
            
        with open("Json/rus_com.json", 'r') as json_file:
            self.rus_com = json.load(json_file)
            
        with open("Json/eng.json", 'r') as json_file:
            self.eng = json.load(json_file)
            
        with open("Json/rus.json", 'r') as json_file:
            self.rus = json.load(json_file)
            
    def get_eng_com_element(self, mnemonic: str) -> str:
        return self.eng_com.get(mnemonic, "Element not found")
    
    def get_rus_com_element(self, mnemonic: str) -> str:
        return self.rus_com.get(mnemonic, "Element not found")
    
    def get_eng_origin_mnemonic(self, mnemonic: str) -> str:
        return self.eng.get(mnemonic, "Element not found")
    
    def get_rus_origin_mnemonic(self, mnemonic: str) -> str:
        return self.rus.get(mnemonic, "Element not found")