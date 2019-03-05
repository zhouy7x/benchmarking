#!/bin/bash

# run bench
bash run-dc-ssr.sh

# clean data and post to server
python postdata.py

