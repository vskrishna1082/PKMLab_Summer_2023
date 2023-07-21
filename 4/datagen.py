#! /usr/bin/env python3
import numpy as np

# number of atoms
natoms = 1000
nmols = 10
system_size = 40.0

# number of bonds - linear polymer
nbonds = nmols*(natoms/nmols - 1)

# assign position to each atom
positions = []
for atom in range(natoms):
    positions.append(np.random.rand(3)*system_size)

# write Lammps data file
with open('random.data', 'w') as fdata:
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
    for idx,pos in enumerate(positions):
        fdata.write('{} 1 {} {} {}\n'.format(idx+1,*pos))
