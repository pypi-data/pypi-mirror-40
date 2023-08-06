#!/usr/bin/env python
"""
makemol: Make/edit molecular/crystal structure file
"""

import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os
import math
import numpy as np
import spglib
import fileUtil
import Molecule
import Selection
import util
import cmptlib

class makemol:

    def __init__(self):

        self.moleculelist = {}
        self.selectionlist = {}

    def run(self, args):

        # set parameters
        self.ctrlfile = args.ctrlfile
        self.reportlevel = args.reportlevel
    
        # open control file
        try:
            self.ctrl = open(self.ctrlfile, 'r')
            if self.reportlevel > 0:
                print('%makemol: Reading control file "{}"'.format(self.ctrlfile))
        except IOError:
            util.Error('%makemol: Failed to open control file "{}"'.format(self.ctrlfile))

        # get the element tree
        self.tree = ET.parse(self.ctrl)
        self.ctrl.close()
        if self.reportlevel > 4:
            for node in tree.iter():
                print(node.tag, node.attrib)

        # root
        root = self.tree.getroot()
        print("root=", root.tag)
        if root.tag != "makemol":
            print("%makemol: Invalid control file for makemol.")
            util.Error('%makemol: The root tag must be "makemol"')

        # process each command
        stat = True
        for node in root.iter():
            stat = self.proc_cmd(node)

        # done
        print("%makemol: END")
        return True

    def proc_cmd(self, node):
        """
        Process one command
        """
        command = node.tag
        print("command = {}".format(command))

        if command == "makemol":
            pass

        elif command == "applySYMOP":
            mol = node.get("mol")
            op = node.get("op")
            dest = node.get("dest")
            self.applySYMOP(mol, op, dest)

        elif command == "checkSym":
            symGrp = node.get("group")
            self.checkSym(molecule, symGrp)

        elif command == "copy":
            self.copy(node)

        elif command == "diffMol":
            mol0 = node.get("mol0")
            mol1 = node.get("mol1")
            self.diffMol(mol0, mol1)

        elif command == "gen_equiv_atoms":
            self.gen_equiv_atoms(node)

        elif command == "set":
            self.set_param(node)

        elif command == "read":
            self.read(node)

        elif command == "replicate":
            self.replicate(node)

        elif command == "rotate":
            self.replicate(node)

        elif command == "select":
            Selection.process(self, node)

        elif command == "translate":
            self.translate(node)

        elif command == "write":
            self.write(node)

        elif command == "printNeighborMap":
            self.printNeighborMap(node)

        elif command == "reportSymmetry":
            self.reportSymmetry(node)

        else:
            util.Error('%makemol: Unrecognized command "{}"'.format(command))

    def applySYMOP(self, mid, expr, dest):
        if expr is None:
            print("%applySYMOP: missing symmetry operation expression.")
            return False
        mol = self.getMol(mid)
        if mol is None:
            print('%applySYMOP: Invalid molecule "{}"'.format(mid))
            return False
        if self.reportlevel > 0:
            print('%applySYMOP: applying op="{}" on mol="{}"'.format(expr, mid))
        mol2 = cmptlib.applySYMOP(mol, expr)
        mol2.id = dest
        if self.reportlevel > 3:
            print("%applySYMOP: dest molecule")
            mol2.report()
        nmol = self.addMol(mol2)
        return True

    def copy(self, node):
        mid = node.get("mol")
        if mid is None:
            util.Error("%makemol.copy: missing the source molecule name.")
        mol0 = self.moleculelist.get(mid)
        if mol0 is None:
            util.Error('%%makemol.copy: Invalid molecule "{}"'.format(mid))
        mol1 = mol0.copy()
        mid = node.get("dest")
        if mid is None:
            util.Error("%makemol.copy: missing the target molecule name.")
        mol1.id = mid
        if self.reportlevel >= 3:
            print("%makemol.copy: dest molecule")
            mol1.report()

    def diffMol(self, mid0, mid1):
        # difference between two molecules
        mol0 = self.getMol(mid0)
        if mol0 is None:
            return False
        mol1 = self.getMol(mid1)
        if mol1 is None:
            return False
        return cmptlib.diffMol(mol0, mol1)

    def gen_equiv_atoms(self, node):
        mid = node.get("mol")
        if mid is None:
            raise EX.inputError("Missing input molecule name.")
        mol = self.moleculelist.get(mid)
        if mol is None:
            raise EX.inputError('Invalid molecule "{}"'.format(mid))
        spcgrp = node.get("spacegroup")
        if spcgrp is None:
            raise EX.inputError("Missing space group name.")
        cmptlib.gen_equiv_atoms(mol, spcgrp)

    def printNeighborMap(self, node):
        mol = util.get_molecule("mol", node, self)
        cutoff = util.get_float("cutoff", node, req=False, default="5.0")
        padding = util.get_list("padding", node, req=False, default="[1,1,1]")
        onlyatoms = util.get_list("onlyatoms", node, req=False, default=None)
        tol = util.get_float("tolerance", node, req=False, default="1.0e-4")

        cmptlib.printNeighborMap(mol, cutoff, padding, onlyatoms, tol)

    def read(self, node):
        fname = util.get_string("file", node)
        fmt = util.get_string("format", node, req=False)
        option = util.get_string("option", node, req=False)
        mol = fileUtil.read(fname, fmt=fmt, option=option,
                            reportlevel=self.reportlevel)
        mol.id = util.get_string("mol", node)
        self.moleculelist.update({mol.id:mol})

        if self.reportlevel >= 3:
            mol.report("%makemol.read: Current molecule")

    def replicate(self, node):
        mol = util.get_molecule("mol", node, self)
        nrep = util.get_list("nrep", node)
        mol1 = cmptlib.replicate(mol, nrep)
        if self.reportlevel >= 3:
            mol1.report("%makemol.replicate:  molecule")
        mol1.id = util.get_string("outmol", node)
        self.moleculelist.update({mol1.id:mol1})

    def reportSymmetry(self, node):
        mol = util.get_molecule("mol", node, self)
        tol = util.get_float("tolerance", node, req=False, default="1.0e-4")
        pcmol = cmptlib.reportSymmetry(mol, tol=tol)
        pcmol.id = util.get_string("pcmol", node, req=False)
        if pcmol.id is not None:
            self.moleculelist.update({pcmol.id:pcmol})

    def translate(self, node):
        sel = util.get_selection("sel", self, node)
        vec = util.get_list("vec", node)
        coord = util.get_string("coord", node, req=False)
        self.molecule = cmptlib.translate(self.molecule, sel, vec, coord)
        if self.reportlevel >= 3:
            print("%translate: modified molecule")
            self.molecule.report()

    def set_param(self, node):
        for name, value in node.items():
            print('%makemol.set_param: {0} = {1}'.format(name, value))
            if name == "title":
                self.title = value
            elif name == "reportlevel":
                self.reportlevel = int(value)

    def write(self, node):
        mol = util.get_molecule("mol", node, self)
        fname = util.get_string("file", node)
        fmt = util.get_string("format", node)
        coord = util.get_string("coord", node, req=False)
        option = util.get_string("option", node, req=False)
        fileUtil.write(mol, fname, fmt=fmt, coord=coord,
                       option=option, reportlevel=self.reportlevel)

if __name__ == "__main__":
    # stand-alone mode
    import argparse
    parser = argparse.ArgumentParser(
        description='Edit a molecular structure file')
    parser.add_argument('ctrlfile', help='control file')
    parser.add_argument('--reportlevel', type=int, default=4,
                        help='Report level index (0-5)')

    args = parser.parse_args()

    app = makemol()
    stat = app.run(args)
