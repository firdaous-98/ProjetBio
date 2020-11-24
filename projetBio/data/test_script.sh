#!/bin/bash

for i in *.gz
do
    gunzip $i
done
for i in *.zip
do
    unzip $i
done
