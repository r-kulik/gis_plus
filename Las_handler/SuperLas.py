import hashlib
import random 
import re
from datetime import datetime

try:
    from Las_handler.LasEncoder import LasEncoder
    from Las_handler.Checker import LASchecker
    from Las_handler.JsonController import JsonController
except ModuleNotFoundError:
    from LasEncoder import LasEncoder
    from Checker import LASchecker
    from JsonController import JsonController

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
        
        
        status = ''
        if len(result[0]) > 0:
            status = "error"
        elif len(result[0]) == 0 and len(result[1]) > 0:
            status = "warn"
        else:
            status = "ok"
            
            
        
        # TODO replace mnemonics
        
        if status != "error":
            curves = result[2].curves.keys()
            js = JsonController()
            rus = [curves[0]] + [js.get_rus_origin_mnemonic(i) for i in curves[1::]]    
            eng = [curves[0]] + [js.get_eng_origin_mnemonic(i) for i in curves[1::]]
            
            if "Element not found" in rus + eng:
                status = "error"
                
                result[0].append("Unknown mnemonic")
                
                features_sklad = {
                "start_depth": None,
                "stop_depth": None,
                "version": None,
                "datetime": None,
                "well": None,
                "company": None,
                "fieldName" : None,
                "mnemonic_list_rus": None,
                "mnemonic_list_eng": None,
            }
                
            else:
                features_sklad = {
                    "start_depth": result[2].well['STRT'].value,
                    "stop_depth": result[2].well['STOP'].value,
                    "version": result[2].version['VERS'].value,
                    "datetime": self.parse_date(result[2].well['DATE'].value),
                    "well": result[2].well['WELL'].value,
                    "company": None,
                    "fieldName" : result[2].well['FLD'].value,
                    "mnemonic_list_rus": rus,
                    "mnemonic_list_eng": eng,
                }
                if 'SRVC' in result[2].well.keys() and result[2].well["SRVC"].value != '':
                    features_sklad["company"] = result[2].well["SRVC"].value
        else:
                        features_sklad = {
                "start_depth": None,
                "stop_depth": None,
                "version": None,
                "datetime": None,
                "well": None,
                "company": None,
                "fieldName" : None,
                "mnemonic_list_rus": None,
                "mnemonic_list_eng": None,
            }
            
            
        errors = []
        
        for i in result[0]:
            errors.append({"status": "error", "description": i})
        for i in result[1]:
            errors.append({"status": "warn", "description": i})
        
        
        report = {"status": status,
                  "description": status, 
                  "features" : features_sklad,
                  "errors": errors}
        
        
        if status != "error":
            with open(f"temp_files/{new_name}", "w" ,encoding="utf-8") as file:    
                result[2].write(file)
            
        return report
    


    def parse_date(self, date_str):
        # Define possible date formats and their corresponding regex patterns
        formats = [
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%d-%m-%Y'),  # day-month-year
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})', '%d-%m-%y'),  # day-month-year (2-digit year)
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%m-%d-%Y'),  # month-day-year
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})', '%m-%d-%y'),  # month-day-year (2-digit year)
        (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', '%Y-%m-%d'),  # year-month-day
        (r'(\d{2})[/-](\d{1,2})[/-](\d{1,2})', '%y-%m-%d'),  # year-month-day (2-digit year)
        (r'(\d{1,2})[.-](\d{1,2})[.-](\d{4})', '%d-%m-%Y'),  # day-month-year with dots
        (r'(\d{1,2})[.-](\d{1,2})[.-](\d{2})', '%d-%m-%y'),  # day-month-year (2-digit year) with dots
        (r'(\d{1,2})[.-](\d{1,2})[.-](\d{4})', '%m-%d-%Y'),  # month-day-year with dots
        (r'(\d{1,2})[.-](\d{1,2})[.-](\d{2})', '%m-%d-%y'),  # month-day-year (2-digit year) with dots
        (r'(\d{4})[.-](\d{1,2})[.-](\d{1,2})', '%Y-%m-%d'),  # year-month-day with dots
        (r'(\d{2})[.-](\d{1,2})[.-](\d{1,2})', '%y-%m-%d'),  # year-month-day (2-digit year) with dots
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', '%d-%m-%Y'),  # day-month-year with periods
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', '%d-%m-%y'),  # day-month-year (2-digit year) with periods
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', '%m-%d-%Y'),  # month-day-year with periods
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', '%m-%d-%y'),  # month-day-year (2-digit year) with periods
        (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', '%Y-%m-%d'),  # year-month-day with periods
        (r'(\d{2})\.(\d{1,2})\.(\d{1,2})', '%y-%m-%d'),  # year-month-day (2-digit year) with periods
        (r'(\d{1,2}) (\d{1,2}) (\d{4})', '%d-%m-%Y'),  # day-month-year with spaces
        (r'(\d{1,2}) (\d{1,2}) (\d{2})', '%d-%m-%y'),  # day-month-year (2-digit year) with spaces
        (r'(\d{1,2}) (\d{1,2}) (\d{4})', '%m-%d-%Y'),  # month-day-year with spaces
        (r'(\d{1,2}) (\d{1,2}) (\d{2})', '%m-%d-%y'),  # month-day-year (2-digit year) with spaces
        (r'(\d{4}) (\d{1,2}) (\d{1,2})', '%Y-%m-%d'),  # year-month-day with spaces
        (r'(\d{2}) (\d{1,2}) (\d{1,2})', '%y-%m-%d'),  # year-month-day (2-digit year) with spaces
    ]

        for pattern, date_format in formats:
            match = re.match(pattern, date_str)
            if match:
                day, month, year = match.groups()
                try:
                    return datetime.strptime(f'{day}-{month}-{year}', date_format)
                except ValueError:
                    return None


        
if __name__ == "__main__":
    c = SuperLas()
    print(c.process_file1("10_IK.las"))