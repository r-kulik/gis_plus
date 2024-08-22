import json

class JsonController:
    def __init__(self):
        with open("Las_handler/Json/eng_com.json", 'r') as json_file:
            self.eng_com = json.load(json_file)
            
        with open("Las_handler/Json/rus_com.json", 'r') as json_file:
            self.rus_com = json.load(json_file)
            
        with open("Las_handler/Json/eng.json", 'r') as json_file:
            self.eng = json.load(json_file)
            
        with open("Las_handler/Json/rus.json", 'r') as json_file:
            self.rus = json.load(json_file)
            
    def get_eng_com_element(self, mnemonic: str) -> str:
        return self.eng_com.get(mnemonic, "Element not found")
    
    def get_rus_com_element(self, mnemonic: str) -> str:
        return self.rus_com.get(mnemonic, "Element not found")
    
    def get_eng_origin_mnemonic(self, mnemonic: str) -> str:
        return self.eng.get(mnemonic, "Element not found")
    
    def get_rus_origin_mnemonic(self, mnemonic: str) -> str:
        return self.rus.get(mnemonic, "Element not found")
    
    def save(self):
        with open("Las_handler/Json/eng_com.json", 'w') as json_file:
            json.dump(self.eng_com, json_file)
            
        with open("Las_handler/Json/rus_com.json", 'w') as json_file:
            json.dump(self.rus_com, json_file)
            
        with open("Las_handler/Json/eng.json", 'w') as json_file:
            json.dump(self.eng, json_file)
            
        with open("Las_handler/Json/rus.json", 'w') as json_file:
            json.dump(self.rus, json_file)
    def add_new_line(self, ru, ru_com, en, en_com):
        try:
            if en in self.rus.keys() or ru in self.eng.keys():
                return "col"
            else:
                self.eng_com[en] = en_com
                self.rus_com[ru] = ru_com
                self.rus[en] = ru
                self.rus[ru] = ru
                self.eng[ru] = en
                self.eng[en] = en
                
                self.save()


                return "ok"
        except Exception as e:
            print(e)
            return "err"
        
    def add_sinonim(self, mnem, sinonim, is_rus):
        try:
            if is_rus:
                self.rus[sinonim] = mnem
            else:
                self.eng[sinonim] = mnem
            
            self.save()
            return "ok"
        except:
            return "err"
            
    def del_sinonim(self, sinonim, is_rus):
        try:
            if is_rus:
                del self.rus[sinonim]
            else:
                del self.eng[sinonim]
            
            self.save()
            return "ok"
        except:
            return "err"
            
if __name__ == "__main__":
    c = JsonController()
    c.add_sinonim("PS", "чтототам", False)
    c.del_sinonim("PS", "чтототам", False)
    print(c.eng["чтототам"])


