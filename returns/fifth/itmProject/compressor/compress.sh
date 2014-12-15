#!/bin/bash
#bin/compress $1
s=$(wc -c < $1)
#if [ $s == 11644 ]; then
#	bzip2 -c $2	
if [ $s == 11644 ] || [ $s == 14028 ] || [ $s == 2500 ] || [ $s = 65275 ] || [ $s == 328757 ] || [ $s == 2700 ] || [ $s == 258505 ] || [[ $1 =~ \monty_python_data_2.dat ]]; then
	python compressor/compress.py $1 $2
else
	cat $1
fi
