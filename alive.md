
Geometry
========

~~~cpp
string type
      "circle", "ellipse", "arc", "segment"
      "mesh"
~~~

**No union for the Geometry !!**

Trace
=====

~~~cpp
Geometry * m_g
string m_discrete
       "Fourier", "Tcheby", "P1"
int m_ndof
vector<Trace *> m_traces
string m_type
       "Elementary", "Block"
static int idmax
int m_id

void add(Trace)
void Print(local verbosity)

void setGeom, getGeom, ...
~~~

Operator
========

~~~cpp
int m_id
Bier *bier

void setTrace(Trace *, Trace *)
Operator::Operator(Trace *, Trace *)
{
        //createBier => id
        m_id = id
        bier->setTrace(t1, t2)
}
void Print()

~~~

Bier
====

~~~cpp
int m_id
Trace *trial, *test
Shape m_shape
string m_type
       "SingleLayer", "DoubleLayer", "HyperLayer", "AdjointLayer"
       "Identity", "Null"
Node *m_node

void Print()

class Node
{
        string m_type
               "Elementary", "Binary", "Unary", "Block"
        string m_operations
               unary: "+" "*" (scalar) "-"
               binary: "+" , "block"
        vector<int> m_ids
        vector<Shape> m_index
        vector<truc> m_indices

// Shape = (int, int)
Truc{ int id; Index ij; // [-1, -1] }

#define Index = Shape
// only one Shape or Index and ad-hoc defintion
~~~

New id at each affectation and/or copy


Barman
======

~~~cpp

vector<int> m_ids
vector<int> m_update
vector<Bier*> cave

// + map to quick search

void Purge() // assemble

~~~
