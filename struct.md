Summary: TL;DR
=============

Kind of problem
---------------

Let N items, such as disks.
Therefore, N+1 domains are considered:

 + N interior domains
 +  one exterior domain

Note that the N interior domains should be *empty*.

In other words, in any case, let N *interfaces*.
To each interface, some BIO are considered, 
and then we would like to solve a BIE.

+ BIE: Boundary Integral Equation
+ BIO: Boudnary Integral Operator

**BIE means an weak formulation based on BIO(s).**



Note about the mechanism behind
-------------------------------

Roughly speaking:

 - BIO is an `Operator`
 - BIE is also an `Operator` which is then transformed into a `Matrix`

An `Operator` manages only *metadata* which is (more or less) pointers,
i.e about the *structure*.
By structure, we have to understand the size and the MPI rank,
but also the block structure if it is.

Basically an `Operator` is represented by a [COO][coo] matrix format:

~~~
A[row, col] = (row, col, *pointer)
~~~

i.e. an `Operator` is nothing more than a list of 3 items.

By construction, the constructor of the operator fills `(0, 0, *p)`
where the pointer `p` points to itself ;
then the method `addBlock` populates this list.

Once the population is satisfied, the method `assemb` launches the
distribution and the assembly part then return a `Matrix`.


[coo]: http://en.wikipedia.org/wiki/Sparse_matrix#Coordinate_list_.28COO.29

Structure
=========

More or less the oganization, and the details are given below.

~~~
								+----++---+
								|Tche||Fou|
								|    ||   |
							   	|    ||   |
							   	+----++---+
  +----------------------------++---------++--+
  |FourierAnalytical           ||Spectral ||o |
  |                            ||         ||t |
  |  + singleLayerHelm_Fourier ||         ||h |
  |  + doubleLayerHelm_Fourier ||         ||e |
  |  + adjointLayerHelm_Fourier||         ||r |
  |  + hyperLayerHelm_Fourier  ||         ||  |
  |	 + projectFunction_Fourier ||  	   	  ||  |
  +----------------------------++---------++--+
  +-------------------------------------------+
  |Core                                       |
  |					  	   	   	   	   	   	  | +----------------+
  |	- LinAlg   	   	   	   - Geom  	   	   	  |	|Log             |
  |                     |                     |	|                |
  |    + Operator       |     + Interface     |	|  nice print    |
  |    + Matrix	        |     + TaskHandler   |	|  info (level)  |
  |    + Vector         |      	   	   	      |	|                |
  |                                           |	|                |
  +-------------------------------------------+	+----------------+
~~~


Note
----

A `ClassThatRocks` starts by upper letter.
A `functionThatRocks` starts by lower letter.
A list of items finished by `s` as `beers`.

Thefore, maybe it could be nice to encapsulated all the PETSc tools
that we need inside a `class` (and maybe a `namespace`)
The advantages are: 1/ when the PETSc API changes, our update is
easier, 2/ it is easy to change the matrix representation if we want
to, i.e. only changing the `namespace` (useful for collaboration as
Xavier) and 3/ this avoid to include all the *weird* PETSc types.


`Log`
=====

A class mimicking the `Message` class of `GetDP`.


`Interface` (other name?)
==========

An *interface* represents the geometrical interface,
so it contains sort of parametrization etc.
[**TODO**: think how to ? keep in mind mesh?]

For what we are interested in now, `Interface` is not so much relevant.

Note that `Interface` needs to have a numbering of the unknowns,
i.e a list (bijection) between the *modes*.
Even if it seems not useful, the key point of this `dofHandler` is to
manage the so prone error indexing.

Moreover, this allows to have access the local numbering of a
interface, which seems useful for debugging purposes (or for guru hacks).

 + **attributes**
	- `kind` : `char` not useful for now
   	- `size`: `int`
   	- `dofs` : `int[2M+1][2]` and by default (constructor),

~~~
   [-M,..., -1, 0, 1,..., M] <---> [0, 1,..., 2M+1]
~~~


 + **methods**
	- constructor and destructor
	- `setDofHandler` : `int[2M+1] |-> int[2M+1][2]`
	it could be overloaded by the user.
	- `getDofHandler`
	
`TaskHandler`
============

It is an independant part and it could contain a dictionnary
between the interface index and the processus (`MPI rank`).

The default mapping could be: one interface per processus.
However, if one iterface is really larger than the other ones, the
user has the ability to map as he/she wants to distribute the load.

Moreover, this object could contain an update to *who* is *where*.

What I have in mind is: let assembly a mudiff matrix per block (one
block per processus) and then let assembly the block diagonal
preconditioner, the rebuilding is avoided.
[**NOTE** don't know if it is useful, maybe this could be included in
the `Matrix`]

**Not enough MPI knowledge, need to discuss.**


 + **attributes**
   - `loads` : `int[N+1][2]`
   
 + **methods**
	- constructor and destructor
	- `setAssignInt2Proc`
	- `getProc` gives the `Interface`(s) associated to a MPI rank
	- `getInterface` gives the MPI rank(s) associated to  a `Interface`


`Matrix`
============

`Mat` needs to be encapsulated into a class, in order to
overload some basic arithmetic operation as `A*x`

Basically, these objects are the matrix and the vector of PETSc, to
keep all the power and in-place tools, without reinventing the wheel.


 + **attributes**
	- `shape` : `int[2]`
	- `kind` : char
	
 + **methods**
	- constructor and destructor
	- `matvec`
	- `matmat`
	- etc.

`Vector`
============

`Vector` is only `Vec` plus maybe some metadata
i.e. the PETSc's vectors encapsulated into a class.


 + **attributes**
 	- `shape` : `int`
	- `kind` : char

 + **methods**
	- constructor and destructor
	- operations with vector

`Operator`
============

It should only and simply be a layer on the top of the matrices of PETSc,
i.e., a nice handler and common interaction of matrices, but to be
clear `Operator` acts only on the `pointer` level.

`Operator` is only something that collect and distribute.

Moreover, it is the same object that manages all the matrices.
Therefore, it is a *big* object.

In other word, until the method `addBlock` is called, the behaviour is
the *classical* behaviour, i.e. the one of we have naturally in mind.
To be clear, it is one block.

Then, if the method `addBlock` is called, there is two options, switch to

 1. block matrix format of PETSc (nested or monolitic etc.)
 2. a classical matrix format

The first option seems clear
and it allows to use mixed kind of blocks.

However, the global matrix could be turn into one of the classical
formats and then assembly in this format.

In other words, or maybe more precisely, it would be nice to
initialize all the *actions* (by pointers?), then when the `assemb`
method is called, all the memory and computations are launched;
i.e.,

 1. performs from `rank0` the organization
 2. launches, which means (more or less)
	   + `MatCreate`
	   + `MatSetValue`
	  and different ways are possible,
	     * a `MatCreate` per *block* and then the PETSc block
	feature
	     * only one `MatCreate` and `MatSetValue` calls a different
	function per *block*

What is not clear for me is :

 - if a BIE is composed by only one BIO
 then we would like to compute it using all the processes available
 - if a BIE is composed by several BIOs
 then we would like to compute them using all the processes available

**That's why from my point of view, we need a `TaskHandler` to
  distribute in a nice and easy way the load.**

 + **attributes**
	- `shape` : `int[2]` size of the returned `Matrix`
	- `coo` : `tCoo[]`
	and create a `struct` s.t. (row, col, val).
	with a nice list *appending*.
	Or
		+ `cols` : list of integer 
		+ `rows` : list of integer 
		+ `vals` : list of `Operator` pointer

	- `Shape` : `int[2]` size block structure
	
 + **methods**
	- constructor and destructor
	- `setValue` : function that feeds the '`PetscScalar values[]`'
	field inside the function `MatSetValue`. 
	- `addBlock`
	- `assemb`
	- `update` : update the values of `shape` and `Shape`
	- `diagonal` : get the diagonal blocks

FourierAnalytical
=================

This is only functions.

~~~cpp
Operator singleLayerHelm_Fourier(Interface test, Interface trial, wavenumber)
Operator doubleLayerHelm_Fourier(Interface test, Interface trial, wavenumber)
Operator adjointLayerHelm_Fourier(Interface test, Interface trial, wavenumber)
Operator hyperLayerHelm_Fourier(Interface test, Interface trial, wavenumber)
~~~


Why `(test, trial)` and not `(trial, test)` ?
---------------------------------------------

because

$$
A_{ij} = <\phi_i , A\psi_j>
	   = \int\int A\psi_j \bar{\phi_i}
$$
with $\phi$ is a test-function and $\psi$ is a trial-function.

In other words, the test-functions correspond to the row
and the trial-function correspond to the column.


Still remains ?
---------------

A question remains: what does `projectFunction_Fourier` return ?
especially in the context of block matrix.

Maybe, the best solution should be to add a `Fucntion` class, which
represents a vector, as `Operator` represents a matrix.


|pointer    |`Operator`  |`Function`|
|:---------:|:----------:|----------:|
|allocated  |`Matrix`    |`Vector`  |


In this way, the prototype is

~~~cpp
Function projectFunction_Fourier(Interface test, Complex func);

// with func such that
Complex func(tPoint p);

//with tPoint a new type, e.g,
typedef struct{
 float x;
 float y;
} tPoint;
// or a class Point
~~~


Example
=======

**to be written**





* * *

