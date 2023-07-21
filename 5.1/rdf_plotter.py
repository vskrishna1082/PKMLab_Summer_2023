#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

myrdf = np.zeros((50,2))
headerlines = 3
plots = 100
height = 50
with open('tmp.rdf', 'r') as file:
    for i in range(headerlines):
        file.readline()
    for plot in range(plots):
        file.readline()
        counter = 0
        for line in range(height):
            a,b,c,d = file.readline().split()
            myrdf[counter][0] = float(b)
            myrdf[counter][1] += float(c)/100
            counter += 1

plt.plot(myrdf[:,0],myrdf[:,1])
plt.ylabel('Radial Distribution Function (lj units)')
plt.xlabel('Distance (lj units)')
plt.title('RDF of polymer')
plt.tight_layout()
plt.savefig('RDF.png')
