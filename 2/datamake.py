#! /usr/bin/env python3

idx = 1
pos = 0.5
for i in range(20):
    print("{} 1 1 {} {} {} 0 0 0 0".format(idx,pos,pos,pos))
    idx+=1
    pos+=1
