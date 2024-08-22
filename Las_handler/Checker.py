import lasio.exceptions
import lasio
import sys
import statistics
import os
import math
import re


try:
    from Las_handler import lascheck
except ModuleNotFoundError:
    import lascheck

# Основной класс чекера. Служит для проверки соответствия формата .las файла
class LASchecker():
    def __init__(self, filepath: str):
        #super(LASchecker, self).__init__()
        try:
            self.filepath = filepath
            self.lascheck = lascheck.read(filepath, encoding='utf-8')
            self.las = lasio.read(filepath, encoding='utf-8')
            self.error = []
        except (lasio.exceptions.LASHeaderError, lasio.exceptions.LASDataError, lasio.exceptions.LASUnknownUnitError):
            exception_type, exception_value, exception_traceback = sys.exc_info()
            self.error = [str(exception_value), 'wrong format in this string'], [], None
        except Exception:
            self.error = [sys.exc_info()[0], ':', sys.exc_info()[1]], [], None

    # Рассчёт шага с помощью среднего (во избежание ошибки округления)
    def calculate_step(self):
        depth_values = self.las.curves[0].data
        differences = [depth_values[i+1] - depth_values[i] for i in range(len(depth_values) - 1)]
        return statistics.fmean(differences)
    
    # Создание поля шаг если отсутствует, его заполнение
    def step(self):
        if not 'STEP' in self.las.well.keys():
            self.las.well.append(lasio.HeaderItem('STEP', unit=self.las.well["STRT"].unit, value='', descr='Step'))
        if self.las.well['STEP'].value == '':
            self.las.well['STEP'].value = self.calculate_step()
            return ["Was not appropriate step. Calculated, choose step {}".format(self.las.well.step.value)]
        return []

    # Создание и заполнение поля STOP
    def stop(self):
        if not 'STOP' in self.las.well.keys():
            self.las.well.append(lasio.HeaderItem('STOP', unit=self.las.well["STRT"].unit, value='', descr='Stop'))
        if self.las.well['STOP'].value == '':
            self.las.well['STOP'].value = self.las.data[-1][0]
            return ["Was not appropriate stop value. Choose stop {}".format(self.las.data[-1][0])]
        return []
    # Создание и заполнение поля STRT
    def start(self):
        if not 'STRT' in self.las.well.keys():
            self.las.well.append(lasio.HeaderItem('STRT', unit=self.las.well["STOP"].unit, value='', descr='Start'))
        if self.las.well['STRT'].value == '':
            self.las.well['STRT'].value = self.las.data[0][0]
            return ["Was not appropriate start value. Choose start {}".format(self.las.data[0][0])]
        return []
    
    # Сверка числа мнемоник с количеством кривых в файле
    def amount_mnem_check(self):
        equal = (len(self.las.curves) == self.las.data.shape[1])
        for i in self.las.curves:
            if i.mnemonic == "UNKNOWN":
                equal = False
        return equal
    
    # Проверка дубликатов секций и того, что секция ~A завершает файл
    def check_sections(self):
        pattern = r'~.'
        with open(self.filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        matches = re.findall(pattern, text)
        doubles = list(set([x for x in matches if matches.count(x) > 1]))
        err = [("Duplicated section " + i) for i in doubles]
        if matches[-1] != '~A':
            err += ["~A should be a last section"]
        return err
    
    # Заполнение секции ~V если она есть
    def check_version(self):
        print(self.las.version.keys())
        warn = []
        if not "Version" in self.lascheck.sections.keys():
            warn += ['Err: Header section Version regexp=~V was not found. Will be created new ~V section.',\
                      'VERS item not found in the ~V section.',\
                        'WRAP item not found in the ~V section']
        if not 'VERS' in self.las.version.keys():
            self.las.version.append(lasio.HeaderItem('VERS', value=2.0, descr=': VERSION 2.0'))
            warn += ['VERS item not found in the ~V section']
        if not 'WRAP' in self.las.version.keys():
            self.las.version.append(lasio.HeaderItem('WRAP', value='NO', descr='Data Wrapping'))
            warn += ['WRAP item not found in the ~V section']
        return warn

    # Автоматическое создание секции NULL и заполнение её, обработка секций stop, step и start
    def check_well(self):
        warn = []
        if 'Well' in self.lascheck.sections.keys():
            if not 'NULL' in self.las.well.keys():
                self.las.well.append(lasio.HeaderItem('NULL', value=-9999.25, descr='Null value'))
                warn += ['NULL item not found in the ~W section']
            if not math.isclose(self.las.well['NULL'].value, -9999) and not \
                math.isclose(self.las.well['NULL'].value, -999.25) and not \
                math.isclose(self.las.well['NULL'].value, -9999.25):
                self.las.well['NULL'].value = '-9999.25'
                warn += ["Wrong NULL value. Should be -9999, -999.25 or -9999.25. Replaced to -9999.25"]
            warn+= self.step()
            warn+=self.stop()
            warn+=self.start()
        return warn

    # Основная функция проверки
    def check(self):
        if len(self.error) != 0:
            return self.error, [], None
        self.error = self.check_sections()
        if len(self.error) != 0:
            return self.error, [], None
        warns = self.check_version()
        warns += self.check_well()

        # Проверка на отсутствие обязательных секций
        for i in lascheck.spec.MandatorySections().get_missing_mandatory_sections(self.lascheck):
            self.error += ["Missing mandatory sections: {}".format(i)]
            return self.error, [], None
        
        # Проверка на непустой раздел ~A, сохранение временного файла (для дальнейшего использования в lasheck)
        if not len(self.las.data) == 0:
            with open('tamed.las', 'w', encoding='utf-8') as f:
                self.las.write(f)
        else:
            self.error += ["Empty Ascii block"]
            return self.error, [], None
        
        # Допроверка lascheck
        self.lascheck = lascheck.read('tamed.las', encoding='utf-8')
        self.lascheck.check_conformity()
        non_conformities = self.lascheck.get_non_conformities() + self.error

        if not self.amount_mnem_check():
            non_conformities.append("Amount of mnemonics doesn't match with curves amount")
        if len(non_conformities) != 0:
            res_file = lasio.read(self.filepath, encoding='utf-8')
        else:
            res_file = lasio.read('tamed.las')
        return non_conformities, warns, res_file # возвращаем критические ошибки, исправленные ошибки и актуальный .las файл

if __name__ == "__main__":
    '''relative_path = os.path.join('temp_files')

    absolute_path = os.path.abspath(relative_path)


    # Iterate through the files in the directory
    for filename in os.listdir(absolute_path):
        print(filename)
    # Construct the full path of the file
        file_path = os.path.join(absolute_path, filename)
        checker = LASchecker(file_path)
        res = checker.check()
        print(res)'''
    relative_path = os.path.join('temp_files', '1_segmented.las')

    absolute_path = os.path.abspath(relative_path)
    checker = LASchecker(absolute_path)
    res = checker.check()
    print(res)
        