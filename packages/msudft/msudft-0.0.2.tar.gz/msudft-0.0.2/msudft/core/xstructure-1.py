#!/usr/bin/env python

from __future__ import division, unicode_literals

import os
import itertools
import warnings
import logging

import numpy as np

from monty.io import zopen
from monty.os.path import zpath

import pymatgen as mg
from monty.json import MSONable

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


class Xstructure(MSONable):
    """
    Object for representing a crystal structure

    Args:
        structure (Structure):  Structure object.
        name (str): Optional name of the crystal. 
                    Defaults to unit cell formula of structure. 
        info (str): Optional info string
        selective_dynamics (Nx3 array): bool values for selective dynamics,
            where N is number of sites. Defaults to None.
        velocities (Nx3 array): Velocities for the sites.
        siteinfo (N list): info string for each site.

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
        if structure.is_ordered:
            site_properties = {}
            if selective_dynamics:
                site_properties["selective_dynamics"] = selective_dynamics
            if velocities:
                site_properties["velocities"] = velocities
            if siteinfo:
                site_properties["siteinfo"] = siteinfo
            structure = Structure.from_sites(structure)
            self.structure = structure.copy(site_properties=site_properties)
            self.name = structure.formula if name is None else name
            self.info = info
        else:
            raise ValueError("Structure with partial occupancies cannot be "
                             "converted into Xstructure!")

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


    def get_string(self, frac=True, 
                   significant_figures=6):
        """
        Returns a string representation of the Xstructure

        Args:
            frac (bool): Whether coordinates are output in fractional or
                cartesian. Defaults to True.
            significant_figures (int): No. of significant figures to
                output all quantities. Defaults to 6. Note that positions are
                output in fixed point, while velocities are output in
                scientific format.

        Returns:
            String representation of Xstructure.
        """

        format_str = "{{:.{0}f}}".format(significant_figures)
        buf = io.StringIO()
        print('<< Xstructure: ', self.name, file=buf)
        print('Info: ', self.info, file=buf)
        print(self.lattice.__repr__(), file=buf)
        print("Sites:", len(self.structure), file=buf)
        hbar = '---- ---- -------------- ------------- ------------- --------'
        print(hbar, file=buf)
        print('indx TYPE    avec[1]        avec[2]       avec[3]      info  ', file=buf)
        print(hbar, file=buf)
        for (i, site) in enumerate(self.structure):
            print('{:>4}'.format(i+1), end=' ', file=buf)
            coords = site.frac_coords if direct else site.coords
            line = " ".join([format_str.format(c) for c in coords])
            if self.selective_dynamics is not None:
                sd = ["T" if j else "F" for j in self.selective_dynamics[i]]
                line += " %s %s %s" % (sd[0], sd[1], sd[2])
            line += " " + site.species_string
            lines.append(line)

            print(' {:>3}'.format(atom.type), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[0]), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[1]), end=' ', file=buf)
            print(' {:>12.8f}'.format(atom.fpos[2]), end=' ', file=buf)
            print(' | {}'.format(atom.info), file=buf)
        print(hbar, file=buf)
        return buf.getvalue()

    lines = ['Xstructure: ' self.name]
        lines.append(self.info)
        for v in latt.matrix:
            lines.append(" ".join([format_str.format(c) for c in v]))

        if self.true_names and not vasp4_compatible:
            lines.append(" ".join(self.site_symbols))
        lines.append(" ".join([str(x) for x in self.natoms]))
        if self.selective_dynamics:
            lines.append("Selective dynamics")
        lines.append("direct" if direct else "cartesian")

        for (i, site) in enumerate(self.structure):
            coords = site.frac_coords if direct else site.coords
            line = " ".join([format_str.format(c) for c in coords])
            if self.selective_dynamics is not None:
                sd = ["T" if j else "F" for j in self.selective_dynamics[i]]
                line += " %s %s %s" % (sd[0], sd[1], sd[2])
            line += " " + site.species_string
            lines.append(line)

        if self.velocities:
            try:
                lines.append("")
                for v in self.velocities:
                    lines.append(" ".join([format_str.format(i) for i in v]))
            except:
                warnings.warn("Velocities are missing or corrupted.")

        if self.siteinfo:
            lines.append("")
            if self.siteinfo_preamble:
                lines.append(self.siteinfo_preamble)
                pred = np.array(self.siteinfo)
                for col in range(3):
                    for z in pred[:,col]:
                        lines.append(" ".join([format_str.format(i) for i in z]))
            else:
                warnings.warn(
                    "Preamble information missing or corrupt. " 
                    "Writing Poscar with no predictor corrector data.")

        return "\n".join(lines) + "\n"

    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of Poscar file.
        """
        return self.get_string()

    def write_file(self, filename, **kwargs):
        """
        Writes POSCAR to a file. The supported kwargs are the same as those for
        the Poscar.get_string method and are passed through directly.
        """
        with zopen(filename, "wt") as f:
            f.write(self.get_string(**kwargs))

    def as_dict(self):
        return {"@module": self.__class__.__module__,
                "@class": self.__class__.__name__,
                "structure": self.structure.as_dict(),
                "true_names": self.true_names,
                "selective_dynamics": np.array(
                    self.selective_dynamics).tolist(),
                "velocities": self.velocities,
                "siteinfo": self.siteinfo,
                "comment": self.comment}

    @classmethod
    def from_dict(cls, d):
        return Poscar(Structure.from_dict(d["structure"]),
                      comment=d["comment"],
                      selective_dynamics=d["selective_dynamics"],
                      true_names=d["true_names"],
                      velocities=d.get("velocities", None),
                      siteinfo=d.get("siteinfo", None))

    def set_temperature(self, temperature):
        """
        Initializes the velocities based on Maxwell-Boltzmann distribution.
        Removes linear, but not angular drift (same as VASP)

        Scales the energies to the exact temperature (microcanonical ensemble)
        Velocities are given in A/fs. This is the vasp default when
        direct/cartesian is not specified (even when positions are given in
        direct coordinates)

        Overwrites imported velocities, if any.

        Args:
            temperature (float): Temperature in Kelvin.
        """
        # mean 0 variance 1
        velocities = np.random.randn(len(self.structure), 3)

        # in AMU, (N,1) array
        atomic_masses = np.array([site.specie.atomic_mass.to("kg")
                                  for site in self.structure])
        dof = 3 * len(self.structure) - 3

        # scale velocities due to atomic masses
        # mean 0 std proportional to sqrt(1/m)
        velocities /= atomic_masses[:, np.newaxis] ** (1 / 2)

        # remove linear drift (net momentum)
        velocities -= np.average(atomic_masses[:, np.newaxis] * velocities,
                                 axis=0) / np.average(atomic_masses)

        # scale velocities to get correct temperature
        energy = np.sum(1 / 2 * atomic_masses *
                        np.sum(velocities ** 2, axis=1))
        scale = (temperature * dof / (2 * energy / const.k)) ** (1 / 2)

        velocities *= scale * 1e-5  # these are in A/fs

        self.temperature = temperature
        try:
            del self.structure.site_properties["selective_dynamics"]
        except KeyError:
            pass

        try:
            del self.structure.site_properties["siteinfo"]
        except KeyError:
            pass
        # returns as a list of lists to be consistent with the other
        # initializations

        self.structure.add_site_property("velocities", velocities.tolist())


