import Levenshtein as l
from random import randint
from pprint import pprint
import unittest

class CodeGenerator():
    def __init__(self, code_len, min_dist, max_codes_cnt):
        if min_dist<3:
            raise Exception('Minimum distance should be greater than 2')
        if min_dist>=code_len:
            raise Exception('Minimum Levenshtein distance cannot be equal or higher than code length')

        self.codes = []
        self.code_len = code_len
        self.min_dist = min_dist
        self.max_codes_cnt = max_codes_cnt
        self.chars_digits = "1234567890"
        self.chars_uppercase_letters = "ABCDEFGHIJKLMNOPQRTUVWXYZ"

        for i in range(0,self.max_codes_cnt):
            code = self.gen_code()
            self.codes.append(code)

    def check_dist(self, new_code, min_dist):
        matches = []
        for code in self.codes:
            l_dist = l.distance(new_code, code)
            if l_dist < min_dist:
                matches.append({'code': code,'new_code': new_code, 'l_dist': l_dist})
        return matches
    
    def gen_code(self):
        for i in range(0,1001):
            # new_code = str(self.random_with_N_digits(self.code_len))
            new_code = self.random_with_N_chars(self.code_len, self.chars_uppercase_letters)
            if len(self.check_dist(new_code, self.min_dist)) > 0:
                continue
            else:
                return new_code
        raise Exception('could not generate code in 1000 trials, try generating longer codes or lower minimum distance')

    def check_code(self, input_code, sensitivity):
        if input_code in self.codes:
            return [input_code]
        matches = self.check_dist(input_code, self.min_dist-sensitivity)
        return [match['code'] for match in matches]
        
    @staticmethod
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    @staticmethod
    def random_with_N_chars(n, char_table):
        result = ''
        for i in  range(0,n):
            i = randint(0, len(char_table)-1)
            result = result + char_table[i]
        return result


#--------TESTS---------
def make_mistakes(code, n):
    for i in range(0,n):
        pos = randint(0, len(code)-1)
        new_char = chr(ord(code[pos])+1)
        code = code[:pos] + new_char + code[pos+1:]
    return code


class TestUnitTest(unittest.TestCase):
    def test_no_typo(self):
        cg = CodeGenerator(6,3,600)
        for code in cg.codes:
            check_result = cg.check_code(code, 1)
            self.assertEqual([code],check_result)

    def test_one_char_typo(self):
        cg = CodeGenerator(6,3,600)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 1)
            check_result = cg.check_code(code_with_error, 1)
            self.assertEqual([code],check_result)

    def test_two_char_typo(self):
        cg = CodeGenerator(10,5,1000)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 2)
            check_result = cg.check_code(code_with_error, 2)
            self.assertEqual([code],check_result)
                
    def test_three_char_typo(self):
        cg = CodeGenerator(14,7,6000)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 3)
            check_result = cg.check_code(code_with_error, 3)
            self.assertEqual([code],check_result)

if __name__ == "__main__":
    cg = CodeGenerator(8,5,60)
    print(cg.codes)