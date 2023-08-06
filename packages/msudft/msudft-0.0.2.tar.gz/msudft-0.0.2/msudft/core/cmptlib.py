#!/usr/bin/env python

"""
cmptlib: library module for cmptools
"""

from __future__ import print_function
import math
import numpy as np
import numpy.linalg as la
import spglib

# tolerance for zero
ztol = 1.0e-10

def list2str(list):
    """
    Convert a list or array to a printable string
    """
    try:
        return '['+', '.join([str(x) for x in list])+']'
    except:
        return str(list)
        
def reduced_vector(vec, pbc):
    """
    Reduced vector with components in the range (-0.5, 0.5]
    """
    return np.array([reduced_number(v1, pbc1)
                     for (v1, pbc1) in zip(vec, pbc)]).reshape(vec.shape)

def reduced_number(v1, pbc1):
    """
    Reduced number in the range (-0.5, 0.5]
    """
    if pbc1:
        return v1 - math.ceil(v1-0.5)
    else:
        return v1

def normalize_frac(vlist):
    """
    Normalize the fractional coordinate
    """
    vlist1 = []
    for v in vlist:
        v = v - math.floor(v)
        vlist1.append(v)
    return vlist1

def py_ang(v1, v2):
    """
    Angle (in radian) between two vectors
    """
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def cell_volume(avec):
    """
    Volume of a cell defined by three vectors
    """
    v01 = np.cross(avec[0], avec[1])
    v012 = np.dot(v01, avec[2])
    return v012

def degree(rad):
    return rad*180.0/math.pi

def radian(deg):
    return deg*math.pi/180.0

def latt_leng_angle(avec):
    vlen = np.array([0.0, 0.0, 0.0])
    vang = np.array([0.0, 0.0, 0.0])
    for idir in range(3):
        jdir = (idir+1) % 3
        kdir = (jdir+1) % 3
        vlen[idir] = la.norm(avec[idir])
        vang[idir] = py_ang(avec[jdir], avec[kdir])
    return vlen, vang

def replicate(mol0, nrep):

    print('nrep = {}'.format(nrep))
    # set molecule
    mol1 = mol0.copy()
    # unit cell
    mol1.unitcell.lattParam = 1.0
    for aid in range(3):
        mol1.unitcell.avec[aid] = mol0.unitcell.avec[aid]*nrep[aid]
    mol1.unitcell.finalize()

    # Generate atoms
    mol1.atomlist = []
    for c0 in range(nrep[0]):
        for c1 in range(nrep[1]):
            for c2 in range(nrep[2]):
                dfpos = np.array([c0, c1, c2])
                for atom0 in mol0.atomlist:
                    atom1 = atom0.copy()
                    atom1.id = len(mol1.atomlist)+1
                    fpos = atom0.fpos + dfpos
                    cpos = np.dot(mol0.unitcell.f2c, fpos)
                    fpos = np.dot(mol1.unitcell.c2f, cpos)
                    atom1.fpos = fpos
                    atom1.cpos = cpos
                    mol1.atomlist.append(atom1)

    return mol1

class Neighbor:
    """
    class for a neighboring atom.
    """
    def __init__(self, atom, cell, dist, cpos):
        self.atom = atom
        self.cell = cell
        self.dist = dist
        self.cpos = cpos

def printNeighborMap(mol, cutoff, padding, onlyatoms, tol):

    crange = [1, 1, 1]
    for idir in range(3):
        if mol.unitcell.pbc[idir]:
            crange[idir] = padding[idir]
        else:
            crange[idir] = 0

    print('===========================================================')
    print('   PRINT NBRMAP   ')
    print('===========================================================')

    for atom1 in mol.atomlist:

        #check if we need to do this atom
        if len(onlyatoms) < 1:
            pass
        elif not(atom1.id in onlyatoms):
            continue

        cpos1 = np.dot(mol.unitcell.f2c, atom1.fpos)
        nbrlist1 = []
        for atom2 in mol.atomlist:
            for c0 in range(-crange[0], crange[0]+1):
                for c1 in range(-crange[1], crange[1]+1):
                    for c2 in range(-crange[2], crange[2]+1):
                        cell = np.array([c0, c1, c2])
                        fpos2 = atom2.fpos + cell
                        cpos2 = np.dot(mol.unitcell.f2c, fpos2)
                        dist = np.linalg.norm(cpos2 - cpos1)
                        if dist < tol:
                            pass
                        elif dist > cutoff:
                            pass
                        else:
                            nbr = Neighbor(atom2, cell, dist, cpos2)
                            nbrlist1.append(nbr)
        nbrlist1.sort(key=lambda nbr: nbr.dist)
        print('({} {}) ({:>12.8f} {:>12.8f} {:>12.8f})'.format(atom1.id, atom1.type, cpos1[0], cpos1[1], cpos1[2]))
        for index, nbr in enumerate(nbrlist1):
            print('    {:>3} {:>7.4f}'.format(index+1, nbr.dist), end=' ')
            print('({:>4} {:>2})'.format(nbr.atom.id, nbr.atom.type), end=' ')
            print('[{:>3}'.format(nbr.cell[0]), end=' ')
            print('{:>3}'.format(nbr.cell[1]), end=' ')
            print('{:>3}]'.format(nbr.cell[2]), end=' ')
            print('({:>12.8f}'.format(nbr.cpos[0]), end=' ')
            print('{:>12.8f}'.format(nbr.cpos[1]), end=' ')
            print('{:>12.8f})'.format(nbr.cpos[2]))
        print('==============================================================================')

def symmetry_map(poslist, numlist, rot, trans, pbc, tol = 1.0e-5):

    natom = len(poslist)
    nop = len(rot)
    sym_map = np.full((natom, nop), -1, dtype=int)
    for i0 in range(natom):
        p0 = poslist[i0]
        n0 = numlist[i0]
        for iop in range(nop):
            p1 = rot[iop].dot(p0) + trans[iop]
            for i2 in range(natom):
                n2 = numlist[i2]
                if n2 == n0:
                    p2 = poslist[i2]
                    dp = p1 - p2
                    dp = reduced_vector(dp, pbc)
                    dist = np.linalg.norm(dp)
                    if dist < tol:
                        sym_map[i0,iop] = i2+1
                        break

    return sym_map

def get_primitive_cell(mol, tol = 1.0e-5):
    """
    Find the primitive cell
    """
    cell = mol.get_spglib_cell()
    pcell = spglib.find_primitive(cell, symprec = tol)
    print('primitive cell=', pcell)
    pmol = mol.from_spglib_cell(pcell)
    pmol.name = 'Primitive cell of ' + mol.name
    pmol.info = 'Primitive cell generated by spglib.find_primitive()'
    return pmol

def translate(mol, sel, vec, coord="cart"):

    print('vec={}'.format(vec))
    mol1 = mol.copy()
    if coord == "frac":
        cvec = np.dot(mol.unitcell.f2c, vec)
    else:
        cvec = vec
    for ia,atom1 in enumerate(mol1.atomlist):
        if (ia+1) in sel.atoms:
            atom1.cpos = atom1.cpos + cvec
            atom1.fpos = np.dot(mol1.unitcell.c2f, atom1.cpos)
    return mol1

def reportSymmetry(mol, tol = 1.0e-5):

    # banner
    print('=====================')
    print('   REPORT SYMMETRY   ')
    print('=====================')

    # spglib cell from a molecule
    cell = mol.get_spglib_cell()
    print('cell=', cell)
    dataset = spglib.get_symmetry_dataset(cell, symprec = tol)

    print('\nSpace Group: {} {}'.format(
        dataset['number'], dataset['international']))
    print('Tolerance =', tol)
    print('Transformation matrix to the standardized basis vectors:')
    for vec in dataset['transformation_matrix']:
        print('  {:>10.6f} {:>10.6f} {:>10.6f} '.format(vec[0], vec[1], vec[2]))
    shift = dataset['origin_shift']
    print('Origin: {:>10.6f} {:>10.6f} {:>10.6f} '
          .format(shift[0], shift[1], shift[2]))
    equivat = dataset['equivalent_atoms']
    # symmetry operations
    rot = dataset['rotations']
    trans = dataset['translations']
    sym_map = symmetry_map(cell[1], cell[2], rot, trans,
                           mol.unitcell.pbc, tol)
    print('Symmetry operations: ', len(rot))
    print('----------------------------------------------------------')
    print('  OP    ROT[1]     ROT[2]     ROT[3]          TRANS       ')
    print('----- ---------- ---------- ---------- -------------------')
    for iop, (r, t) in enumerate(zip(rot, trans)):
        print('{:>4}:'.format(iop+1), end=' ')
        print('({:>2} {:>2} {:>2})'
              .format(r[0][0], r[0][1], r[0][2]), end=' ')
        print('({:>2} {:>2} {:>2})'
              .format(r[1][0], r[1][1], r[1][2]), end=' ')
        print('({:>2} {:>2} {:>2})'
              .format(r[2][0], r[2][1], r[2][2]), end=' ')
        print('({:>7.4f} {:>7.4f} {:>7.4f})'
              .format(t[0], t[1], t[2]))
    # set multiplicity
    multipl = np.zeros(len(equivat), dtype=np.int)
    for ia in range(len(equivat)):
        multipl[equivat[ia]] += 1
    for ia in range(len(equivat)):
        multipl[ia] = multipl[equivat[ia]]
    wyckoff = dataset['wyckoffs']
    print('---------------------------------------------------', end='')
    print('----'*len(rot))
    print('INDX SYMB    x        y        z     EQAT MULT WYKO', end='')
    for iop in range(len(rot)):
        print(' {:>3}'.format(iop+1), end='')
    print()
    print('---- ---- -------- -------- -------- ---- ---- ----', end='')
    print('----'*len(rot))
    for ia, atom in enumerate(mol.atomlist):
        print('{:>4}'.format(ia+1), end=' ')
        print('{:>4}'.format(atom.type), end=' ')
        print('{:>8.4f}'.format(atom.fpos[0]), end=' ')
        print('{:>8.4f}'.format(atom.fpos[1]), end=' ')
        print('{:>8.4f}'.format(atom.fpos[2]), end=' ')
        print('{:>4}'.format(equivat[ia]+1), end=' ')
        print('{:>4}'.format(multipl[ia]), end=' ')
        print('{:>4}'.format(wyckoff[ia]), end='')
        for iop in range(len(rot)):
            print(' {:>3}'.format(sym_map[ia,iop]), end='')
        print()
    print('---------------------------------------------------', end='')
    print('----'*len(rot))

    # primitive cell
    pc = get_primitive_cell(mol, tol)
    print('\n=== Primitive cell ===')
    pc.report()
    return pc

if __name__ == "__main__":
    # stand-alone mode
    a = [1, 2, 3]
    print('{} => {}'.format(a, list2str(a)))
    a = 3.5
    print('{} => {}'.format(a, list2str(a)))

    v1 = [1.0, 0.0, 0.0]
    v2 = [0.1, -2.0, 0.0]
    print('v1 = {}'.format(v1))
    print('v2 = {}'.format(v2))
    print('angle(v1,v2) = {} rad'.format(py_ang(v1,v2)))
    print('angle(v1,v2) = {} deg'.format(degree(py_ang(v1,v2))))

    v1 = [1.0, 0.0, 0.0]
    v2 = [1.2, 0.0, -0.01]
    print('v1 = {}'.format(v1))
    print('v2 = {}'.format(v2))
    m1 = la.norm(v1)
    m2 = la.norm(v2)
    print('norm(v1), norm(v2) = {}, {}'.format(m1, m2))
    ang12 = py_ang(v1,v2)
    print('angle(v1,v2) = {} rad'.format(ang12))
    print('angle(v1,v2) = {} deg'.format(degree(ang12)))
    print('dot(v1,v2) = {}'.format(np.dot(v1,v2)))
    print('|v1|.|v2|.cos(ang(v1,v2)) = {}'.format(m1*m2*np.cos(ang12)))
