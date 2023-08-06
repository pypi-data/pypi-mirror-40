#!/usr/bin/env python

"""
print-nbrmap: Print neighbor map
"""

from __future__ import print_function
import numpy as np
import fileUtil

class Neighbor:
    """
    class for a neighboring atom.
    """
    def __init__(self, atom, cell, dist, cpos):
        self.atom = atom
        self.cell = cell
        self.dist = dist
        self.cpos = cpos

class print_nbrmap:

    def __init__(self, tolerance, reportlevel):

        self.tolerance = tolerance
        self.reportlevel = reportlevel

    def run(self, args):

        # banner
        print('==================')
        print('   PRINT NBRMAP   ')
        print('==================')

        # read input file
        mol = fileUtil.read(args.infile, fmt=args.infmt, reportlevel=self.reportlevel)

        # convert padding
        try:
            pad = eval(args.padding)
        except IOError:
            print('Invalid padding descriptor')
            raise

        # convert onlyatom list
        try:
            onlyatoms = eval(args.onlyatoms)
        except IOError:
            print('Invalid padding descriptor')
            raise

        # print a neighbor map
        self.print_nbrmap(mol, args.cutoff, pad, onlyatoms)

    def print_nbrmap(self, mol, cutoff, pad, onlyatoms):
        crange = [1, 1, 1]
        for idir in range(3):
            if mol.unitcell.pbc[idir]:
                crange[idir] = pad[idir]
            else:
                crange[idir] = 0

        print('===========================================================')
        print('   PRINT NBRMAP   ')
        print('===========================================================')

        for atom1 in mol.atomlist:

            #check if we need to do this atom
            if len(onlyatoms) < 1:
                pass
            elif not(atom1.id in onlyatoms):
                continue

            cpos1 = np.dot(mol.unitcell.f2c, atom1.fpos)
            nbrlist1 = []
            for atom2 in mol.atomlist:
                for c0 in range(-crange[0], crange[0]+1):
                    for c1 in range(-crange[1], crange[1]+1):
                        for c2 in range(-crange[2], crange[2]+1):
                            cell = np.array([c0, c1, c2])
                            fpos2 = atom2.fpos + cell
                            cpos2 = np.dot(mol.unitcell.f2c, fpos2)
                            dist = np.linalg.norm(cpos2 - cpos1)
                            if dist < self.tolerance:
                                pass
                            elif dist > cutoff:
                                pass
                            else:
                                nbr = Neighbor(atom2, cell, dist, cpos2)
                                nbrlist1.append(nbr)
            nbrlist1.sort(key=lambda nbr: nbr.dist)
            print(atom1.id, atom1.type, atom1.info, cpos1)
            for index, nbr in enumerate(nbrlist1):
                s = '    {:>3} {:>7.4f}'.format(index+1, nbr.dist)
                s += ' {:>4} {:>2}'.format(nbr.atom.id, nbr.atom.type)
                print(s, nbr.atom.info, nbr.cell, nbr.cpos)
        print('===========================================')


if __name__ == '__main__':
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='print-nbrmap: Print a neighbor map.  Ex) print-nbrmap.py GdN.msf 10.0 --padding="[3,2,2]" --onlyatoms="[1,18]" > GdN.nbrmap.out')
    parser.add_argument('infile', help='input file')
    parser.add_argument('cutoff', type=float, default=5.0,
                        help='cutoff radius')
    parser.add_argument('-i', '--infmt',  default=None,
                        help='format for input file')
    parser.add_argument('--padding', type=str, default='[1, 1, 1]',
                        help='No. of cells to duplicate in each direction. Given as a string of a valid python int list.  Ex) "[3,3,3]"')
    parser.add_argument('--onlyatoms', type=str, default='[]',
                        help='List of only atom indices to check neighbors. Given as a string of a valid python int list.  Ex) "[1,2,8,10]".  "[]"=ALL')
    parser.add_argument('--tolerance', type=float, default=1.0e-4,
                        help='tolerance to be considered as zero')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')

    args = parser.parse_args()

    app = print_nbrmap(args.tolerance, args.reportlevel)
    app.run(args)
