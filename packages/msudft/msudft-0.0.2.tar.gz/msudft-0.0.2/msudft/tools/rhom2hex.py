#!/usr/bin/env python

"""
HRconcert: Convert a molecule from rhombohedral to hexagonal unit cell 
            or vice versa 
"""

from __future__ import print_function
import os
import numpy as np
import fileUtil
import cmptlib

def R2H(mol0):
    """
    Convert a molecule from rhombohedral to hexagonal unit cell 
    """

    mol1 = mol0.copy()
    # new lattice vectors
    mol1.unitcell.type = "hexagonal"
    mol1.unitcell.avec[0] = mol0.unitcell.avec[0] - mol0.unitcell.avec[1]
    mol1.unitcell.avec[1] = mol0.unitcell.avec[1] - mol0.unitcell.avec[2]
    mol1.unitcell.avec[2] = mol0.unitcell.avec[0] + mol0.unitcell.avec[1] + mol0.unitcell.avec[2] 
    mol1.unitcell.finalize()
    print('New hexagonal unit cell:')
    mol1.unitcell.report()

    # position generators
    dfposlist = []
    dfpos = [0, 0, 0]
    dfposlist.append(dfpos)
    dfpos = [0, 1, 0]
    dfposlist.append(dfpos)
    dfpos = [1, 1, 0]
    dfposlist.append(dfpos)

    # generate atom positions
    mol1.unitcell.atomcoord = "frac"
    mol1.atomlist = []
    for dfpos in dfposlist:
        for atom0 in mol0.atomlist:
            atom1 = atom0.copy()
            fpos = atom0.fpos + dfpos
            cpos = np.dot(mol0.unitcell.f2c, fpos)
            fpos = np.dot(mol1.unitcell.c2f, cpos)
            fpos = cmptlib.normalize_frac(fpos)
            atom1.fpos = fpos
            atom1.cpos = cpos
            mol1.atomlist.append(atom1)

    """
    from scipy.interpolate import RegularGridInterpolator
    xlist0 = np.linspace(0.0, 1.0, mol0.volumedata.npnt[0])
    ylist0 = np.linspace(0.0, 1.0, mol0.volumedata.npnt[1])
    zlist0 = np.linspace(0.0, 1.0, mol0.volumedata.npnt[2])
    my_func = RegularGridInterpolator((xlist0, ylist0, zlist0), mol0.volumedata.data)

    nx = mol0.volumedata.npnt[0]
    ny = mol0.volumedata.npnt[1]
    nz = mol0.volumedata.npnt[2]
    
    xfactor=1.0/np.float_(nx-1)
    yfactor=1.0/np.float_(ny-1)
    zfactor=1.0/np.float_(nz-1)

    mol.volumedata = Molecule.VolumeData(nx,ny,nz)
    for iz in xrange(nz):
        z = iz*zfactor
        for iy in xrange(ny):
            y = iy*yfactor
            for ix in xrange(nx):
                x = ix*xfactor
                fpos = np.array([x,y,z])
                cpos = np.dot(mol.unitcell.f2c, fpos)
                fpos0 = np.dot(mol0.unitcell.c2f, cpos)
                fpos0 = normalize_fraction(fpos0)
                mol1.volumedata.data[ix,iy,iz] = my_func(fpos0)
    """
    
    mol1.report()
    return mol1

class rhom2hex:

    def __init__(self, reportlevel):

        self.reportlevel = reportlevel
        self.header = []

    def run(self, infile, outfile):

        # banner
        print('====================')
        print('      RHOM2HEX      ')
        print('====================')

        # read input file
        mol0 = fileUtil.read(infile, self.reportlevel)
        mol0.report()

        # convert to hexagonal lattice
        mol1 = R2H(mol0)

        # write output file
        fileUtil.write(mol1, outfile, reportlevel=self.reportlevel)

if __name__ == '__main__':
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='rhom2hex: '+
        'Convert a molecule from rhombohedral to hexagonal coord system')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')

    args = parser.parse_args()

    app = rhom2hex(reportlevel=args.reportlevel)
    app.run(args.infile, args.outfile)
