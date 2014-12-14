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


Huffman Coding and Decoding
---------------------------

`Huffman codes <http://en.wikipedia.org/wiki/Huffman_coding>`_ are optimal binary prefix codes for given data. We will cover here
how (symbol, Huffman code) -mappings are encoded in the project so that the Huffman
coding itself can be included in the compressed file.

 



bzip2
---------

Information about bzip2