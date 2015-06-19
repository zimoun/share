#!/usr/bin/env python
# coding: utf8

import bio

test = [1, 2, 3]
trial = [4, 5, 6, 7]
val = 2

mybio = bio.Fou(test, trial, stuff=val)
F = mybio.create()

test =  [4, 5, 6, 7]
trial = [1, 2, 3]
k = 1+1j

mybio = bio.Helm(test, trial, wave=k)
H = mybio.create()

print(F)
print(H)
