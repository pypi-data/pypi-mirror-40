#!/usr/bin/env python

from __future__ import division, unicode_literals

import math
import itertools
import logging
import warnings
import copy
import os
import json
from fractions import Fraction

import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

from monty.fractions import lcm

import pymatgen as mg
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice

"""
Class for crystal structure
"""

__author__ = "Seong-Gon Kim, Mississippi State University"
__copyright__ = "Copyright 2018, Seong-Gon Kim"
__version__ = "1.0"
__maintainer__ = "Seong-Gon Kim"
__email__ = "sk162@msstate.edu"
__status__ = "alpha"
__date__ = "Dec 10, 2018"

logger = logging.getLogger(__name__)

class Xstructure(Structure):
    """
    Object for representing a crystal structure

    .. attribute:: structure

        Associated Structure.

    .. attribute:: name

        Optional name string.

    .. attribute:: info

        Optional info string.

    .. attribute:: selective_dynamics

        Selective dynamics attribute for each site. 
        A Nx3 array of booleans.

    .. attribute:: velocities

        Velocities for each site. 
        A Nx3 array of floats.

    .. attribute:: siteinfo

        Info for each site. 
        List of strings of size N.

    """

    def __init__(self, structure, name=None, info=None,
                 selective_dynamics=None,
                 velocities=None, 
                 siteinfo=None):
        """
        Makes a Xstructure, a Structure object with additional information
        and methods pertaining to a crystaline solid.

        Args:
            structure (Structure):  Structure object.
            name (str): Optional name of the crystal. 
                Defaults to unit cell formula of structure. 
            info (str): Optional info string
            selective_dynamics (Nx3 array): bool values for selective dynamics,
                where N is number of sites. Defaults to None.
            velocities (Nx3 array): Velocities for the sites.
            siteinfo ([str]): info string for each site.
        """

        site_properties = {}
        if selective_dynamics:
            site_properties["selective_dynamics"] = selective_dynamics
        if velocities:
            site_properties["velocities"] = velocities
        if siteinfo:
            site_properties["siteinfo"] = siteinfo
        structure = Structure.from_sites(structure)
        self.structure = structure.copy(site_properties=site_properties)

        if name is None:
            self.name = structure.formula
        else:
            self.name = name

        if info is None:
            self.info = ''
        else:
            self.info = info

    @property
    def lattice(self):
        return self.structure.lattice

    @property
    def velocities(self):
        return self.structure.site_properties.get("velocities")

    @property
    def selective_dynamics(self):
        return self.structure.site_properties.get("selective_dynamics")

    @property
    def siteinfo(self):
        return self.structure.site_properties.get("siteinfo")

    @velocities.setter
    def velocities(self, velocities):
        self.structure.add_site_property("velocities", velocities)

    @selective_dynamics.setter
    def selective_dynamics(self, selective_dynamics):
        self.structure.add_site_property("selective_dynamics",
                                         selective_dynamics)

    @siteinfo.setter
    def siteinfo(self, siteinfo):
        self.structure.add_site_property("siteinfo",
                                         siteinfo)

    @property
    def site_symbols(self):
        """
        Sequence of symbols associated with the structure. 
        Similar to 6th line in vasp 5+ POSCAR.
        """
        syms = [site.specie.symbol for site in self.structure]
        return [a[0] for a in itertools.groupby(syms)]

    @property
    def natoms(self):
        """
        Sequence of number of sites of each type associated with the Xstructure.
        Similar to 7th line in vasp 5+ POSCAR.
        """
        syms = [site.specie.symbol for site in self.structure]
        return [len(tuple(a[1])) for a in itertools.groupby(syms)]

    def __setattr__(self, name, value):
        if name in ("selective_dynamics", "velocities"):
            if value is not None and len(value) > 0:
                value = np.array(value)
                dim = value.shape
                if dim[1] != 3 or dim[0] != len(self.structure):
                    raise ValueError(name + " array must be same length as" +
                                     " the structure.")
                value = value.tolist()
        if name in ("siteinfo"):
            if value is not None and len(value) > 0:
                if len(value) != len(self.structure):
                    raise ValueError(name + " list must be same length as" +
                                     " the structure.")
                value = value.tolist()
        super().__setattr__(name, value)

    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of Poscar file.
        """
        return self.get_string()

    def get_string(self):
        """
        Returns a string representation of the Xstructure
        """

        lines = ['='*10 + ' Xstructure ' + '='*40]
        lines.append('Name: {}'.format(self.name))
        lines.append('Info: {}'.format(self.info))
        lines.append(self.lattice.__repr__())
        lines.append('Sites: {}'.format(len(self.structure)))

        header = 'INDX SPEC  (    FRAC_COORD      )  '
        header += '  [      CART_COORD      ]   '
        if self.selective_dynamics is not None:
            header += '(SDYN) '
        header += ' INFO '
        width = len(header)
        lines.append('-'*width)
        lines.append(header)
        lines.append('-'*width)

        for (i, site) in enumerate(self.structure):
            line = '{:>4} {:<3}'.format(i+1,site.species_string)
            vec = site.frac_coords
            line += ' ('+' '.join(['{:>7.4f}'.format(c) for c in vec])+')'
            vec = site.coords
            line += ' ['+' '.join(['{:>8.3f}'.format(c) for c in vec])+']'
            if self.selective_dynamics is not None:
                sd = ['T' if j else 'F' for j in self.selective_dynamics[i]]
                line += ' ('+' '.join([s for s in sd])+')'
            if self.siteinfo is not None:
                line += ' {}'.format(site.siteinfo)
            lines.append(line)
        lines.append('='*width)
        return '\n'.join(lines)

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "name": self.name,
                "info": self.info,
                "structure": self.structure.as_dict(),
                "selective_dynamics": np.array(
                    self.selective_dynamics).tolist(),
                "velocities": self.velocities,
                "siteinfo": self.siteinfo}

    @classmethod
    def from_dict(cls, d):
        return cls(Structure.from_dict(d["structure"]),
                   name=d["name"],
                   info=d["info"],
                   selective_dynamics=d["selective_dynamics"],
                   velocities=d.get("velocities", None),
                   siteinfo=d.get("siteinfo", None))

    def copy(self):
        """
        Convenience method to get a copy of the Xstructure
        """
        return Xstructure(self.structure, name=self.name, info=self.info,
                          selective_dynamics=self.selective_dynamics,
                          velocities=self.velocities, 
                          siteinfo=self.siteinfo)

if __name__ == "__main__":
    # stand-alone mode
    lattice = Lattice([[1, 2, -1], [3, 0, 1], [2, -2, 1]])
    print(lattice)
    fpos = np.array([1.0, 1.0, 0.5])
    print('fpos0=', fpos)
    cpos = lattice.get_cartesian_coords(fpos)
    print('cpos=', cpos)
    fpos1 = lattice.get_fractional_coords(cpos)
    print('fpos1=', fpos1)
    
    symbols = []
    coords = []
    sdyn = []
    siteinfo = []

    symbols.append('Hf')
    coords.append([1, 0, 0])
    sdyn.append([True, False, True])
    siteinfo.append('Hf1')

    symbols.append('S')
    coords.append([1, 0.5, 0])
    sdyn.append([True, True, True])
    siteinfo.append('S2')

    symbols.append('V')
    coords.append([0.2, -0.25, -0.75])
    sdyn.append([True, True, True])
    siteinfo.append('V3')

    symbols.append('Ca')
    coords.append([0.5, -0.52, 0.35])
    sdyn.append([True, True, False])
    siteinfo.append('Ca4')

    xstr = Xstructure(Structure(lattice, symbols, coords),
                      name='Test crystal structure',
                      selective_dynamics=sdyn,
                      siteinfo=siteinfo)
    print(xstr)
