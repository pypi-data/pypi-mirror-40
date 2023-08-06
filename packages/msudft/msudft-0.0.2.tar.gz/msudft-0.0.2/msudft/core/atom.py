#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from msudft.core import cmptlib

class Atom:
    """
    module for an atom
    """
    def __init__(self):
        self.id = 0
        self.type = ""
        self.info = ""
        self.cpos = np.array([0.0, 0.0, 0.0])
        self.fpos = np.array([0.0, 0.0, 0.0])

    def copy(self):
        cp = Atom()
        cp.id = self.id
        cp.type = self.type
        cp.info = self.info
        cp.cpos = self.cpos.copy()
        cp.fpos = self.fpos.copy()
        return cp

    def report(self, coord="frac"):
        print("Atom: #{} type={} info={}".format(
            self.id, self.type, self.info), end='')
        if coord == "frac":
            print(" fpos={}".format(cmptlib.list2str(self.fpos)))
        else:
            print(" cpos={}".format(cmptlib.list2str(self.cpos)))

if __name__ == "__main__":
    # stand-alone mode
    atom = Atom()
    atom.fpos = np.array([1, 0, 0])
    atom.cpos = np.dot(uc.f2c, atom.fpos)
    atom.report(coord="frac")
    atom.report(coord="cart")
    atom.fpos = np.array([1, 0.5, 0])
    atom.cpos = np.dot(uc.f2c, atom.fpos)
    atom.report(coord="frac")
    atom.report(coord="cart")
