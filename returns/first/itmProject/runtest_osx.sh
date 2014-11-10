touch my.stat; rm my.stat; touch my.stat

#make sure you keep only the minimum required files in directory 'decompressor'
size1=0
for f in $(stat -f%z decompressor/*)
do
	size1=$(expr $size1 + $f)
done

for file in data/*
do
    size0=$(stat -f%z $file)
    printf "%s: %d -> " $file $size0

    sfile=$(echo "s$file" | sed 's/\.dat/\.sdat/')
    if test ! -e "$sfile"
    then
	sfile=""
    else
	printf "*"
    fi
    compressor/compress.sh $sfile $file >data/tmp.dat
#    gzip <$file >data/tmp.dat

    printf "%d + " $size1
    size2=$(stat -f%z data/tmp.dat)
    perc2=$(expr 100 '*' $size2 / $size0)
    printf "%d (%d%%) = " $size2 $perc2
    size=$(expr $size1 + $size2)
    perc=$(expr 100 '*' $size / $size0)
    printf "%d (%d%%) " $size $perc

    echo $size >>my.stat

    decompressor/decompress.sh $sfile data/tmp.dat >data/tmp2.dat
#    gunzip <data/tmp.dat >data/tmp2.dat

    diff --brief $file data/tmp2.dat >/dev/null
    ret=$?
    if test $ret != 0
    then
	echo "You screwed up!"
	exit -1
    else
	echo "Ok."
    fi
done

rm data/tmp.dat data/tmp2.dat
