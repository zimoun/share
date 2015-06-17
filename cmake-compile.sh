#!/bin/sh

cd $HOME

wget http://www.cmake.org/files/v3.2/cmake-3.2.3.tar.gz
tar -xzvf cmake-3.2.3.tar.gz
cd cmake-3.2.3/

./bootstrap && make

cd $HOME
return 0