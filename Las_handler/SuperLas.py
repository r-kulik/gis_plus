import hashlib
import random 
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import lasio
import io


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
        
    def process_file1(self, file_path: str) -> dict:
        encoder = LasEncoder(file_path)
        new_name = encoder.update_encoding()
        print(new_name)
        
        checker = LASchecker(f"temp_files/{new_name}")
        result = checker.check()
        
        
        status = ''
        print(result)
        if len(result[0]) > 0:
            status = "error"
        elif len(result[0]) == 0 and len(result[1]) > 0:
            status = "warn"
        else:
            status = "ok"
            
                    
        if status != "error":
            curves = result[2].curves.keys()
            js = JsonController()
            rus = [curves[0]] + [js.get_rus_origin_mnemonic(i) for i in curves[1::]]    
            eng = [curves[0]] + [js.get_eng_origin_mnemonic(i) for i in curves[1::]]
            
            if "Element not found" in rus + eng:
                a = rus + eng
                er = a.index("Element not found")
                status = "error"
                
                result[0].append(f"Unknown mnemonic {curves[er]}")
                
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
                "file_path": None
            }
                
            else:
                features_sklad = {
                    "start_depth": float(result[2].well['STRT'].value),
                    "stop_depth": float(result[2].well['STOP'].value),
                    "version": str(result[2].version['VERS'].value),
                    "datetime": self.parse_date(result[2].well['DATE'].value),
                    "well": str(result[2].well['WELL'].value),
                    "company": None,
                    "fieldName" : result[2].well['FLD'].value,
                    "mnemonic_list_rus": rus,
                    "mnemonic_list_eng": eng,
                    "file_path": new_name
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
                "file_path": None
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
            for i in range(len(rus)):
                result[2].curves[i].mnemonic=rus[i]
            print(result[2].curves.keys())
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
    
    def get_image(self, file_name):
        try:
            # Step 1: Read the LAS file
            las_file_path = f"temp_files/{file_name}"
            las = lasio.read(las_file_path)

            # Step 2: Extract log data into a pandas DataFrame
            cur = las.curves
            labels = []
            for i in range(len(cur)):
                labels.append(f"{cur[i].mnemonic}, {cur[i].unit}")
            x_label = labels[0]
            y_labels = labels[1::]

            df = las.df()
            x = df.index
            df = df.reset_index(drop=True)
            curve_names = list(df.columns)
            num = len(y_labels)

            fig, axs = plt.subplots(1, num, figsize=(num * 4, 12), sharey=True)
            cmap = plt.get_cmap('tab10')  # You can choose any colormap you prefer

            if num != 1:
                for i in range(len(y_labels)):
                    axs[i].plot(df[curve_names[i]], x, color=cmap(i % 10))  # Note the swap of x and df[curve_names[i+1]]
                    axs[i].set_xlabel(y_labels[i])
                    axs[i].set_ylabel(x_label)
                    axs[i].grid(True)  # Add grid to each subplot
            else:
                for i in range(len(y_labels)):
                    axs.plot(df[curve_names[i]], x, color=cmap(i % 10))  # Note the swap of x and df[curve_names[i+1]]
                    axs.set_xlabel(y_labels[i])
                    axs.set_ylabel(x_label)
                    axs.grid(True)  # Add grid to the single subplot

            plt.gca().invert_yaxis()  # Invert the y-axis to show depth from top to bottom
            plt.tight_layout()
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)  # Reset the stream position to the beginning

            plt.close(fig)
            
            return img
        except:
            p = "file1.jpg"
            with open(p, "rb") as f:
                img = io.BytesIO(f.read())
            return img
    
    def translate(self, file):
        file_name = f"temp_files/{file}"
        new_name = f"{hashlib.md5(file.encode("utf-8")).hexdigest()}.las"
        las = lasio.read(file_name)
        names = las.curves.keys()
        js = JsonController()

        eng = [names[0]] + [js.get_eng_origin_mnemonic(i) for i in names[1::]]
        
        for i in range(len(eng)):
            las.curves[i].mnemonic=eng[i]
        with open(f"temp_files/{new_name}", "w" ,encoding="utf-8") as file:    
            las.write(file)
        
        return new_name




        
if __name__ == "__main__":
    c = SuperLas()
    print(c.translate("10_IK.las"))
    #c.get_image("42.las")
    """c = SuperLas()
        print(c.process_file1("15_2.las"))"""
    """import os
    relative_path = os.path.join('temp_files')

    absolute_path = os.path.abspath(relative_path)


    # Iterate through the files in the directory
    for filename in os.listdir(absolute_path):
        print(filename)
        print(c.process_file1(filename))"""
