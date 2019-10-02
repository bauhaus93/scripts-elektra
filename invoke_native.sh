#!/bin/sh

mkdir -p $PWD/output
rm -f $PWD/output/build.sh

../scripts/script_gen/script_gen.py $@

[[ -f $PWD/output/build.sh ]] && chmod +x $PWD/output/build.sh && sh $PWD/output/build.sh

