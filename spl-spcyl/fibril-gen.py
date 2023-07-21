#!/usr/bin/env python3
# Single Fibril generator

############################################
#            System Details                #
############################################
#  90 molecules                            #
#  Arranged in a 30x3 grid                 #
#  Represents beta-sheet str               #
#                                          #
############################################

import numpy as np
import numba as nb
from mylmp import Atom

radius = 1.0
dist_horz = 2.0
dist_vert = 2.5
n_horz = 3
n_vert = 30
natoms = n_horz*n_vert

filename = 'fibril.xyz'

# posarray[i][j] -> ith row, jth atom - 30 rows x 3 columns
posarray = np.zeros((n_vert, n_horz, 3))


# Note: iterating over a np array is slow for large arrays
# but works fine here
def fill_posarray(arr):
    v, h, d = arr.shape
    out = np.empty((v, h, d), dtype=arr.dtype)
    for i in range(v):
        for j in range(h):
            out[i][j] = [dist_horz*j+radius,radius,dist_vert*i+radius]
    return out

posarray = fill_posarray(posarray)

# generate list of atoms
atoms = []
for i in range(natoms):
    myatom = Atom(i+1) # id of atom
    myatom.set_pos(*posarray[i//n_horz][i%n_horz])
    atoms.append(myatom)

with open(filename, 'w') as fdata:
    # number of atoms
    fdata.write('{}\n'.format(natoms))
    # title
    fdata.write('Fibril\n')
    # atom positions
    for atom in atoms:
        fdata.write('A {} {} {}\n'.format(*atom.pos))

# print after completion
print("Datafile generated successfully.")
