salut Dude,

parce que je ne peux pas trop vraiment m'en empêcher, voilà quelques
réflexions que j'ai eu sous la douche :-)

TL;DR: différents points de vue sont possibles: nous devons en choisir
un et se lancer.  Je parle pour moi, et souvent un 'nous' n'implique
que moi, enfin je veux dire que parfois il t'inclue et parfois
non. Donc si tu vois un 'nous' et tu te dis "bah non! je ne pense pas
ça" c'est que c'est un 'nous' qui est un 'je' (simon).
Oulà, c'est compliqué pour dire une chose simple: j'écris 'nous' par
facilité en ayant conscience que parfois c'est uniquement moi.
Bref!

Ensuite, on efface tous les noms que l'on a utilisé avant.
Ici Operator, Matrix, Barman etc. ne représente pas ce dont on a déjà
parlé.

J'essaie de résumer nos idées et ce que nous voulons.

1 / Qu'est-ce que nous voulons/aimerions ?
==========================================

Quand je réfléchis à nos discussions, je me dis que nous voulons
quelque chose qui fait tout, sans vraiment séparer les couches, les
problèmes etc. et du coup nous nous perdons.

Pour moi, il y a 2 couches distinctes:
 -a- manipulations de matrices par blocs
 -b- constructions des opérateurs intégraux


-a- Manipulation de matrices par bloc
-------------------------------------

Je veux un outil qui me permet d'ajouter, récupérer etc. des blocs
dans une matrice sans me soucier des indices.

Sur le papier, j'écris des blocs, ce qui correspondrait
informatiquement à ajouter (setBlock) pour former la matrice finale.

Sur le papier, je récupère un bloc pour e.g. calculer son inverse ce
qui correspondrait à récupérer (getBlock).

Toujours sur le papier, je fais des opérations algébriques sur des
matrices par blocs et donc je voudrais faire la même chose. Opérations
algébriques signifiant les opérations arithmétiques usuelles (+-*) et
aussi d'autres comme /,transpose etc.

Deux idées derrières: mon application MTF qui est massivement par
blocs et tester des méthodes de Krylov par bloc (resilient Kyrlov,
préconditionneur etc.).

J'ai un script python qui fait ce job. C'est une classe toute simple
bac à sable.

Quel est le problème ?

J'en vois 2, et ils concernent les opérations algébriques:
 - vouloir faire cela dans contexte parallèle
 - qu'est-ce qui défini un bloc élémentaire ?

Pour le contexte parallèle, on se décharge sur un outil qui fait le boulot e.g. PETSc.
Note: petsc est l'outil qui semble adapté mais d'autres seraient envisageables, e.g.,
http://docs.enthought.com/distarray/

Un bloc élémentaire est un tableau de coefficients (matrice), ce qui
dans ce cas, ne pose pas trop de difficultés. Cependant, nous avons en
tête de définir un bloc élémentaire par son produit matrice-vecteur,
et dans ce cas, informatiquement, les choses ne sont plus si simples:
comment définir l'addition de fonctions ? ou la composition
(multiplication de matrices) ?


-b- Constructions des opérateurs intégraux (ou autres)
------------------------------------------

C'est une manière d'obtenir des blocs élémentaires.

Quel est le problème ?

J'en vois 2:
 - gestion des frontières non-connexes
 - comment aussi faire de simples opérations (arithmétique (+-*)

Il faut cependant raffiner les choses, parce qu'il y a une question
sur qui et comment sont gérées les matrices d'interaction entre
frontières non-connexes.

Et de même comment gérer des opérations arithmétiques sur des
"fonctions"


2/ Propositions -- très grossières
==================================

Nous pensons à des formulations faibles, où il ya des fonctions trials
et des fonctions tests.

A) Gestion des inconnues (Inconnues / Dof / Trace / TT)
------------------------

Les inconnues sont relatives à un domaine. Et un domaine signifie des
propriétés physiques (nombre d'onde, conductivité etc.).

Dans le contexte équations intégrales, les inconnues sont aussi
attachées à un domaine puisque nous parlons de trace extérieure ou de
trace intérieure.

Les inconnues sont liées aux fonctions trials. Et dans un contexte
formulation faible, il y aussi des fonctions tests.

Note: le nombre de fonctions tests et trials peut être différent.

Un domaine (frontière) signifie aussi géométrie (donc un objet
Géométrie).

La question est:
 -- est-ce la définition d'un seul objet Inconnue par frontière connexe ?
 -- ou est-ce un objet Inconnue par géométrie (connexe ou non) ?

La réponse à cette question implique différentes manières de gérer les
interactions.

Prenons l'exemple de 2 cercles 1 et 2, et construisons un opérateur,
disons le simple couche du problème extérieur.

+ choix-i: objet Inconnue cercle 1 et objet Inconnue cercle 2
ceci signifie des mécanismes de super-inconnues pour les regrouper par bloc

+ choix-ii: objet Géométrie cercles = cercle 1 et cercle 2, puis objet Inconnu cercles

/me: je suis pour le choix-i. Car ceci simplifie l'implémentation et
au final c'est ce que nous faisons sur le papier.


B) Gestion des formes faibles [opérateurs] (WeakForm / biLinForm)
------------------------------------------

Cet objet construit un tableau (matrice) correspondant à l'application
des fonctions tests et trial sur un opérateur.  Cela pourrait même
n'être que simple fonction prenant en entrée un objet Inconnue et
renvoyant un tableau de double (ou complexe)

Les différents opérateurs intégraux (Fourier, Tcheby, Laplace,
Helmholtz etc.) dérivent de celui-ci.


C) Gestion des blocs des formes faibles (LinSys / Operator)
---------------------------------------

Cet objet permet de regrouper et gérer les différentes formes faibles
par blocs.

choix-1:
 + fournir la liste des Inconnues
 + assembler les formes faibles par patron (template)

choix-2:
 + créer la forme faible
 + les assembler.

Concernant le choix 1, il y a 2 façon de gérer:
 choix-a: créer un objet élementaire (Bier)
 choix-b: utiliser le même objet.

Quel est le problème ?

Nous souhaitons faire des blocs de blocs et donc appliquer une
récursivité. Et donc, sur quel objet le fait-on ?

Pour être précis,  à une matrice/Matrix (niveau discret) correspond un
LinSys/Operator (niveau continu), ce qui implique:

 + dans le choix-1+a, un objet élémentaire ne peut pas donner une
matrice, et il faut construire un LinSys/Operator

 + dans le choix-1+b et le choix-2, tout objet élémentaire est en
quelque sorte un LinSys/Operator, comme sur le papier

Et il y a un Barman/TaskHandler qui gère ces objets élémentaires, qui
sait qui est construit pour quelle Inconnue.


Pour moi, nous étions parti sur le choix-2 (qui implique le choix-b).
Ce n'est peut-être pas la bonne solution, en terme de difficultés
d'implémentation et il faut peut-être distinguer les choses.
Cependant, c'est 2 visions du même problème, il faut juste en choisir
une. Peut-être qu'en terme d'implémentation, l'une est meilleur que
l'autre. A réfléchir ?


D) Gestion des matrices par blocs (Matrix)
---------------------------------

Ceci est une surcouche à PETSc, avec des metadata qui nous permet
d'extraire les blocs sans avoir recourt aux index.


E) Illustrations
----------------

Imaginons que l'on souhaite construire la "matrice/opérateur"
(assez proche d'un MTF 2 domaines, en remplaçant V par du Caldéron)

~~python
A = 2*[
        [ Vaa, Vab,  5*X,  0 ]  [ua]
        [ Vba, Vbb,    0,  0 ]  [ub]
        [   0,   0,   V1,  0 ]  [u1]
        [   0,   Y,    0, V2 ]  [u2]
      ]


# choix 2:

##Inconnue contient uniquement Trial ou Test


                             trial       test
Operator Vaa = SingleLayer(Inconnue_a, Inconnue_a)
Operator Vab = SingleLayer(Inconnue_a, Inconnue_b)
Operator Vba = SingleLayer(Inconnue_b, Inconnue_a)
Operator Vbb = SingleLayer(Inconnue_b, Inconnue_b)

Operator V0;
V0.setBlock(0, 0, Vaa)
V0.setBlock(0, 1, Vab)
V0.setBlock(1, 0, Vba)
V0.setBlock(1, 1, Vbb)

Operator X = Identity(Inconnue_1, Inconnue_a)
Operator V1 = SingleLayer(Inconnue_1, Inconnue_1)

Operator Y = Identity(Inconnue_b, Inconnue_2)
Operator V2 = SingleLayer(Inconnue_2, Inconnue_2)

Operator C;

C.setBlock(0, 0, V0)
C.setBlock(1, 1, V1)
C.setBlock(2, 2, V2)

C.setBlock(0, 1, 5*X)
C.setBlock(2, 0, Y)
// il faudra probablement ajouter 2 Null
// pour avoir des tailles qui matchent.

Matrix A = (C+C).assemble()


# choix 1-a:

##Inconnue contient Trial+Test

Bier V;
V.kind(SingleLayer)

Bier Id;
Id.kind(Identity)


        trial+test
Inconnue Inconnue_0;
Inconnue_0.union(Inconnue_a, Inconnue_b)

LinSys D;

D.structList(Inconnue_0, Inconnue_1, Inconnue_2)

D.setBlock(0, 0, V)
D.setBlock(1, 1, V)
D.setBlock(2, 2, V)

D.setBlock(0, 1, Id) // missing 5* ??
D.setBlock(2, 1, Id)

Matrix A = (D+D).assemble()
~~

Pour résumer:
=============

choix-1+a:

 + où met-on l'arithmétique ?
dans l'exemple, il faudrait en mettre une dans LinSys et une dans
Bier.
Ou alors Bier devient un LinSys, et cela correspond au choix-1+b.

 + Chouette système de patron qui simplifie l'écriture redondante.


choix 2:

 + c'est plus ou moins comment fonctionne BEM++
 + cela est contenu par le choix-1


=========================
Ma conclusion provisoire
=========================

Il nous faut:

 - un objet "fonction" par frontière connexe (qui peut-être ouverte)
contient des propriétés physiques du domaine
cet objet représente les fonctions tests *ou* les fonctions trials

 - un objet "produit de dualité" par frontière connexe
contient 2 objets "fonction"s si ces objets ont: la même frontière
connexe et donc les mêmes propriétés physiques.

On doit pouvoir faire des unions de "produit de dualité" pour pouvoir
traiter des frontières non-connexes.

 - un objet "opérateur" qui possède une arithmétique et qui gère des
   blocs, c'est-à-dire qui est récursif.
Les opérateurs intégraux en dérivent, c'est la terminaison de la
   récursivité.

 - un objet "système linéaire" qui gère de façon transparente les
   "opérateur"s en connaissant: les "produit de dualité" et la struture


to finish...
