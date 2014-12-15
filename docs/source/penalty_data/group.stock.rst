``group.stock.dat``
===================

File ``group.stock.dat`` was seen to contain a shape in the data when unpacked
as signed or unsigned shorts (16 bit integers), as seen in Figure 1. The key point 
in the figure (as the group sees it) is that the difference between two consecutive 
shorts is usually rather small. 

.. figure:: figures/group_stock_shorts.png

	Figure 1. File ``group.stock`` unpacked as 1250 unsigned shorts.
	
Naturally, the regularity seen in the Figure 1. be taken into account when 
compressing. We used a simple method where we only marked the starting number of the sequence and then the 
difference between each number and its predecessor. This sequence was then concatenated 
as a string, e.g. suppose that the three first numbers are 3000, 2500 and 2700,
then, the yielded string would be ``3000-500+200``. 

Acquired string was Huffman coded using each character in the string as an 
individual symbol and written to a file. The (symbol, code) -mapping 
was then added into decompressor in order to obtain the original data.