#!/usr/bin/env python
# coding: utf8


class Operator:
    # constructor
    def __init__(self, shape=(0, 0), f=lambda i, j: 0+0j):
        self.shape = shape
        self.func = f

    # call a function
        ## note that if the function 'foo ' is attached to an Object
        ## all the attributes are used by this function 'foo' 
        ## and so by this method. Yeah Python rocks ! :-)
    def evalAt(self, i, j):
        return self.func(i, j)

    # just to be able to see something (method called by print())
    def __str__(self):
        s = "shape={} \nvals: ".format(self.shape)
        for ii in range(self.shape[0]):
            for jj in range(self.shape[1]):
                s = s+" {} ".format(self.evalAt(ii, jj))
        return s
