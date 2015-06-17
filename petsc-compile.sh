#!/bin/sh

cd $HOME

wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.6.0.tar.gz
tar -xzf petsc-3.6.0.tar.gz
cd petsc-3.6.0/

export PETSC_DIR=$PWD
export PETSC_ARCH=linux_complex

./configure \
--with-scalar-type=complex \
--with-clanguage=cxx \
--with-shared-libraries=1 \
--with-x=0 \
--download-fblaslapack=1 \
--download-mpich=1 \
--with-debugging=0


make PETSC_DIR=$HOME/petsc-3.6.0 PETSC_ARCH=linux_complex all
make PETSC_DIR=$HOME/petsc-3.6.0 PETSC_ARCH=linux_complex test
make PETSC_DIR=$HOME/petsc-3.6.0 PETSC_ARCH=linux_complex streams NPMAX=4

pwd
cd $HOME
ls -l