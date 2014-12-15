monty_python 
====================

The idea in our penalty data was to create a pseudo-Fibonacci sequence, then pick a certain subsequence of
it and perform some bit manipulations to it in order to create a random appearance.

The sequence was created with the starting values of 1 and 3, thus generating the sequence 1,3,4,7,11,18,29,...
We then chose a subsequence, for instance the numbers between indeces 80 and 140, and forced the chosen numbers
into an 8 digit binary format. For each eight bit binary string, we moved the last 3 digits of this binary to the
front so that, for example, 10011010 would become 01010011. Finally, we concatenated these eight digit strings
together and used a suitable part of the resulting string as our penalty code in order to satisfy the length
requirement that was set for the data.

We used the same sequence in both penalty datas, just changed the starting index of the subsequence to be encoded
and the manner of the bit level manipulation. We represented each penalty data with a file of length 1 byte, since
we could generate the original data completely by running our generating algorithm again in the decompressor.
In the decoding phase we only needed to identify our data file, which was possible by looking at the single byte
content of the file.