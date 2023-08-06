#!/usr/bin/env python
"""
Module for xstr file I/O
"""

from __future__ import print_function
import xml.etree.ElementTree as ET
import numpy as np
from ..core import Xstructure, Unitcell, Atom
from ..core import cmptlib

def read(infile, verbose=0):
    # open input file
    try:
        f = open(infile, 'r')
        print('Reading input file "{}"'.format(infile))
    except IOError:
        Error('Failed to open input file "{}"'.format(infile))

    # get the element tree
    tree = ET.parse(f)
    if verbose > 8:
        print("%xstr.read: printing nodes")
        for node in tree.iter():
            print(node.tag, node.attrib)

    # convert the tree to a X-structure
    xstr = Xstructure()
    node = tree.find("name")
    if node != None:
        if node.text != None:
            xstr.name = node.text.strip()
    node = tree.find("info")
    if node != None:
        if node.text != None:
            xstr.info = node.text.strip()
    xstr.unitcell = _read_unitcell(tree)
    xstr.frac_coord, xstr.atomlist = _read_atomlist(
        tree, xstr.unitcell.c2f, xstr.unitcell.f2c)

    return xstr

def _read_unitcell(tree):
    uc = Unitcell()
    node = tree.find('unitcell')
    if node is None:
        raise Exception("<unitcell> tag missing")
    for elem in node.iter():
        if elem.tag == "unitcell":
            uc.type = elem.get("type", default="general")
        if elem.tag == "lattParam":
            uc.lattParam = float(elem.get("value", default=1.0))
        if elem.tag == "pbc":
            svec = elem.get("vector")
            if svec == None:
                raise Exception('%xstr-error: "vector" is missing in <pbc> tag')
            uc.pbc = eval(svec)
        if elem.tag == "axis":
            aname = elem.get("name")
            try:
                aid = ["a1","a2","a3"].index(aname)
            except ValueError:
                raise Exception(
                    '%xstr-error: Invalid axis name "{}"'.format(aname))
            svec = elem.get("vector")
            if svec == None:
                raise Exception('%xstr-error: "vector" is missing in <axis> tag')
            avec = np.array(eval(svec), dtype=float)
            uc.avec[aid] = avec*uc.lattParam
    uc.finalize()
    return uc

def _read_atomlist(tree, c2f, f2c):
    atomlist = []
    node = tree.find("atomlist")
    if node == None:
        raise Exception("<atomlist> tag missing")
    coord = node.get("coord")
    if coord == None:
        raise Exception('"<atomlist coord" attribute missing')
    elif coord in ["frac", "cart"]:
        pass
    else:
        raise Exception('%xstr-error: invalid coord value "{}"'.format(coord))

    for elem in node.iter():
        if elem.tag == "atom":
            atom = Atom()
            atom.id = len(atomlist)+1
            atom.type = elem.get("type", default="??")
            svec = elem.get("pos")
            if svec == None:
                raise Exception('%xstr-error: "pos" is missing in <atom> tag')
            pos = np.array(eval(svec), dtype=float)
            if coord == "frac":
                atom.fpos = pos
                atom.cpos = np.dot(f2c, pos)
            else:
                atom.cpos = pos
                atom.fpos = np.dot(c2f, pos)
            atom.info = elem.get("info", default="")
            atomlist.append(atom)

    return coord, atomlist

def write(xstr, f, coord=None, verbose=0):
    # Header
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<Xstructure>\n')
    f.write('  <name>{}</name>\n'.format(xstr.name))
    f.write('  <info>{}</info>\n'.format(xstr.info))
    # Unitcell
    f.write('  <unitcell>\n')
    f.write('    <pbc vector="{}" />\n'.format(
        cmptlib.list2str(xstr.unitcell.pbc)))
    f.write('    <lattParam value="{}" />\n'.format(
        xstr.unitcell.lattParam))
    for aid in range(3):
        avec = xstr.unitcell.avec[aid]/xstr.unitcell.lattParam
        f.write('    <axis name="a{}" vector="{}" />\n'.format(
            aid+1,cmptlib.list2str(avec)))
    f.write('  </unitcell>\n')
    # atomlist
    if coord == None:
        coord = xstr.atomcoord
    f.write('  <atomlist coord="{}" >\n'.format(coord))
    for iatm, atom in enumerate(xstr.atomlist):
        s = '    <atom id="{}"'.format(iatm+1)
        s += ' type="{}"'.format(atom.type)
        if coord == "frac":
            pos = atom.fpos
        else:
            pos = np.dot(xstr.unitcell.f2c, atom.fpos)
        s += ' pos="{}"'.format(cmptlib.list2str(pos))
        s += ' info="{}" />\n'.format(atom.info)
        f.write(s)
    f.write('  </atomlist>\n')
    f.write('</Xstructure>\n')

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='xstr.py: Read and write a xstr format file')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('--coord', default=None, choices=['frac', 'cart'],
                        help='coord system for output file')

    args = parser.parse_args()

    f = open(args.infile, 'r')
    xstr = read(f, verbose=5)
    f.close()
    f = open(args.outfile, 'w')
    write(xstr, f, verbose=5)
    f.close()
