#!/usr/bin/env python
"""
Module for vasp file I/O
"""

from __future__ import print_function
import sys
import os
import numpy as np
import pymatgen as mg
from msudft import Xstructure

def read(infile, reportlevel=0):
    poscar = mg.Poscar.from_file(infile)
    structure = poscar.structure
    name = poscar.comment
    if len(name) < 1:
        name = None
    info = None
    selective_dynamics = poscar.selective_dynamics
    velocities = poscar.velocities
    siteinfo = None
    return Xstructure(structure, name=name, info=info,
                      selective_dynamics=selective_dynamics,
                      velocities=velocities, 
                      siteinfo=siteinfo)

def write(xstr, f, coord=None, reportlevel=0):
    # X-structure name
    f.write('{}\n'.format(xstr.name))
    # unit cell
    f.write("%s\n" % xstr.unitcell.lattParam)
    for aid in range(3):
        avec = xstr.unitcell.avec[aid]/xstr.unitcell.lattParam
        f.write("%s\n" % str(avec)[1:-1])

    # set of different atom types
    typelist = []
    for atom in xstr.atomlist:
        if not (atom.type in typelist):
            typelist.append(atom.type)

    # sort atoms
    alist = []
    nalist = []
    for type in typelist:
        na = 0
        for atom in xstr.atomlist:
            if atom.type == type:
                na += 1
                alist.append(atom)
        nalist.append(na)

    # type list
    s = ' '.join([str(t) for t in typelist])
    f.write(' {}\n'.format(s))
    s = ' '.join([str(na) for na in nalist])
    f.write(' {}\n'.format(s))
    
    # atomlist
    if coord == None:
        coord = xstr.atomcoord
    if coord == "frac":
        s = "Direct"
    else:
        s = "Cartesian"
    f.write('{}\n'.format(s))
    for atom in alist:
        if coord == "frac":
            pos = atom.fpos
        else:
            pos = atom.cpos
        f.write(' {}'.format(str(pos)[1:-1]))
        f.write(' {}\n'.format(atom.info))
                        

if __name__ == "__main__":
    # stand-alone mode
    if len(sys.argv) < 3:
        print('Usage: vasp.py infile outfile')
    else:
        infile = sys.argv[1]
        f = open(infile, 'r')
        print('Reading input VASP file "{}"'.format(infile))
        xstr = read(f, reportlevel=5)
        f.close()
        outfile = sys.argv[2]
        print('Writing output VASP file "{}"'.format(outfile))
        f = open(outfile, "w")
        write(xstr, f, reportlevel=5)
        f.close()
