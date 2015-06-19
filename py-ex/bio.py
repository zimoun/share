#!/usr/bin/env python
# coding: utf8


# do not forget the namespace :-)
import op


class BIO:
    # constructor
    def __init__(self, test, trial):
        self.test = test 
        self.trial = trial

    # kind of virtual method
    def getValue(self):
        pass
    
    # create an Operator
    def create(self):                
        return op.Operator(shape=(len(self.test), len(self.trial)), f=self.getValue)


# A derivate class
class Fou(BIO):
    # overload of the constructor
    def __init__(self, test, trial, stuff=1):
        # because the function 'super' is a bit different between Py2 and Py3
        # and I do not know which one you use
        # ==> try statement !! (yeah nice pythonic feature :-)
        try:
        # run before the constructor of the Mother class
            super().__init__(test, trial)
        except:
            BIO.__init__(self, test, trial)
        self.stuff = stuff
    
    # the function that compute
    def getValue(self, i, j):
        return self.stuff 

# Another derivate class
class Helm(BIO):
    # another overload, note that wave could be everything
    def __init__(self, test, trial, wave=1):
        try:
            # this Py3 is just shorter :-)
            super().__init__(test, trial)
            # this is more explicit and works with Py2 except when inheritance
            #  super(self.__class__, self).__init__(test, trial)
        except:
            BIO.__init__(self, test, trial)

        self.wave = wave

    # another function that computes complicated things
    def getValue(self, i, j):
        return self.wave * self.test[i] * self.trial[j]

