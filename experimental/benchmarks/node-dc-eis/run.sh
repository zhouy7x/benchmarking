#!/bin/bash

# run bench
bash run-dc-eis.sh

# clean data and post to server
python postdata.py

