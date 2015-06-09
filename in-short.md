
Kind of skeleton
================

Because `Python` rocks !
a quick illustration.

**Hope that the syntax is clear enough to underline the structure**


For sure, it is not optimized and a lot of checks need to be added.
Let just focus of the main: **the ideas** !

Let say that `Numpy` plays the role of PETSc, i.e. it used to
represent the Linear Algebraic operations.

Quick &amp; Dirty `Operator`
---------------------------

~~~python
class Operator:

    # kind of constrcutor
    def __init__(self, shape=(0, 0), coef=lambda i,j: 0.,
                 Shape = (0, 0)):
        
        # Local
        self.shape = shape
        self.coef = coef

        # Block
        self.Shape = Shape
        self.coo = []

        # Private
        self._bandRow = []
        self._bandCol = []


    def addBlock(self, pos, Op):
        self.coo.append((pos, Op))
        # Then the Update the Shape
        n, m = pos
        N, M = self.Shape[0], self.Shape[1]
        upd, ate = N, M
        if n > N:
            upd = n
        if m > M:
            ate = m
        self.Shape = (upd, ate)

    # Update... and maybe checks !
    def _update(self):
        if self.coo == []:
            return None
        self.coo.sort()
        for ii, elem in enumerate(self.coo):
            (n, m), Op = elem
            if n==m:
                row, col = Op.shape
                self._bandRow.append(row)
                self._bandCol.append(col)
        self.shape = (sum(self._bandRow), sum(self._bandCol))
        return None


    def _indexTot2Block(self, i, j):
        Row, ij = [0], 0
        for up in self._bandRow:
            cur = Row[ij]
            Row.append(cur+up)
            ij += 1
        Col, ij = [0], 0
        for up in self._bandCol:
            cur = Col[ij]
            Col.append(cur+up)
            ij += 1

        ii, jj = -1, -1
        for r in Row:
            if i < r:
                break
            ii += 1
        for c in Col:
            if j < c:
                break
            jj += 1
            
        # I,J are the indexes inside a block (local index)
        I, J = i - sum(Row[:ii]) , j - sum(Col[:jj])
        return I, J, ii, jj


    def _coefOfblock(self, i, j):
        if self.coo == []:
            return self.coef(i, j)

        I, J , ii, jj = self._indexTot2Block(i, j)

        coef = self.coef
        for pos, Op in self.coo:
            if (ii, jj) == pos:
                coef = Op.coef
                break
        return coef(I, J)

    # Really not Optimized
    # but the basic that we talked, I guess (or hope so! :-)
    def assemb(self):
        self._update()
        ROW, COL = self.shape
        Mat = np.empty((ROW, COL))
        for i in range(ROW):                
            for j in range(COL):
                Mat[i, j] = self._coefOfblock(i, j)
        return Mat
~~~



Let mimick a kind of BIO
------------------------

~~~python
def computeA(i, j):
    return (i+1)*(j+1)

def createA(n, m):
    Op = Operator((n, m))
    Op.coef = computeA
    return Op
~~~

**The library part is done.**


Example / User side
===================

~~~python
# User Script

A = createA(5, 5)

# Python hack to be synthetic
b = Operator((3, 3),  lambda i, j: 2.)
c = Operator((2, 2),  lambda i, j: 3.)
d = Operator((5, 2),  lambda i, j: 5.)


# Build the BIE
Z = Operator()
Z.addBlock((2, 2), c)
Z.addBlock((1, 1), b)
Z.addBlock((0, 0), A)
Z.addBlock((0, 2), d)

# Well done !!
S = Z.assemb()
## S is a matrix 
~~~
