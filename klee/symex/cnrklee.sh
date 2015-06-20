#!/bin/bash

# Usage: ./cnrklee.sh <controller path> <include path>

set -v  
set -e

CONTROLLER_MAIN=./controller_main_symbolic
KLEE_INCLUDE=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/include/
FINAL_OBJECT=./C
KLEE_WRAP=./kleewrap.py

CONTROLLER_PATH=$1
CONTROLLER_INCLUDE=$2

###########################################
# DO NOT USE -g when compiling for KLEE: adds more paths?
###########################################

# compile controller_main_symbolic.c
llvm-gcc -I $KLEE_INCLUDE -I $CONTROLLER_INCLUDE --emit-llvm -c -g $CONTROLLER_MAIN.c -o $CONTROLLER_MAIN.o

# compile given controller
llvm-gcc -emit-llvm -c -g -D KLEE_ASSUMES $CONTROLLER_PATH -I $KLEE_INCLUDE -I $CONTROLLER_INCLUDE -o controller.o

# link all
llvm-ld --disable-opt ./controller.o $CONTROLLER_MAIN.o -o $FINAL_OBJECT.o

# run klee
# klee -optimize -only-output-states-covering-new -solver-optimize-divides=0 -smtlib-human-readable --write-pcs --write-smt2s --use-query-log=all:pc $FINAL_OBJECT.o.bc
# klee -only-output-states-covering-new -solver-optimize-divides=0 -smtlib-human-readable --write-pcs --write-smt2s --use-query-log=all:pc $FINAL_OBJECT.o.bc

klee -solver-optimize-divides=0 -smtlib-human-readable --write-pcs --write-smt2s --use-query-log=all:pc $FINAL_OBJECT.o.bc

#klee -stop-after-n-tests=2 -solver-optimize-divides=0 -smtlib-human-readable --write-pcs --write-smt2s --use-query-log=all:pc $FINAL_OBJECT.o.bc
# klee -exit-on-error -smtlib-human-readable --write-pcs --write-smt2s --use-query-log=all:pc C.o.bc

# read klee outputs and display
# $KLEE_WRAP ./klee-last/*.ktest --int-arr

# go to test_results
cd ./klee-last/
# prep smt2 files for z3
../remove_decls_smt2.sh
cd ..

# rename error smt to smt2.error
cd ./klee-last/
../rename_error_smt.sh
cd ..

# delete all previosuly existing path files
rm -f $CONTROLLER_INCLUDE/paths/*.smt2

# copy all smt2 paths generated by klee
for f in ./klee-last/*.smt2
do
  cp $f  $CONTROLLER_INCLUDE/paths/
done

echo 'Successfull....'