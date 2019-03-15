#!/bin/bash

node --max_old_space_size=4096 require/require.perf.js | tee report.temp
