#!/usr/bin/env python
"""
chgcar-split: split a chgcar file to a chgden and a magden file
"""

import os
import numpy as np

class chgcar_split:

    def __init__(self, reportlevel):

        self.reportlevel = reportlevel
        self.header = []

    def run(self, args):

        root = os.path.splitext(args.infile)[0]
        fchgden = root+'-chgden.vasp'
        fmagden = root+'-magden.vasp'

        # open chgcar file
        try:
            fin = open(args.infile, 'r')
            print('Reading input file "{}"'.format(args.infile))
        except IOError:
            print('Failed to open the input file "{}"'.format(args.infile))
            raise

        # read header
        self.read_header(fin, keep=True, fout=None)

        # process chgden
        print('Writing chgden to "{}"'.format(fchgden))
        self.write_chgden(fin, fchgden)

        # write magden file
        if len(peek_line(fin)) > 0:
            print('Writing magden to "{}"'.format(fmagden))
            # one blank line
            self.readline(fin)
            self.write_chgden(fin, fmagden)
        else:
            print('No magden found in "{}"'.format(fin.name))

        # close chgcar file
        fin.close()

    def read_header(self, fin, keep=True, fout=None):
        # Title
        self.readline(fin, keep, fout)
        # unit cell
        self.read_unitcell(fin, keep, fout)
        # element list
        self.read_elementlist(fin, keep, fout)
        # atom list
        self.read_atomlist(fin, keep, fout)
        # one blank line
        self.readline(fin, keep, fout)

    def readline(self, fin, keep=False, fout=None):
        line = fin.readline().rstrip()
        if keep:
            self.header.append(line)

        if fout is not None:
            fout.write(line+'\n')
        return line
        
    def read_unitcell(self, fin, keep=True, fout=None):
        # lattice parameter
        self.readline(fin, keep, fout)
        # primitive axes
        for ivec in range(3):
            self.readline(fin, keep, fout)

    def read_elementlist(self, fin, keep=True, fout=None):
        elemlist = []
        # test if this is the line for number of atoms
        words = self.readline(fin, keep, fout).split()
        try:
            natom = int(words[0])
            vasp5 = False
        except:
            vasp5 = True

        # number of atoms for each element
        if vasp5:
            words = self.readline(fin, keep, fout).split()

        self.natomlist = []
        for sn in words:
            self.natomlist.append(int(sn))

    def read_atomlist(self, fin, keep=True, fout=None):
        # coord system
        self.readline(fin, keep, fout)
        
        atomlist = []
        for natom in self.natomlist:
            for iatom in range(natom):
                line = self.readline(fin, keep, fout)

    def write_chgden(self, fin, fname):

        # open chgden file
        try:
            fout = open(fname, 'w')
        except IOError:
            print('Failed to open the output file "{}"'.format(fname))
            raise

        # write header
        self.write_header(fout)

        # read volume data
        self.read_vol_data(fin, fout)

        # read aug charge data
        self.read_aug_chg(fin, fout)

        # close chgden file
        fout.close()

    def read_vol_data(self, fin, fout):
        # grid dimensions
        line = self.readline(fin, fout=fout).rstrip()
        print('first line: {}'.format(line))
        words = line.split()
        nx = int(words[0])
        ny = int(words[1])
        nz = int(words[2])

        #read data on grid points
        ndata = nx*ny*nz

        words = []
        for iz in range(nz):
            for iy in range(ny):
                for ix in range(nx):
                    if len(words) < 1:
                        words = self.readline(fin, fout=fout).split()
                    words.pop(0)
        
    def read_aug_chg(self, fin, fout=None):
        if fin is None:
            return
        # for each atom type
        for natom in self.natomlist:
            for iatom in range(natom):
                line = peek_line(fin).strip()
                if len(line) < 1:
                    return
                words = line.split()
                if words[0] != 'augmentation':
                    return
                words = self.readline(fin, fout=fout).strip().split()
                npoint = int(words[3])
                #read data on grid points
                words = []
                for ip in range(npoint):
                    if len(words) < 1:
                        words = self.readline(fin, fout=fout).split()
                    words.pop(0)

    def read_atom_magmom(self, fin, fout):
        words = []
        for natom in self.natomlist:
            for iatom in range(natom):
                if len(words) < 1:
                    words = self.readline(fin, fout=fout).split()
                words.pop(0)

    def write_header(self, outfile):
        for line in self.header:
            outfile.write(line+'\n')

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

def peek_next_word(f):
    line = peek_line(f)
    if len(line) < 1:
        return None
    return line.split()[0]

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='chgcar-split: split a chgcar file to a chgden and a magden file')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input file')

    args = parser.parse_args()

    app = chgcar_split(reportlevel=args.reportlevel)
    app.run(args)
