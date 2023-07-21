#! /usr/bin/env python3

class Atom:
    def __init__(self, id):
        self.id = id
    pos = [0,0,0]
    vel = [0,0,0]
    mass = 1
    mol_id = 1
    charge = 0
    atom_type = 1
    def set_pos(self, x,y,z):
        self.pos = [x,y,z]
    def set_vel(self, vx,vy,vz):
        self.vel= [vx,vy,vz]
