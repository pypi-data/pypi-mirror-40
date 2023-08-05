#!/bin/sh

ln -fs ../crfsuite.cpp
ln -fs ../export.i

if test "$1" = "--swig"; then
    swig -c++ -python -I../../include -o export_wrap.cpp export.i
fi
