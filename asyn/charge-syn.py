#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
from Bio.SeqUtils.ProtParam import ProteinAnalysis

phys_pH = 7
structfile = 'primary_struct.txt'
struct = open(structfile, 'r').readline()

charge_list = []
for i in struct:
    charge_list.append(ProteinAnalysis(i).charge_at_pH(phys_pH))

fig,ax = plt.subplots(figsize=(10,2))
sns.heatmap([charge_list], cmap='bwr', cbar_kws={"orientation": "horizontal"}, xticklabels=False)
plt.tight_layout()
plt.savefig("asyn-charge_distrib.png")
