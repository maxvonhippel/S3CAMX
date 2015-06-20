#!/usr/bin/env bash
set -o verbose

soname=fuzzy_controller.so
SOURCE=fuzzy_controller.c

# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
