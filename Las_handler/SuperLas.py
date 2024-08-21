import random 
from LasEncoder import LasEncoder

class SuperLas:
    def __init__(self):
        pass
    
    def process_file(self, file_path: str) -> dict:
        return {"status" : random.choice(["ok", "warn", "error"]),  # Это — глобальный статус результата процессинга. Если случился как минимум один warning — глобальный статус хотя бы "warn", если есть хоть один fatal error — глобальный статус равен "error" Сейчас рандомно для теста, потом по умному.
                "description": "Всё отлично",
                "features": 
                    {
                        "start_depth": 100,
                        "stop_depth": 1000,
                        "version": "1.1",
                        "datetime": None,
                        "company": "Шазпром",
                        "well": "5555",
                        "mnemonic_list_rus": ['ПС', "ИН", "A"],
                        "mnemonic_list_eng": ['D', "O", "G"],
                        "file_path": "Encoded/1.las",
                        
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
        
    def process_file(self, file_path: str) -> dict:
        encoder = LasEncoder(file_path)
        new_name = encoder.update_encoding()