#!/bin/bash

cd gem5
if  test -z "$1"
then
  scons build/X86/gem5.opt -j4
else
  scons build/X86/gem5.opt -j$1
fi
