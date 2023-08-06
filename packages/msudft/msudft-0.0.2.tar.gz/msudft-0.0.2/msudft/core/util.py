#!/usr/bin/env python

"""
util: convenience utility module
"""

from __future__ import print_function
import sys
import os
from msudft import Xstructure
from msudft.io import xstr, vasp, pdb, chgcar, xsf, xyz

def Error(msg):
    """
    Error handler
    """
    print(msg)
    sys.exit(0)

def Warn(msg):
    """
    Warning handler
    """
    print(msg)

def get_string(key, node, req=True, default=None):

    s = node.get(key, default=default)
    if req and s is None:
        Error('%makemol: Missing required key "{}"'.format(key))
    return s

def get_bool(key, node, req=True, default=None):

    s = get_string(key, node, req=req, default=default)
    try:
        v = bool(s)
    except IOError:
        Error('%makemol: Invalid boolean value "{}"'.format(s))
    return v

def get_float(key, node, req=True, default=None):

    s = get_string(key, node, req=req, default=default)
    try:
        v = float(s)
    except IOError:
        Error('%makemol: Invalid float value "{}"'.format(s))
    return v

def get_list(key, node, req=True, default=None):

    s = get_string(key, node, req=req, default=default)
    try:
        v = list(eval(s))
    except IOError:
        Error('%makemol: Invalid list value "{}"'.format(s))
    return v

def get_molecule(key, node, system):

    mid = get_string(key, node, req=True)
    mol = system.moleculelist.get(mid)
    if mol is None:
        Error('%makemol: Invalid molecule "{}"'.format(mname))
    return mol

def get_selection(key, node, system):

    sid = get_string(key, node, req=True)
    sel = system.selectionlist.get(sid)
    if sel is None:
        Error('%makemol: Invalid selection "{}"'.format(sid))
    return sel

def read_next_line(f):
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Discard comments and empty lines
        return line

def read_from_file(infile, fmt=None, option=None, verbose=0):
    """
    Read a molecule from an input file "infile"
    """
    if fmt == None:
        fmt = os.path.splitext(infile)[1][1:]
    if verbose > 3:
        print('Input format =', fmt)

    if fmt == "xstr":
        xstr = xstr.read(infile, verbose)
    elif fmt == "pdb":
        xstr = pdb.read(infile, verbose)
    elif fmt == "fdf":
        xstr = fdf.read(infile, verbose)
    elif fmt == "vasp" or fmt == "poscar":
        xstr = vasp.read(infile)
    elif fmt == "xsf":
        xstr = xsf.read(infile, verbose)
    elif fmt == "xyz":
        xstr = xyz.read(infile, verbose)
    else:
        Error('%msudft: Unrecognized format "{}"'.format(fmt))

    return xstr

def write_to_file(mol, outfile, fmt=None, coord=None, option=None,
                  verbose=0):
    """
    Write a molecule to an output file
    """
    # open output file
    try:
        f = open(outfile, 'w')
        print('Writing output file "{}"'.format(outfile))
    except IOError:
        Error('%msudft: Failed to open output file "{}"'.format(outfile))

    if fmt == None:
        fmt = os.path.splitext(outfile)[1][1:]
    if verbose > 3:
        print('Output format =', fmt)
    if fmt == "xstr":
        xstr.write(mol, f, coord, verbose)
    elif fmt == "fdf":
        fdf.write(mol, f, coord, verbose)
    elif fmt == "pdb":
        pdb.write(mol, f, verbose)
    elif fmt == "vasp" or fmt == "poscar":
        vasp.write(mol, f, coord, verbose)
    elif fmt == "xsf":
        xsf.write(mol, f, verbose)
    else:
        Error('%msudft: Unrecognized format "{}"'.format(fmt))

if __name__ == "__main__":
    # stand-alone mode

    pass
