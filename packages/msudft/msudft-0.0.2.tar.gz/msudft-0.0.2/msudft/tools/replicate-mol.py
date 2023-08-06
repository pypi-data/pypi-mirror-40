#!/usr/bin/env python

"""
replicate-mol: Replicate molecular structure
"""

import numpy as np
import fileUtil

class replicate_mol:

    def __init__(self, reportlevel):

        self.reportlevel = reportlevel

    def run(self, args):

        # banner
        print('===================')
        print('   REPLICATE MOL   ')
        print('===================')

        # read input file
        mol0 = fileUtil.read(args.infile, reportlevel=self.reportlevel)

        # replicate molecule
        mol1 = self.replicate(mol0, (args.n1, args.n2, args.n3))
        mol1.report()

        # write output file
        fileUtil.write(mol1, args.outfile, reportlevel=self.reportlevel)

    def replicate(self, mol0, nrep):

        print('nrep = {}'.format(nrep))
        # set molecule
        mol1 = mol0.copy()
        # unit cell
        mol1.unitcell.lattParam = 1.0
        for aid in range(3):
            mol1.unitcell.avec[aid] = mol0.unitcell.avec[aid]*nrep[aid]
        mol1.unitcell.finalize()

        # Generate atoms
        mol1.atomlist = []
        for c0 in range(nrep[0]):
            for c1 in range(nrep[1]):
                for c2 in range(nrep[2]):
                    dfpos = np.array([c0, c1, c2])
                    for atom0 in mol0.atomlist:
                        atom1 = atom0.copy()
                        atom1.id = len(mol1.atomlist)+1
                        fpos = atom0.fpos + dfpos
                        cpos = np.dot(mol0.unitcell.f2c, fpos)
                        fpos = np.dot(mol1.unitcell.c2f, cpos)
                        atom1.fpos = fpos
                        atom1.cpos = cpos
                        mol1.atomlist.append(atom1)

        return mol1

if __name__ == '__main__':
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='print-nbrmap: Print a neighbor map')
    parser.add_argument('infile', help='input file')
    parser.add_argument('n1', type=int, default=1,
                        help='no. of cells to replicate in a1')
    parser.add_argument('n2', type=int, default=1,
                        help='no. of cells to replicate in a2')
    parser.add_argument('n3', type=int, default=1,
                        help='no. of cells to replicate in a3')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')

    args = parser.parse_args()

    app = replicate_mol(args.reportlevel)
    app.run(args)
