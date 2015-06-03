


# First summarize

### voc

+ BIE = Boundary Integral Equation
+ BIO = Boundary Integral Operator

## Main goals

+ Using different basis (Fourier, Tcheby, BEM, etc.)
+ Possibility to specifying manually the kernel


Computational problems:

+ Light as possible (kiss)               
+ Make it easy to be maintained!!        
+ Front-end: python                      
+ Back-end : C or C++ (to be discussed). 

[ 
By C++, say only some class, no multiple heritage (complicated).
Only few objects/encapulsations.
]

## To be discussed

+ Parallelism (PETSc ?) ?                        
+ Possibility to plug library: FMM, H-matrix, ...

## Simon's stuff

Possibility to compute the identity between different basis functions (eg: Fourier/Tchebitchev)


## PostProcessing
### Accepted Output format

ASCII, GMSH (.pos), VTK/Paraview (.vtk or .vtu) (hard-coded, no external lib for now)

### Post operation

+ Near field
+ Far field
+ Trace/Normal derivative trace

## License

GPL or BSD

## Name

+ bemused
+ bemusement
+ etc.


# Notes

PDF output :

    pandoc first-try_by-Berty.md --latex-engine=pdflatex -o out.pdf

or with the section numbered

    pandoc -N first-try_by-Berty.md --latex-engine=pdflatex -o out.pdf
