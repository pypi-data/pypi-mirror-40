#!/usr/bin/env python

from . import util, cmptlib
import numpy as np

class Selection:
    """
    module for selection of atoms
    """
    def __init__(self, sid=None):
        self.sid = sid
        self.data = dict({})

    def add(self, mid, atoms):
        if mid in self.data:
            self.data[mid].update(atoms)
        else:
            self.data.update({mid:atoms})

    def difference(self, sel2):
        sel3 = Selection()
        mols = [m for m in self.data.keys() if m in sel2.data.keys()]
        for m in mols:
            s1 = self.data[m]
            s2 = sel2.data[m]
            s3 = s1.difference(s2)
            if len(s3) > 0:
                sel3.add(m, s3)
        return sel3 

    def intersection(self, sel2):
        sel3 = Selection()
        mols = [m for m in self.data.keys() if m in sel2.data.keys()]
        for m in mols:
            s1 = self.data[m]
            s2 = sel2.data[m]
            s3 = s1.intersection(s2)
            if len(s3) > 0:
                sel3.add(m, s3)
        return sel3 

    def report(self, header=None):
        if header is not None:
            print(header)
        print('Selection: {}'.format(self.sid))
        print(self.data)

    def union(self, sel2):
        sel3 = Selection()
        mols = [m for m in self.data.keys() if m in sel2.data.keys()]
        for m in mols:
            s1 = self.data[m]
            s2 = sel2.data[m]
            s3 = s1.union(s2)
            if len(s3) > 0:
                sel3.add(m, s3)
        return sel3 

def process(system, node):
    """
    Process a select command
    """
    action = node.get("action", default="add")

    if action == "add":
        add(system, node)
    elif action == "difference":
        difference(system, node)
    elif action == "intersection":
        intersection(system, node)
    elif action == "report":
        report(system, node)
    elif action == "union":
        union(system, node)
    else:
        util.Error('%select: Unrecognized action "{}"'.format(action))
        
def add(system, node):

    mol = util.get_molecule("mol", node, system)
    slist = util.get_string("atoms", node, default="*")
    if slist == '*':
        atoms = range(1,len(mol.atomlist)+1)
    else:
        try:
            atoms = eval(slist)
        except IOError:
            util.Error('%select: Invalid atoms list "{}"'.format(slist))

    sid = util.get_string("sel", node)
    sel = system.selectionlist.get(sid)
    if sel is None:
        sel = Selection(sid)
    sel.add(mol.id, atoms)
    system.selectionlist.update({sid:sel})

def difference(system, node):

    sel1 = util.get_selection("sel1", node, system)
    sel2 = util.get_selection("sel2", node, system)
    sel = sel1.difference(sel2)
    sid = util.get_string("sel", node)
    sel.sid = sid
    system.selectionlist.update({sid:sel})

def intersection(system, node):

    sel1 = util.get_selection("sel1", node, system)
    sel2 = util.get_selection("sel2", node, system)
    sel = sel1.intersection(sel2)
    sid = util.get_string("sel", node)
    sel.sid = sid
    system.selectionlist.update({sid:sel})

def report(system, node):

    sel = util.get_selection("sel", node, system)
    header = util.get_string("header", node, req=False)
    sel.report(header)

def union(system, node):

    sel1 = util.get_selection("sel1", node, system)
    sel2 = util.get_selection("sel2", node, system)
    sel = sel1.union(sel2)
    sid = util.get_string("sel", node)
    sel.sid = sid
    system.selectionlist.update({sid:sel})

if __name__ == "__main__":
    # stand-alone mode
    sel1 = Selection('sel1')
    print('sel1 after adding mol1')
    sel1.add('mol1', {1, 3, 5, 14})
    sel1.report()
    sel1.add('mol1', {2, 3, 4, 5, 14})
    sel1.report()
    print('sel1 after adding mol0')
    sel1.add('mol0', {1, 2, 3, 6})
    sel1.report()

    sel2 = Selection('sel2')
    sel2.add('mol1', {2, 3, 7, 8, 12, 14, 15})
    sel2.report()
    sel2.add('mol0', {3, 5, 6, 8})
    sel2.report()

    sel3 = sel1.intersection(sel2)
    sel3.sid = 'sel1.intersection.sel2'
    sel3.report()

    sel4 = sel1.union(sel2)
    sel4.sid = 'sel1.union.sel2'
    sel4.report()

    sel5 = sel1.difference(sel2)
    sel5.sid = 'sel1.difference.sel2'
    sel5.report()
