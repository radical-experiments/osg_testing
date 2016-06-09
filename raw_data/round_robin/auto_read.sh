#!/usr/bin/env bash

for folder in `ls -d */`; do 
    if [ "${folder:0:1}" = "p" ]; then
        echo ${folder%'/'}
        for file in `ls $folder`; do
            echo $file
            python json_read.py ${folder%'/'}/$file >> ./summary/summary_${folder%'/'}.txt
        done
    fi
done
