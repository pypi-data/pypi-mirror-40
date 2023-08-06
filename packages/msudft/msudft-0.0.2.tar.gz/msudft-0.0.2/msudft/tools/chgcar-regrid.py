#!/usr/bin/env python
"""
chgcar-regrid: regrid a chgcar file
"""

from __future__ import print_function
import os
import numpy as np

class chgcar_regrid:

    def __init__(self, reportlevel):

        self.reportlevel = reportlevel
        self.header = []

    def run(self, fn_infile, fn_outfile, nx, ny, nz):

        # open input file
        try:
            self.infile = open(fn_infile, 'r')
            print('Reading input file "{}"'.format(fn_infile))
        except IOError:
            print('Failed to open the input file "{}"'.format(fn_infile))
            raise

        # read header
        self.read_header()
        
        # open output file
        try:
            self.outfile = open(fn_outfile, 'w')
            print('Opened file "{}" for writing chgden'.format(fn_outfile))
        except IOError:
            print('Failed to open the output file "{}"'.format(fn_outfile))
            raise

        # write header to chgden file
        self.write_header(self.outfile)

        # read data on a grid
        self.read_data_on_grid()

        # write data on a new grid
        self.write_data_on_grid(nx, ny, nz)

        # close files
        self.infile.close()
        self.outfile.close()

    def read_header(self):
        # Title
        self.readline(keep='h')
        # unit cell
        self.read_unitcell()
        # element list
        self.read_elementlist()
        # atom list
        self.read_atomlist()
        # one blank line
        self.readline(keep='h')

    def readline(self, keep=None, dest=None):
        line = self.infile.readline().rstrip()
        if keep == 'h':
            self.header.append(line)

        if dest == None:
            pass
        else:
            dest.write(line+'\n')
        return line
        
    def read_unitcell(self):
        # lattice parameter
        self.readline(keep='h')
        # primitive axes
        for ivec in range(3):
            self.readline(keep='h')

    def read_elementlist(self):
        elemlist = []
        # test if this is the line for number of atoms
        line = self.readline(keep='h')
        words = line.split()
        try:
            natom = int(words[0])
            vasp5 = False
        except:
            vasp5 = True

        # number of atoms for each element
        if vasp5:
            line = self.readline(keep='h')
            words = line.split()

        self.natomlist = []
        for sn in words:
            self.natomlist.append(int(sn))

    def read_atomlist(self):
        # coord system
        self.readline(keep='h')
        
        atomlist = []
        for natom in self.natomlist:
            for iatom in range(natom):
                line = self.readline(keep='h')

    def read_data_on_grid(self):
        # grid dimensions
        line = self.readline()
        words = line.split()
        self.nx = int(words[0])
        self.ny = int(words[1])
        self.nz = int(words[2])

        #read data on grid points
        self.ndata = self.nx*self.ny*self.nz

        self.data = np.zeros( (self.nx, self.ny, self.nz), dtype=np.float_ )
        words = []
        for iz in xrange(self.nz):
            for iy in xrange(self.ny):
                for ix in xrange(self.nx):
                    if len(words) < 1:
                        line = self.readline()
                        words = line.split()
                    self.data[ix,iy,iz] = np.float_(words.pop(0))
        
    def write_data_on_grid(self, nx, ny, nz):
        from scipy.interpolate import RegularGridInterpolator
        xlist0 = np.linspace(0.0, 1.0, self.nx)
        ylist0 = np.linspace(0.0, 1.0, self.ny)
        zlist0 = np.linspace(0.0, 1.0, self.nz)
        my_func = RegularGridInterpolator((xlist0, ylist0, zlist0), self.data)

        xfactor=1.0/np.float_(nx-1)
        yfactor=1.0/np.float_(ny-1)
        zfactor=1.0/np.float_(nz-1)

        self.outfile.write(' {} {} {}\n'.format(nx, ny, nz))
        max_count_per_line = 5
        line = ''
        count = 0
        for iz in xrange(nz):
            z = iz*zfactor
            for iy in xrange(ny):
                y = iy*yfactor
                for ix in xrange(nx):
                    x = ix*xfactor
                    pos = np.array([x,y,z])
                    value = my_func(pos)
                    word = '{:17.10E}'.format(value[0])
                    line = line + ' ' + word
                    count = count + 1
                    if count >= max_count_per_line:
                        self.outfile.write(line+'\n')
                        line = ''
                        count = 0

        if len(line) > 0:
            self.outfile.write(line+'\n')
            line = ''
            count = 0
                        
    def write_header(self, outfile):
        for line in self.header:
            outfile.write(line+'\n')

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='chgcar-regrid: regrid a chgcar file')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input chgcar file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('nx', type=int, help='nx')
    parser.add_argument('ny', type=int, help='ny')
    parser.add_argument('nz', type=int, help='nz')

    args = parser.parse_args()

    app = chgcar_regrid(reportlevel=args.reportlevel)
    app.run(args.infile, args.outfile, args.nx, args.ny, args.nz)
