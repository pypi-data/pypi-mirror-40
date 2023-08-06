#!/usr/bin/env python
"""
Module for vasp file I/O
"""

from __future__ import print_function
import sys
import os
import numpy as np
from ..core import Xstructure

def read(f, reportlevel=0):
    molecule = Molecule.Molecule()

    # unit cell
    molecule.unitlength = "angstrom"
    molecule.unitcell = Molecule.Unitcell()
    molecule.unitcell.pbc = [False, False, False]
    molecule.unitcell.finalize()
    
    # no of atoms
    try:
        words = f.readline().strip().split()
        natom = int(words[0])
    except Exception:
        raise RuntimeError('Invalid or missing no of atoms')

    # header
    molecule.name = f.readline().strip()

    molecule.atomcoord = "cart"
    molecule.atomlist = _read_atomlist(f, natom)
    molecule.finalize()

    return molecule

def _read_atomlist(f, natom):
    atomlist = []
    for iatom in range(natom):
        line = f.readline().strip()
        words = line.split()
        atom = Molecule.Atom()
        atom.id = len(atomlist) + 1
        atom.type = words[0]
        s1 = words[1]
        s2 = words[2]
        s3 = words[3]
        atom.cpos = np.array([float(s1),float(s2),float(s3)])
        if len(words) > 4:
            atom.info = ' '.join(words[4:])
        else:
            atom.info = ''
        atomlist.append(atom)
    return atomlist

def write(mol, f, reportlevel=0):
    # no of atoms
    f.write(' {}'.format(len(mol.atomlist)))
    # Molecule name
    f.write('{}\n'.format(mol.name))
    # atomlist
    for atom in mol.atomlist:
        f.write(' {}'.format(str(atom.cpos)[1:-1]))
        f.write(' {}\n'.format(atom.info))

if __name__ == "__main__":
    # stand-alone mode
    if len(sys.argv) < 3:
        print('Usage: vasp.py infile outfile')
    else:
        infile = sys.argv[1]
        f = open(infile, 'r')
        print('Reading input XYZ file "{}"'.format(infile))
        mol = read(f, reportlevel=5)
        f.close()
        outfile = sys.argv[2]
        print('Writing output XYZ file "{}"'.format(outfile))
        f = open(outfile, "w")
        write(mol, f, reportlevel=5)
        f.close()
