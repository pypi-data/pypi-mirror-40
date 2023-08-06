#!/usr/bin/env python

from __future__ import print_function

import io
import numpy as np
import pymatgen as mg
from msudft.core import Atom

class Xstructure:
    """
    module for a crystal structure.
    """
    def __init__(self):
        """
        Create a crystal structure
        """
        self.name = ''
        self.info = ''
        self.unitcell = mg.Lattice.cubic(1.0)
        self.atomcoord = 'frac'
        self.atomlist = []

    def copy(self):
        cp = Xstructure()
        cp.name = self.name
        cp.info = self.info
        cp.unitcell = self.unitcell.copy()
        cp.atomcoord =  self.atomcoord
        cp.atomtypes = list(self.atomtypes)
        cp.atomlist = []
        for atom0 in self.atomlist:
            atom = atom0.copy()
            cp.atomlist.append(atom)
        return cp

    def augment(self, xstr):
        """
        Augment the given sructure to this structure
        """
        aug = self.copy()
        for atom in xstr.atomlist:
            atom1 = atom.copy()
            atom1.fpos = self.unitcell.get_fractional_coords(atom1.cpos)
            aug.atomlist.append(atom1)
        return aug

    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of crystal structure
        """
        return self.get_string()

    def get_string(self):
        buf = io.StringIO()
        print("Name:", self.name, file=buf)
        print("Info:", self.info, file=buf)
        print(self.unitcell.__repr__(), file=buf)
        print("Atomcoord:", self.atomcoord, file=buf)
        print("Atoms:", len(self.atomlist), file=buf)
        print('-------------------------------------------------------------', file=buf)
        print('indx TYPE    avec[1]        avec[2]       avec[3]      info  ', file=buf)
        print('---- ---- -------------- ------------- ------------- --------', file=buf)
        for ia, atom in enumerate(self.atomlist):
            print('{:>4}'.format(ia+1), end=' ', file=buf)
            print(' {:>3}'.format(atom.type), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[0]), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[1]), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[2]), end=' ', file=buf)
            print(' | {}'.format(atom.info), file=buf)
        print('-------------------------------------------------------------', file=buf)
        return buf.getvalue()

    def finalize(self):
        # set of different atom types
        self.atomtypes = []
        for atom in self.atomlist:
            if not (atom.type in self.atomtypes):
                self.atomtypes.append(atom.type)
        # finalize atomlist
        if self.atomcoord == 'frac':
            for atom in self.atomlist:
                atom.cpos = self.unitcell.get_cartesian_coords(atom.fpos)
        else:
            for atom in self.atomlist:
                atom.fpos = self.unitcell.get_fractional_coords(atom.cpos)

    def get_spglib_cell(self):
        """
        Return a cell format used by spglib
        """
        latt = [self.unitcell.avec[i] for i in range(3)]
        poslist = [atom.fpos for atom in self.atomlist]
        numbers = [self.atomtypes.index(atom.type) for atom in self.atomlist]
        return (latt, poslist, numbers)

    def from_spglib_cell(self, cell):
        """
        Construct a XStructure from a cell format used by spglib
        """
        (latt, poslist, numbers) = (cell[0], cell[1], cell[2])
        xstr = XStructure()
        xstr.unitcell = self.unitcell.copy()
        xstr.unitcell.avec = latt
        xstr.atomcoord = 'frac'
        xstr.atomlist = []
        for (pos, num) in zip(poslist, numbers):
            atom = Atom()
            atom.type = self.atomtypes[num]
            atom.fpos = pos
            xstr.atomlist.append(atom)
        xstr.finalize()
        return xstr

if __name__ == "__main__":
    # stand-alone mode
    uc = mg.Lattice([[1, 2, -1], [3, 0, 1], [2, -2, 1]])
    print(uc)
    fpos = np.array([1.0, 1.0, 0.5])
    print('fpos1=', fpos)
    cpos = uc.get_cartesian_coords(fpos)
    print('cpos=', cpos)
    fpos1 = uc.get_fractional_coords(cpos)
    print('fpos1=', fpos1)
    
    xstr = Xstructure()
    xstr.unitcell = uc.copy()
    xstr.atomlist = []
    atom = Atom()
    atom.fpos = np.array([1, 0, 0])
    xstr.atomlist.append(atom)
    atom = Atom()
    atom.fpos = np.array([1, 0.5, 0])
    xstr.atomlist.append(atom)
    atom = Atom()
    atom.fpos = np.array([0.2, -0.25, -0.75])
    xstr.atomlist.append(atom)
    xstr.finalize()
    print('Test crystal structure')
    print(xstr)
