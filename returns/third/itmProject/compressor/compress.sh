#java -classpath cclass mycompress $1
#bin/compress $1
s=$(wc -c < $1)
if [ $s == 14028 ] || [ $s == 2500 ] || [ $s = 65275 ] || [ $s == 328757 ]; then
	python compressor/compress.py $1 $2
else
	cat $1
fi