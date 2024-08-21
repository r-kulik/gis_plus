import hashlib
import random 
try:
    from Las_handler.LasEncoder import LasEncoder
    from Las_handler.Checker import LASchecker
except ModuleNotFoundError:
    from LasEncoder import LasEncoder
    from Checker import LASchecker

class SuperLas:
    def __init__(self):
        pass
    
    def process_file(self, file_path: str) -> dict:
        encoder = LasEncoder(file_path)
        new_name = encoder.update_encoding()
        return {"status" : random.choice(["ok", "warn", "error"]),  # Это — глобальный статус результата процессинга. Если случился как минимум один warning — глобальный статус хотя бы "warn", если есть хоть один fatal error — глобальный статус равен "error" Сейчас рандомно для теста, потом по умному.
                "description": "Всё отлично",
                "features": 
                    {
                        "start_depth": 100,
                        "stop_depth": 1000,
                        "version": "1.1",
                        "datetime": None,
                        "company": random.choice([
                            "Шизпром",
                            "ШизГаз Уфа",
                            "булкин и ко ко ко",
                            "Ш.У.Е. Ltd"
                        ]),
                        "fieldName": random.choice([
                            "Урен-гой",
                            "Хаханты-манстйск",
                            "Бульба",
                            "Булкинасс",
                            "Место Х"
                        ]),
                        "well": str(
                            random.randint(100, 1000)
                        ),
                        "mnemonic_list_rus": ['ПС', "ИН", "A"],
                        "mnemonic_list_eng": ['D', "O", "G"],
                        "file_path": new_name,
                    },
                "errors": [
                    {
                        "status": random.choice(["warn", "error"]),
                        "description": "LoremIsplum dolor sit amet"
                    },
                    {
                        "status": random.choice(["warn", "error"]),
                        "description": "LoremIsplum dolor sit amet"
                    },
                    {
                        "status": random.choice(["warn", "error"]),
                        "description": "LoremIsplum dolor sit amet"
                    },
                    {
                        "status": random.choice(["warn", "error"]),
                        "description": "LoremIsplum dolor sit amet"
                    },
                    {
                        "status": random.choice(["warn", "error"]),
                        "description": "LoremIsplum dolor sit amet"
                    }
                ]
        }
        
    def process_file1(self, file_path: str) -> dict:
        encoder = LasEncoder(file_path)
        new_name = encoder.update_encoding()
        
        checker = LASchecker(f"temp_files/{new_name}")
        result = checker.check()
        return result
        
if __name__ == "__main__":
    c = SuperLas()
    print(c.process_file1("10_IK.las"))
    
