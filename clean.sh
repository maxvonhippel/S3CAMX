#!/bin/bash

echo 'deleting pyc and klee outputs'
echo 'delete? press ctrl-c to cancel'
ls *.pyc
read
rm *.pyc
echo 'delete? press ctrl-c to cancel'
ls klee-out-*
read
rm -rf klee-out-*
rm klee-last
#rm *.o
echo 'removing tstc files too...'
# remove compiled tst files with extension: tstc
find ./|grep --color=never '\.tstc$'|xargs rm