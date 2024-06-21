#!/bin/bash
module load python
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/lib
python3 run_hphc.py
