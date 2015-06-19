#!/usr/bin/env python
# coding: utf8

# all from bio.py in this namespace
from bio import *

# data
test = [1, 2, 3]
trial = [4, 5, 6, 7]
val = 2

f = Fou(test, trial, stuff=val) # instanciate a BIO (type Fou)
F = f.create() # instanciate a Operator

# other data
test =  [4, 5, 6, 7]
trial = [1, 2, 3]
k = 1+1j

# same with other derived class
h = Helm(test, trial, wave=k)
H = h.create()

# just display to validate that Python rocks! :-)
print(F)
print(H)
