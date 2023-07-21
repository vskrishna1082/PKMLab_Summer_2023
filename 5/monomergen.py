#! /usr/bin/env python3
# xyz data generation file
natoms = 50
title = 'polymer'
atomtype = 'A'
coord = [0.0,0.0,0.0]
filename = 'polymer.xyz'
with open(filename, 'w') as fdata:
    fdata.write('{}\n'.format(natoms))
    fdata.write('{}\n'.format(title))
    for atom in range(natoms):
        fdata.write('{} {:.1f} {:.1f} {:.1f}\n'.format(atomtype, *coord))
        for idx,coordinate in enumerate(coord):
            coord[idx] = (coordinate + 0.1)
