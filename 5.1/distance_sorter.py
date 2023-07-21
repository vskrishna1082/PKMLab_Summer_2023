#! /usr/bin/env python3
import numpy as np

list_len = 100
posarray = (np.random.rand(list_len, 3)*10).astype(int)

def get_dist(pos1,pos2):
    return np.sum(np.absolute(pos1-pos2))

idx_list = list(range(list_len))
curr_idx = 0
while curr_idx < list_len-1:
    nn_idx = curr_idx+1 # use next in list as first nearest trial
    dist_nn = get_dist(posarray[curr_idx], posarray[nn_idx])

    # loop through all subsequent indices to look for neighbors
    for i in range(curr_idx+1, 10):
        dist = get_dist(posarray[curr_idx], posarray[idx_list[i]])
        if dist_nn > dist:
            nn_idx = i
            dist_nn = dist
    # move the neighbor to right of curr_idx
    idx_list.insert(curr_idx+1, idx_list.pop(nn_idx))
    curr_idx += 1 # increment current index

posarray = posarray[idx_list]
