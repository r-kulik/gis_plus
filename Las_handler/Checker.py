import lasio.exceptions
import lasio
import sys
import statistics
import os
import math


try:
    from Las_handler import lascheck
except ModuleNotFoundError:
    import lascheck

class LASchecker():
    def __init__(self, filepath: str):
        #super(LASchecker, self).__init__()
        try:
            self.filepath = filepath
            self.lascheck = lascheck.read(filepath, encoding='utf-8')
            self.las = lasio.read(filepath, encoding='utf-8')
            self.error = 0
        except (lasio.exceptions.LASHeaderError, lasio.exceptions.LASDataError, lasio.exceptions.LASUnknownUnitError):
            exception_type, exception_value, exception_traceback = sys.exc_info()
            self.error = [], [exception_value]
        except Exception:
            self.error = [], [sys.exc_info()[0], ':', sys.exc_info()[1]]

    def calculate_step(self):
        depth_values = self.las.curves[0].data
        differences = [depth_values[i+1] - depth_values[i] for i in range(len(depth_values) - 1)]
        return statistics.fmean(differences)
    
    def step(self):
        if self.las.well.step.value == '':
            self.las.well.step.value = self.calculate_step()
            return ["Was not appropriate step. Calculated, choose step {}".format(self.las.well.step.value)]
        return []

    def amount_mnem_check(self):
        equal = (len(self.las.curves) == self.las.data.shape[1])
        for i in self.las.curves:
            if i.mnemonic == "UNKNOWN":
                equal = False
        return equal

    def check_spaces(self):
        for i in self.las.well:
            for j in ['mnemonic', 'unit']:
                if ' ' in str(i[j]): return [False, '~W section']
        for i in self.las.params:
            for j in ['mnemonic', 'unit']:
                if ' ' in str(i[j]): return [False, '~P section']
        for i in self.las.curves:
            for j in ['mnemonic', 'unit']:
                if ' ' in str(i[j]): return [False, '~C section']
        for i in self.las.version:
            for j in ['mnemonic', 'unit']:
                if ' ' in str(i[j]): return [False, '~V section']
        return [True]


    def check(self):
        if self.error != 0:
            return self.error
        warns = []
        errors = []
        if not "Version" in self.lascheck.sections.keys():
            warns += ['Err: Header section Version regexp=~V was not found. Created ~V section.',\
                      'VERS item not found in the ~V section.',\
                        'WRAP item not found in the ~V section']
        if not 'VERS' in self.las.version.keys():
            self.las.version.append(lasio.HeaderItem('VERS', value=2.0, descr=': VERSION 2.0'))
            warns += ['VERS item not found in the ~V section']
        if not 'WRAP' in self.las.version.keys():
            self.las.version.append(lasio.HeaderItem('WRAP', value='NO', descr='Data Wrapping'))
            warns += ['WRAP item not found in the ~V section']
        if 'Well' in self.lascheck.sections.keys():
            if not 'NULL' in self.las.well.keys():
                self.las.well.append(lasio.HeaderItem('NULL', value='-9999.25', descr='Null value'))
                warns += ['NULL item not found in the ~W section']
            if not math.isclose(self.las.well['NULL'].value, -9999) and not \
                math.isclose(self.las.well['NULL'].value, -999.25) and not \
                math.isclose(self.las.well['NULL'].value, -9999.25):
                self.las.well['NULL'].value = '-9999.25'
                warns += ["Wrong NULL value. Should be -9999, -999.25 or -9999.25. Replaced to -9999.25"]
            warns+= self.step()
        for i in lascheck.spec.MandatorySections().get_missing_mandatory_sections(self.lascheck):
            errors += ["Missing mandatory sections: {}".format(i)]
        with open('tamed.las', 'w', encoding='utf-8') as f:
            self.las.write(f)
        self.lascheck = lascheck.read('tamed.las', encoding='utf-8')
        self.lascheck.check_conformity()
        non_conformities = self.lascheck.get_non_conformities() + errors
        if not self.amount_mnem_check():
            non_conformities.append("Amount of mnemonics doesn't match with curves amount")
        if not self.check_spaces()[0]:
           non_conformities.append("Additional whitespaces in {}".format(self.check_spaces()[1]))
        if len(non_conformities) != 0:
            res_file = lasio.read(self.filepath, encoding='utf-8')
        else:
            res_file = lasio.read('tamed.las')
        return non_conformities, warns, res_file

if __name__ == "__main__":
    relative_path = os.path.join('temp_files')

    absolute_path = os.path.abspath(relative_path)

    # Iterate through the files in the directory
    for filename in os.listdir(absolute_path):
        print(filename)
    # Construct the full path of the file
        file_path = os.path.join(absolute_path, filename)
        checker = LASchecker(file_path)
        res = checker.check()
        print(res)
        