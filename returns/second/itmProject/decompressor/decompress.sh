if [ ! -f decompressor/d.py ]; then
	gunzip decompressor/d.py.gz
fi
python decompressor/d.py $1 $2

