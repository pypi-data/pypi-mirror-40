#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from msudft.core import cmptlib

class Unitcell:
    """
    module for a unit cell of a crystal structure
    """
    def __init__(self):
        self.type = "general"
        self.lattParam = 1.0
        self.pbc = [True, True, True]
        self.avec = np.eye(3)
        self.f2c = np.eye(3)
        self.c2f = np.eye(3)

    def copy(self):
        cp = Unitcell()
        cp.type = self.type
        cp.lattParam = self.lattParam
        cp.pbc = self.pbc
        cp.avec = self.avec.copy()
        cp.f2c = self.f2c.copy()
        cp.c2f = self.c2f.copy()
        return cp

    def finalize(self):
        from numpy.linalg import inv
        # transformation matrix -- fractional to cartesian coordinates
        self.f2c = np.transpose(self.avec)
        # transformation matrix -- cartesian to fractional coordinates
        self.c2f = inv(self.f2c)

    def report(self):
        print("Unitcell:")
        print("  type={}".format(self.type))
        print("  lattice parameter=", self.lattParam)
        print("  pbc=", self.pbc)
        print("  Lattice vector, lengths, angles")
        vlen, vang = cmptlib.latt_leng_angle(self.avec)
        fmt = '{:>3}: [{:>12.8f}, {:>12.8f}, {:>12.8f}] ' + \
              '{:>12.8f} {:>8.4f}'
        print('---------------------------------------------------------------------')
        print('indx    avec[x]        avec[y]       avec[z]      length      angle  ')
        print('---- -------------- ------------- ------------- ------------ --------')
        for idir in range(3):
            print(fmt.format(
                idir+1, self.avec[idir][0],
                self.avec[idir][1], self.avec[idir][2],
                vlen[idir], cmptlib.degree(vang[idir])))
        print('---------------------------------------------------------------------')
        print('  Cell volume = {}'.format(cmptlib.cell_volume(self.avec)))
        print("  Fractional to cartesian transformation matrix:")
        print(self.f2c)
        print("  Cartesian to fractional transformation matrix:")
        print(self.c2f)

if __name__ == "__main__":
    # stand-alone mode
    uc = Unitcell()
    uc.avec = np.array([[1, 2, -1], [3, 0, 1], [2, -2, 1]], dtype = np.float_)
    uc.finalize()
    uc.report()
