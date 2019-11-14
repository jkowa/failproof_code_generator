# Failproof code generator
# Copyright (C) 2019 Jacek Kowalski

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import Levenshtein as l
from random import randint
from pprint import pprint
import unittest
import string
import argparse
from math import floor
class CodeGenerator():
    def __init__(self, code_len, min_dist, max_codes_cnt, charset = string.digits):
        """ Generates and validates fail-proof codes. Each pair of generated codes has the Levenshtein distance 
        equal or greater than min_dist parameter. Codes are resilient to floor(min_dist/2) typos.
        Recommended settings: 
        CodeGenerator(6,3,600) will generate codes resilient to 1 typo
        CodeGenerator(10,5,1000) will generate codes resilient to 2 typos
        CodeGenerator(14,7,4000)  will generate codes resilient to 3 typos
        Parameters:
        code_len (int): Length of the code to generate
        min_dist (int):
        max_codes_cnt (int): number of codes to generate
        charset (str): charset used to generate codes, i.e. string.digits or string.ascii_uppercase

        Returns:
        CodeGenerator:Returning value
        """
        if min_dist<3:
            raise Exception('Minimum distance should be greater than 2')
        if min_dist>=code_len:
            raise Exception('Minimum Levenshtein distance cannot be equal or higher than code length')

        self.codes = []
        self.code_len = code_len
        self.min_dist = min_dist
        self.max_codes_cnt = max_codes_cnt
        self.sensitivity = floor(float(self.min_dist)/2)

        for i in range(0,self.max_codes_cnt):
            code = self.gen_code(charset)
            self.codes.append(code)

    def check_dist(self, new_code, min_dist, codes):
        matches = []
        for code in codes:
            l_dist = l.distance(new_code, code)
            if l_dist < min_dist:
                matches.append({'code': code,'new_code': new_code, 'l_dist': l_dist})
        return matches
    
    def gen_code(self, charset):
        for i in range(0,1001):
            new_code = self.random_with_N_chars(self.code_len, charset)
            if len(self.check_dist(new_code, self.min_dist, self.codes)) > 0:
                continue
            else:
                return new_code
        raise Exception('could not generate code in 1000 trials, try generating longer codes or lower minimum distance')

    def check_code(self, input_code, sensitivity):
        if input_code in self.codes:
            return [input_code]
        matches = self.check_dist(input_code, self.min_dist-sensitivity, self.codes)
        return [match['code'] for match in matches]
        
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
            check_result = cg.check_code(code, cg.sensitivity)
            self.assertEqual([code],check_result)

    def test_one_char_typo(self):
        cg = CodeGenerator(6,3,600)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 1)
            check_result = cg.check_code(code_with_error, cg.sensitivity)
            self.assertEqual([code],check_result)

    def test_wrong_code(self):
        cg = CodeGenerator(6,3,600)
        wrong_code = "(*&(*&(^*())))"
        check_result = cg.check_code(wrong_code, cg.sensitivity)
        self.assertEqual([],check_result)

    def test_two_char_typo(self):
        cg = CodeGenerator(10,5,1000)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 2)
            check_result = cg.check_code(code_with_error, cg.sensitivity)
            self.assertEqual([code],check_result)
                
    def test_three_char_typo(self):
        cg = CodeGenerator(14,7,4000)
        for code in cg.codes:
            code_with_error = make_mistakes(code, 3)
            check_result = cg.check_code(code_with_error, cg.sensitivity)
            self.assertEqual([code],check_result)

if __name__ == "__main__":
    cg = CodeGenerator(8,5,60)
    print(cg.codes)