
Because at some point, we would like to note e.g. the matvec by `A*x`,
then, `C++` (and the simple operator overloading) seems better than
pure `C`.

Kind of Problem
===============

Let N items, such as disks.
Therefore, N+1 domains are considered: 

 + N interior domains
 +  one exterior domain

Note that the N interior domains should be *empty*.

In other words, in any case, let N *interfaces*.
And then we would like to solve a BIE 
(BIE means an weak formulation based on BIO).

Objects (core)
=======

The **core** objects are:

 + `Interface` (don't know if Space is not better)
 + `DofHandler` (could be directly included in `Interface`)
 + `TaskHandler`
 + `BMatrix` [**TODO**: find a nicer name, `Operator` ?]
 + `Matrix`
 + `Vector`

and if you dive a bit, then it is close to `bem++`.


`Interface` / `DofHandler`
-------------------------

An *interface* represents the geometrical interface, 
so it contains sort of parametrization etc.
[**TODO**: think how to ? keep in mind mesh?]

For what we are interested in now, `Interface` owns  the *test* and
*trial* functions types, as attributes.

These test and trial functions imply a `DofHandler`
i.e., a numbering of the unknowns.
Roughly speaking, it is a list (bijection) between the *modes*
(test/trial function) and the unknowns (more or less vector indexes)

    [-M,..., -1, 0, 1,..., M] <-> [0, 1,..., 2M+1]
            
more maybe some metadata. 
The key point of the `DofHandler` is to manage the so prone error indexing.


`TaskHandler`
------------

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


`Matrix` and `Vector`
------------------

`Mat` needs to be encapsulated into a class, in order to
overload some basic arithmetic operation as `A*x`

`Vector` is only `Vec` plus maybe some metadata
i.e. the PETSc's vectors encapsulated into a class.

Basically, these objects are the matrix and the vector of PETSc, to
keep all the power and in-place tools, without reinventing the wheel.


`BMatrix`
--------

This object is the core of the kernel, the heart of the performances,
my graal.

It should only and simply be a layer on the top of the blocked
matrices of PETSc,
i.e., a nice handler and common interaction of blocked matrices.

The basic use should be

    bA = BMatrix(params);
    A = pA.assemb();

with `bA` is a pointer and `A` is of the type `Matrix` 

`BMatrix` has some methods such that `addBlock`
And the method `assemb` lunches the building.

`Bmatrix` has attributes such as the global `size` (updated at each
`addBlock`), the sizes of each block etc.

**TODO** think to a recursive mechanism to add a block composed itself
  of sub-blocks.

To be clear about the mechanism behind, it is described below with the
example.


Objects/functions (operators)
=================

The Fourier single layer would be built in this way,

    bV = singleLayer_Fourier(Interface test, Interface trial, params);
    V = V.assemb();


Example of Use (will provide as example)
==============

Kind of EFIE with 2 circles (C1 and C2)
---------------------------

  1. Full way
    
         int main(int argc, char *argv[])
         {

         Interface geom; // contains C1 and C2
         BMatrix bV;
         Matrix V;
         Vector e;

         b = rhs...  // to clarify

         bV = singleLayer_Fourier(geom, geom, params);
         V = bV.assemb();

         x = gmres(V, b, params);
         // or x = direct(V, b); i.e. x = V\b; if the overload is possible

         // post-processing
         // to clarify too
         }


  2. per circle

        int main(int argc, char *argv[])
        {

        Interface geom[2]; 

        BMatrix bVV;
        Matrix VV;
        Vector e;

        C1 = geom[0];
        C2 = geom[1];


        bV11 = singleLayer_Fourier(C1, C1, params);
        bV12 = singleLayer_Fourier(C1, C2, params);
        bV21 = singleLayer_Fourier(C2, C1, params);
        bV22 = singleLayer_Fourier(C2, C2, params);

        bVV.addBlock( (0, 0), bv11); 
        bVV.addBlock( (0, 1), bv12); 
        bVV.addBlock( (1, 0), bv21);
        bVV.addBlock( (1, 1), bv22);

        VV = bVV.assemb();

        b = rhs...  // to clarify
        x = gmres(VV, b, params);
        // or x = direct(VV, b); i.e. x = VV\b; if the overload is possible

        // post-processing
        // to clarify too
        }



Explanations about mechanism (of `BMatrix` and not about `singleLayer_`)
-----------------------------

The first example, the PETSc kind of `Mat` behind of `bV` is the one
given by default by `stuff_Fourier`.
i.e., the function fills metadata of `bV` such that `kind`, `size`
etc.
Then `assemb` lunches the PETSc functionality (distribution ect.)

The second example, the PETSc kind of `Mat` behind of `bVij` is the one
given by default by `stuff_Fourier`, but they are never used.
And because, the method `addBlock` is used, the attribute `kind` is
changed from the default one by a block one.
Moreover, the four `addBlock` do nothing, except fill the values for
the PETSc block `Mat`, such that the indexes etc.
Then `assemb` uses the PETSc functionnality of this block `Mat` to
distribute etc.


