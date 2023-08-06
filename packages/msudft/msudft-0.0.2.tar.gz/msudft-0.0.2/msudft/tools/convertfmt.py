#!/usr/bin/env python

"""
convertfmt: Convert crystal structure file format
"""

from __future__ import print_function
import msudft

class convertfmt:

    def __init__(self):

        pass

    def run(self, args):

        # banner
        print('====================')
        print('   CONVERT FORMAT   ')
        print('====================')

        # read input file
        xstr = msudft.util.read_from_file(args.infile, fmt=args.infmt,
                                          reportlevel=self.reportlevel)

        # write output file
        msudft.util.write_to_file(xstr, args.outfile, fmt=args.outfmt,
                                  coord=args.coord,
                                  reportlevel=self.reportlevel)

if __name__ == '__main__':
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='convertfmt: Convert a molecular structure file format')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('-i', '--infmt',  default=None,
                        help='format for input file')
    parser.add_argument('-o', '--outfmt',  default=None,
                        help='format for output file')
    parser.add_argument('--coord', default=None, choices=['frac', 'cart'],
                        help='coord system for output file')

    args = parser.parse_args()

    app = convertfmt(args.reportlevel)
    app.run(args)
