#!/bin/sh

DIR="${0%/*.sh}"
$DIR/run_test.sh &&
$DIR/run_valgrind.sh
