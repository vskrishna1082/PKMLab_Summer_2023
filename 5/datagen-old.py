#! /usr/bin/env python3
# Lammps datafile generator
# * linear polymers
# * atom_type molecular

import numpy as np
import sys
from mylmp import atom

# filename
filename = 'polymer.data'

# number of atoms
natoms = 100
nmols = 10
system_size = 10.0

# number of bonds - linear polymer
nbonds = int(nmols*(natoms/nmols - 1))

# assign position to each atom
# posarray = np.random.rand(natoms,3)*system_size
posarray = np.random.rand(natoms,3)
# sort all pos s.t. i is close to i+1 - does not work!!!
def sort_posarray(posarray)
    def get_dist(pos1,pos2):
        return np.sum((pos1-pos2)**2)

    idx_list = list(range(natoms))
    curr_idx = 0
    while curr_idx < natoms-1:
        nn_idx = curr_idx+1 # use next in list as first nearest trial
        dist_nn = get_dist(posarray[curr_idx], posarray[nn_idx])

        # loop through all subsequent indices to look for neighbors
        for i in range(curr_idx+1, natoms):
            dist = get_dist(posarray[curr_idx], posarray[idx_list[i]])
            if dist_nn > dist:
                nn_idx = i
                dist_nn = dist
        # move the neighbor to right of curr_idx
        idx_list.insert(curr_idx+1, idx_list.pop(nn_idx))
        curr_idx += 1 # increment current index

    return posarray[idx_list]

# generate list of atoms
atoms = []
for i in range(natoms):
    myatom = atom(i+1) # id of atom
    myatom.set_pos(*posarray[i])
    myatom.mol_id = i//nmols + 1
    atoms.append(myatom)

# bond pairs
bonds = []
for i in range(natoms):
    # skip first atom of each molecule
    if i%nmols == 0:
        continue
    # join atom to previous atom
    bonds.append((i,i+1)) # add 1 to adjust for 0
# sanity check
if len(bonds) != nbonds:
    raise UserWarning('Computed and specified number of bonds did not match!')

# compute average bond length
def get_avg_bondlen():
    avg = 0
    for bond in bonds:
        pos1 = atoms[bond[0]-1].pos
        pos2 = atoms[bond[1]-1].pos
        dist = 0
        for i in range(len(pos1)):
            dist+=(pos1[i] - pos2[i])**2
        dist = np.sqrt(dist)
        avg+=dist
    avg /= nbonds
    return avg
print(get_avg_bondlen())

# write Lammps data file
with open(filename, 'w') as fdata:
    # comment line
    fdata.write("LAMMPS Data File for polymers\n\n")

    # Header
    # atom no. and type
    fdata.write('{} atoms\n'.format(natoms))
    fdata.write('{} bonds\n'.format(nbonds))
    fdata.write('{} atom types\n'.format(1))
    fdata.write('{} bond types\n'.format(1))
    fdata.write('\n')

    # box dimensions
    fdata.write('{} {} xlo xhi\n'.format(0.0,system_size))
    fdata.write('{} {} ylo yhi\n'.format(0.0,system_size))
    fdata.write('{} {} zlo zhi\n'.format(0.0,system_size))
    fdata.write('\n')

    # atoms section
    fdata.write('Atoms\n\n')
    for atom in atoms:
        fdata.write('{} {} {} {} {} {} {}\n'.format(atom.id,
                                               atom.mol_id,
                                               atom.atom_type,
                                               atom.charge,
                                               *atom.pos))
    fdata.write('\n')

    # velocity section
    fdata.write('Velocities\n\n')
    for atom in atoms:
        fdata.write('{} {} {} {}\n'.format(atom.id, *atom.vel))
    fdata.write('\n')

    # bonds section
    fdata.write('Bonds\n\n')
    for idx,bond in enumerate(bonds):
        fdata.write('{} 1 {} {}\n'.format(idx+1, *bond))

# print after completion
print("Datafile '{}' created.".format(filename))
print("{} Atoms.".format(natoms))
print("{} Molecules.".format(nmols))
print("{} Bonds.".format(nbonds))
