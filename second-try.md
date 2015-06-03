

After the sandwich of Berty and simon still drinking coffee,
here the short summarize of what we talked about.

Matrix representation
=====================

We are agree that the **parallel management** of the matrices is difficult.
Therefore, we will use `PETSc`, because

+ it is easy to obtain a "parallel matrix" (`assembly`)
+ nice tools are already there (`linear solver`, fft, complex, etc.)

Objects
=======

Here, *objects* do not mean necessary a `C++` object.

+ BIO = Bounday Integral Operator
+ BIE = Bounday Integral Equation
+ Block
+ BlockManager / MatBlock

Moreover, in a general perspective, we would like having,

+ Parametrization of the Geometry
+ hot-plug Kernel
+ Compression such that ACA and all the H-matrix stuff.

First structure
---------------

							 +---------+   	+-------+
							 |         |   	|       |
							 |         | 	|       |
							 +---------+	+--/----+
								   \---	   /---
			 +----------+	   	  +----\-----+
			 |2         |  	 	  |3         |
			 |  Fourier |		  |  General |
			 |  Circle  |		  |  Canonical
			 +--------+-+		  +---/------+
	   	   	   	   	  \ 		     /
   	   	   	   	  +----\------------/--+
				  |1   MatBlock        |
				  |    BlockManagement |
				  +--------------------+


Let only focus on the boxes (1) and (2).

 + (1) is the core
 + (2) build the operators.

The question is: *are the boxes connected ?*


Kind of snapshot
----------------

Let the matrix such that

    A = [
	  [ V, X ],
	  [ K, 0 ]
	  	]

+ V is dense
+ X is sparse
+ K is a matrix-free

And the user interface should be

    V = FourierSingleLayer(params)
    X = FourierIdentity(params)
    K = myTunedFunction(params)

    A = Matblock()
    A.addBlock( (0, 0), V)
    A.addBlock( (0, 1), X)
    A.addBlock( (1, 0), K)


Details
=======

We need to split the `lib` part to the *user* part
i.e. the multiple diffraction, the MTF etc. are an end-layer,
and will done by the user of the lib.
In the same sense that `GetDP` provides all the tools and the user
writes a weak formulation.

To be concrete, the `lib` is only the tools 
to be able to write a BIE (formulation).
Nothing more, nothing less.

Block
-----

A **block** is (more or less) a BIO

+ a sparse matrix
+ a dense
+ a matrix-free

Note that a block could also be a block, e.g.

	A0 = [
	   [ -K0, V0 ],
	   [ W0, Q0 ]
		 ]
	A1 = [
	   [ -K1, V1 ],
	   [ W1, Q1 ]
		 ]

	D = [
	  [ A0, 0 ],
	  [ 0, A1]
	  	]	

Question : 
are the blocks assembled only in serial or also in parallel ?


Let a BIO 
$$
T = \int_A \int_B \bullet
$$

+ $A= B$ is the *auto* interation
+ $A\neq B$ is the *far* interation

And so, for non-connected closed surface $\Gamma= S \cup C$, 
it is possible to write,

    T = [
   	  [ Tss, Tsc ],
   	  [ Tcs, Tcc ],
	    ]

So the question is, in other words:
the parallel task, 
is it done by the block part 
or only by the block-management part 
or both ?


MatBlock / BlockManager
-----------------------

The goal is to easily plug together the different BIO
i.e., skip all the index mistakes.

The part is **enough generic** to be usable in other context (3D etc.)
but still needs to be thought in a `PETSc` environment.

The main idea of this object is to allow the user to write a BIE
(formulation) as he/she writes on the paper.


First Conclusion
----------------

Roughly speaking,

 + BIO = `Block`
 + BIE = `BlockManager`

therefore, we need two layers on the top of `PETSc`,

 + a layer able to easily switch between the PETSC's `Mat`s
i.e. assembly in parallel a BIO
 + a layer able to easily plug BIOs and to stay in parallel

**What are the troubles ?**
`==>` mix the parallel level


