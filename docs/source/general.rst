General Methods
===============

This section describes basic compression and decompression work flow, and some general methods used 
during the process.

Work Flow
---------

Compression and decompression both have general two-part work flow, where first
the appropriate bash script (:program:`compress.sh` or :program:`decompress.sh`) is executed. The shell
script decides if the file is handled using basic Unix functionality (:command:`cat`
or :command:`bzip2`), or passed to Python script which handles more complex compression 
(``compress.py``) or decompression (``d.py``). Both shell scripts identify the 
files by checking the length of the file. The main difference is that the
``decompress.sh`` looks first if there is a file named ``d.py``, and if it is 
not found, decompresses ``d.py.bz2`` using :command:`bzip2`.

If file is passed down to Python script, its identity is checked and appropriate
section in the script is executed. During compression identification
is done using the filename, and in decompression each individual file is 
identified by using ID byte (generated during the compression ) at the start of the file.


.. _huffman:

Huffman Coding and Decoding
---------------------------

`Huffman codes <http://en.wikipedia.org/wiki/Huffman_coding>`_ are optimal binary prefix codes for given data. We will cover here
how (symbol, code) -mappings are encoded in the project so that the Huffman
coding itself can be included in the compressed file.

The binary representation of the (symbol, code) -mappings used in this project
consists of three parts: 

	1. total number of codes
	2. (index, code length) -mappings
	3. concatenated binary codes
The first part's length is one byte, therefore restricting the amount of codes
to at most 256. Second part, i.e. *(index, code length)* -mappings, tells each symbol's 
index in the decompressor's symbol list and its binary code's length. *Index* part 
is always 8 bits long, but *code length* part's length, :math:`\#cl`, varies based on the maximum of the code 
lengths, i.e. :math:`\#cl = \lceil \, \log_{2}( \, \max( \, \{ \#c \mid c \in \text{codes} \} \, ) \, ) \, \rceil`,
as all the code lengths are subtracted by 1 during the compression, which is again
added during the decompression. The last part contains concatenated binary codes, which
can be split into individual codes using the code length information from the second part.
Finally, the whole concatenated binary string is padded with tailing zero bits in
order to get full bytes.

.. note::

	Suppose we have four symbols in the following order: ``A``, ``B``, ``C`` and ``D`` with codes
	``10``, ``111``, ``0`` and ``110``, respectively. Then, the Huffman code
	is encoded to a binary string::
	
		 #codes      A    #A     B    #B     C    #C     D    #D   codes   padding
		00000100 00000000 01 00000001 10 00000010 00 00000011 10 101110110 0000000 
		       |        |         |         |         |        |        |        |   
		bits   8       16        24        32        40       48       56       64
 

When compressing, we mark up what was the maximum code length, the amount of padding bytes,
and the list of used symbols for each generated Huffman code (that will have its mapping 
information added to the binary), and add the information to the appropriate part in decompressor.


bzip2
---------

Information about bzip2