#!/usr/bin/env bash

rm locations.csv

for file in `ls`; 
do 
    grep Locations $file | cut -c 29- | sed "s/u'//g" | sed "s/)//g" | rev | sed "s/'n//g" | sed 's/\\//g' | rev | sed "s/ //g" | sed "s/:/,/g" | sed 's/nan/nan,nan/g' >> locations.csv
done

sed -i '1d' locations.csv
