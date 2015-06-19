#!/usr/bin/env python
# coding: utf8

import op

class BIO:
    def __init__(self, test, trial):
        self.test = test 
        self.trial = trial

    def getValue(self):
        pass
        
    def create(self):                
        return op.Operator(shape=(len(self.test), len(self.trial)), f=self.getValue)


class Fou(BIO):
    def __init__(self, test, trial, stuff=1):
        super(self.__class__, self).__init__(test, trial)
        self.stuff = stuff
          
    def getValue(self, i, j):
        return self.stuff 

class Helm(BIO):
    def __init__(self, test, trial, wave=1):
        super(self.__class__, self).__init__(test, trial)
        self.wave = wave

    def getValue(self, i, j):
        return self.wave * self.test[i] * self.trial[j]

if __name__ == "__main__":
    t = [1, 2]
    tt = [3, 4, 5]
    b = BIO(t, tt)

    f = Fou(t, tt)
