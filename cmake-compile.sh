#!/bin/sh

cd $HOME

wget http://www.cmake.org/files/v3.2/cmake-3.2.3.tar.gz
tar -xzvf cmake-3.2.3.tar.gz > untar.cmake
cd cmake-3.2.3/

./bootstrap && make -j 4

bin/cmake --version

pwd
cd $HOME
ls -rtl
