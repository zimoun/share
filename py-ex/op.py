#!/usr/bin/env python
# coding: utf8


class Operator:
    def __init__(self, shape=(0, 0), f=lambda i, j: 0+0j):
        self.shape = shape
        self.func = f

    def evalAt(self, i, j):
        return self.func(i, j)

    def __str__(self):
        s = "shape={} \nvals: ".format(self.shape)
        for ii in range(self.shape[0]):
            for jj in range(self.shape[1]):
                s = s+" {} ".format(self.evalAt(ii, jj))
        return s


if __name__ == "__main__":
    o = Operator()
    print(o)

    p = Operator((3,3))
    print(p)
