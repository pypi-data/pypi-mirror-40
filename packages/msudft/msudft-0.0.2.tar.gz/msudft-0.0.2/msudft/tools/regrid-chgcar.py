#!/usr/bin/env python
"""
regrid-chgcar: Re-grid a chgcar file
"""

from __future__ import print_function
import numpy as np

class chgcar:
    def __init__(self):
        self.header = []
        self.nx = 0
        self.ny = 0
        self.nz = 0

    def read(self, fname):
        """
        Read a chgcar file
        """
        try:
            self.infile = open(fname, 'r')
            print('%chgcar.read: Reading input file "{}"'
                  .format(fname))
        except IOError:
            print('%chgcar.read: Failed to open the input file "{}"'
                  .format(fname))
            raise

        # Title
        self._readline(True)

        # unit cell
        self._read_unitcell()

        # element list
        self._read_elementlist()

        # atom list
        self._read_atomlist()

        # one blank line
        self._readline(keep=True)

        # charge density
        self._read_chgden()

    def _readline(self, keep=True):
        line = self.infile.readline().strip()
        if keep:
            self.header.append(line)
        return line
        
    def _read_unitcell(self):
        # lattice parameter
        self._readline(keep=True)
        # primitive axes
        for ivec in range(3):
            self._readline(keep=True)

    def _read_elementlist(self):
        elemlist = []
        # test if this is the line for number of atoms
        line = self._readline(keep=True)
        words = line.split()
        try:
            natom = int(words[0])
            vasp5 = False
        except:
            vasp5 = True

        # number of atoms for each element
        if vasp5:
            line = self._readline(keep=True)
            words = line.split()

        self.natomlist = []
        for sn in words:
            self.natomlist.append(int(sn))

    def _read_atomlist(self):
        # coord system
        self._readline(keep=True)
        
        atomlist = []
        for natom in self.natomlist:
            for iatom in range(natom):
                line = self._readline(keep=True)

    def _read_chgden(self):
        # grid dimensions
        line = self._readline(keep=False)
        words = line.split()
        self.nx = words[0]
        self.ny = words[1]
        self.nz = words[2]

        #read data on grid points
        self.ndata = self.nx*self.ny*self.nz
        self.data = np.zeros( (self.nx, self.ny, self.nz) )

        words = []
        for iz in xrange(self.nz):
            for iy in xrange(self.ny):
                for ix in xrange(self.nx):
                    if len(words) < 1:
                        line = self._readline(keep=False)
                        words = line.split()
                    self.data[ix,iy,iz] = words.pop(0)
        
def write(mol, f, coord=None, options="", verbose=0):
  print("options=", options)
  newinfo = strutil.getvalue(options, "newinfo")
  f.write("{} {}\n".format(mol.name, mol.info))
  f.write("{}\n".format(mol.unitcell.lattParam))
  for aid in range(3):
    s = ""
    avec = mol.unitcell.axis[:,aid]/mol.unitcell.lattParam
    for ixyz in range(3):
      s += "  {:12.6f}".format(avec[ixyz])
    f.write("{}\n".format(s))

  # elementlist
  elemlist = []
  for atom in mol.atomlist:
    if atom.symbol in elemlist:
      pass
    else:
      elemlist.append(atom.symbol)
  s = ''
  for elem in elemlist:
    s += " " + elem
  f.write("{}\n".format(s))

  # sort atoms
  atmlist2 = []
  for elem in elemlist:
    na = 0
    for atom in mol.atomlist:
      if atom.symbol == elem:
        na += 1
        atmlist2.append(atom)
    f.write(" {:8}".format(na))
  f.write('\n')

  # atomlist
  if coord == None:
    coord = mol.atomcoord
  if coord == "frac":
    s = "Direct"
  else:
    s = "Cartesian"
  f.write("{}\n".format(s))
  for iatm,atom in enumerate(atmlist2):
    if coord == "frac":
      pos = atom.fpos
    else:
      pos = np.dot(mol.unitcell.f2c, atom.fpos)
    s = ""
    for aid in range(3):
      s += " {:12.6f}".format(pos[aid])
    if newinfo:
      info = "# {}{}".format(atom.symbol, iatm)
    else:
      info = atom.info
    s += " {}\n".format(info)
    f.write(s)
  f.write('\n')

        
class regrid_chgcar:

    def __init__(self, reportlevel):

        self.reportlevel = reportlevel

    def run(self, infile, outfile, ndim):

        chg = chgcar()
        chg.read(infile)
        self.regrid(chg, ndim)
        chg.write(outfile)

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='Interpolate a charge density file')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('nx', type=int, help='nx')
    parser.add_argument('ny', type=int, help='ny')
    parser.add_argument('nz', type=int, help='nz')

    args = parser.parse_args()

    app = regrid_chgcar(reportlevel=args.reportlevel)
    app.run(args.infile, args.outfile, (args.nx, args.ny, args.nz))
