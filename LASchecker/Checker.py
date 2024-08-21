import lasio
import lascheck
import statistics

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


    def check(self):
        self.step()
        self.lascheck.check_conformity()
        non_conformities = self.lascheck.get_non_conformities()
        if not self.amount_mnem_check():
            non_conformities.append("Amount of mnemonics doesn't match with curves amount")
        if not self.check_spaces()[0]:
            non_conformities.append("Additional whitespaces in {}".format(self.check_spaces()[1]))
        return non_conformities


checker = LASchecker("1.las")
print(checker.check())

'''print(check_spaces(las2))

calculate_step(las2)
las2.write("12.las")
print(las.check_conformity())
print(las.get_non_conformities())
print(amount_mnem_check(las2))'''