import lasio
import lascheck
import statistics
import os

class LASchecker():
    def __init__(self, filepath: str):
        #super(LASchecker, self).__init__()
        self.lascheck = lascheck.read(filepath)
        self.las = lasio.read(filepath)

    def calculate_step(self):
        depth_values = self.las.curves[0].data
        differences = [depth_values[i+1] - depth_values[i] for i in range(len(depth_values) - 1)]
        return statistics.fmean(differences)
    
    def step(self):
        if self.las.well.step.value == '':
            self.las.well.step.value = self.calculate_step()
            self.las.write('filename')

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
    def check_for_potentially_deadly(self):
        fixed = []
        if not 'VERS' in self.las.version.keys(): pass
        if not 'WRAP' in self.las.version.keys(): return "WRAP not in ~V section"
        if not 'NULL' in self.las.well.keys(): return "NULL not in ~V section"


    def check(self):
        warns = []
        if not "Version" in self.lascheck.sections.keys():
            warns += ['Header section Version regexp=~V was not found.',\
                      'VERS item not found in the ~V section.',\
                        'WRAP item not found in the ~V section']
            self.las.write('tamed.las') 
            self.lascheck = lascheck.read('tamed.las')
        print(warns)
        print(self.las.version)
        print(self.lascheck.version)
        print(self.las.version.keys())
        first_problems = self.check_for_potentially_deadly()
        self.step()
        self.lascheck.check_conformity()
        non_conformities = self.lascheck.get_non_conformities()
        if not self.amount_mnem_check():
            non_conformities.append("Amount of mnemonics doesn't match with curves amount")
        if not self.check_spaces()[0]:
           non_conformities.append("Additional whitespaces in {}".format(self.check_spaces()[1]))
        return non_conformities


relative_path = os.path.join('.', 'Las_handler', 'Encoded', 'LAS_NGE.93394')

absolute_path = os.path.abspath(relative_path)
checker = LASchecker(absolute_path)
print(checker.check())