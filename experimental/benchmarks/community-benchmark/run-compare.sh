#!/bin/bash -xv

export CATEGORY="octane"
export BASE=master
export TARGET=v4.x

export RUNS=1
export FILTER=''
export MACHINE_THREADS=''

bash run.js
