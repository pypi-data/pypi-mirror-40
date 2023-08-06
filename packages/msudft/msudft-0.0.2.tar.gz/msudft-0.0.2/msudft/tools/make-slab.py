#!/usr/bin/env python
"""
make-slab: Make a slab from given structure
"""

from __future__ import print_function
import pymatgen as mg
import math
import numpy as np
from msudft.core import util

class makeSlab:

    def __init__(self):

        pass

    def run(self, args):

        # banner
        print('===================')
        print('   MAKE SLAB   ')
        print('===================')

        # read input file
        mol = util.read_from_file(args.infile)

        # Slab generator
        from pymatgen.core.surface import SlabGenerator
        gen = SlabGenerator(initial_structure=mol.structure(),
                            miller_index=args.miller_index,
                            min_slab_size=args.min_slab_size,
                            min_vacuum_size=args.min_vac_size,
                            in_unit_planes=args.in_unit_planes
        )
        slab = gen.get_slab()
        print(slab)

        # write output file
        mol2 = Molecule.Molecule.from_pymatgen_structure(slab)
        mol2.name = "slab " + args.infile + " " + str(args.miller_index)
        fileUtil.write(mol2, args.outfile, coord=args.coord)

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='Make a slab from a given input structure')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile',
                        help='Input structure file')
    parser.add_argument('outfile',
                        help='Output structure file for the slab')
    parser.add_argument('miller_index', type=str,
                        help='Miller index of plane parallel to surface, Ex) "[0,0,1]"')
    parser.add_argument('min_slab_size', type=float,
                        help='Minimum size of layers containing atoms')
    parser.add_argument('min_vac_size', type=float,
                        help='Minimize size of vacuum')
    parser.add_argument('--in_unit_planes', action='store_true',
                        help='Flag to set min_slab_size and min_vac_size in units of hkl planes. If not set, Ang is used.')

    args = parser.parse_args()
    print(args)
    # convert miller index
    try:
        index = eval(args.miller_index)
        args.miller_index = index
    except IOError:
        print('Invalid Miller index')
        raise

    app = makeSlab()
    app.run(args)
