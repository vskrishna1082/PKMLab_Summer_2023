#! /usr/bin/env python3
# Lammps datafile generator
# * linear polymers
# * atom_type molecular

import numpy as np
import sys
from mylmp import atom

# filename
filename = 'spcyl.data'

# number of atoms
nmols = 400
system_size = 100.0
vel_max = 2.0

xyzfie = 'spcyl-packed.xyz'
xyz = open(xyzfie, 'r')
natoms = int(xyz.readline())
title = xyz.readline()

# number of bonds - linear polymer
nbonds = int(nmols*(natoms/nmols - 1))

# length/number of atoms in a molecule
len_mol = natoms/nmols

index = 0
posarray = np.zeros((natoms, 3))
for i,line in enumerate(xyz):
    temp_atom,x,y,z = line.split()
    posarray[i]= np.array([float(x),float(y),float(z)])
xyz.close()

# generate list of velocities per mol
vels = []
for i in range(nmols):
    vels.append(np.random.rand(3)*vel_max)

# generate list of atoms
atoms = []
for i in range(natoms):
    myatom = atom(i+1) # id of atom
    myatom.set_pos(*posarray[i])
    myatom.mol_id = i//nmols + 1
    myatom.vel = vels[myatom.mol_id-1]
    atoms.append(myatom)

# bond pairs
bonds = []
for i in range(natoms):
    # skip first atom of each molecule
    if i%len_mol == 0:
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
bondlen = get_avg_bondlen()
bond_k = 30
print('Average Bond Length = {}'.format(bondlen))

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

    # mass
    fdata.write('Masses\n\n')
    fdata.write('1 1\n')
    fdata.write('\n')

    # bond coeffs
    fdata.write('Bond Coeffs\n\n')
    fdata.write('1 {} {}\n'.format(bond_k, bondlen))
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
