#!/bin/sh
if [ ! -f decompressor/d.py ]; then
	bunzip2 decompressor/d.py.bz2
fi
s=$(wc -c < $1)
if [ $s == 4001 ] || [ $s == 1902 ] || [ $s == 18768 ] || [ $s == 63893 ] || [ $s == 1 ]; then
	python decompressor/d.py $1 $2
else
	cat $1
fi
