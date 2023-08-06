#!/usr/bin/env python
"""
chgcar-combine: Combine two chgcar files
"""

import os
import numpy as np
from pymatgen.io.vasp.outputs import Chgcar

class chgcar_combine:

    def __init__(self):

        pass

    def run(self, args):

        # banner
        print('====================')
        print('   CHGCAR COMBINE   ')
        print('====================')

        # read input file A
        print('\nReading CHGCAR a: "{}"'.format(args.chgcar1))
        self.chgcar1 = Chgcar.from_file(args.chgcar1)
        print(self.chgcar1.structure)
        print('Volumetric data: ', self.chgcar1.dim)

        # read input file B
        print('\nReading CHGCAR b: "{}"'.format(args.chgcar2))
        self.chgcar2 = Chgcar.from_file(args.chgcar2)
        print(self.chgcar2.structure)
        print('Volumetric data: ', self.chgcar2.dim)

        # combine input chagcar files
        self.chgcar3 = combine(self.chgcar1, self.chgcar2, expr=args.expr)

        # write output file
        print('Writing output file "{}"'.format(args.chgcar3))
        self.chgcar3.write_file(args.chgcar3)

def combine(chgcar1, chgcar2, expr='a+b'):

    print('combination expression: ', expr)
    def comb_func(a,b):
        return eval(expr)

    # Assure two chgcar files have the same structure
    if chgcar1.structure != chgcar2.structure:
        raise ValueError("Combination operations can only be "
                         "performed for volumetric data with the exact "
                         "same structure.")

    # Combine two chgcar files
    data = {}
    for k in chgcar1.data.keys():
        data[k] = comb_func(chgcar1.data[k], chgcar2.data[k])
    return Chgcar(chgcar1.poscar, data, data_aug=chgcar1.data_aug)

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='chgcar-combine: Combine CHGCAR files')
    parser.add_argument('chgcar1', help='input CHGCAR1')
    parser.add_argument('chgcar2', help='input CHGCAR2')
    parser.add_argument('chgcar3', help='output CHGCAR3')
    parser.add_argument('expr',
                        help='Expression to combine CHGCAR files. Must be enclosed in quotation marks. Ex) "a-b", "(a+b)/2"')

    args = parser.parse_args()

    app = chgcar_combine()
    app.run(args)
