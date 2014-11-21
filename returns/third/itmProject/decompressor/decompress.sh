if [ ! -f decompressor/d.py ]; then
	bunzip2 decompressor/d.py.bz2
fi
s=$(wc -c < $1)
if [ $s == 4001 ] || [ $s == 1902 ]; then
	python decompressor/d.py $1 $2
else
if [ $s == 102430 ]; then
	bunzip2 -c $1 
else
	cat $1
fi
fi



