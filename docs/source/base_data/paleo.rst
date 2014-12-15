``paleo.csv``
=============

The ``paleo.csv`` file contains scientific data about prehistoric ammonoids. The data is listed as fourteen attributes in a row, separated by semicolons. The first line in the field contains the names of the attributes. On the rest of the rows the first attribute is a string, representing the name of the ammonoid species, anonymised as random words of Finnish, and the rest are floating point numbers and integers representing different measures, e.g. diameters. The data contained two fields labeled ’maxdm’, and they are referenced 

The first idea was to just compress the whole thing using bzip2, which reduced the file size from roughly 329kB to 102kB, and this was actually our solution for the first return of this data. Next week we had more time to explore the data, and we found out that some of the fields in each record were reproducible form the other fields in the record by simple computations. Because bzip2 did so well on its own, we wondered whether manipulating the values to a more simple for would improve its results even further. We used the following formulas:

.. math::
	
	maxdm(1) &= ceil(dm)\\[3mm]
	maxdm(2) &= ceil(dm) \text{ or } maxdm(1)\\[3mm]
	ww/dm &=  \frac{ww}{dm}\\[3mm]
	ww/wh &= \frac{ww}{wh}\\[3mm]
	uw/dm &= \frac{uw}{dm}\\[3mm]
	WER &= (\frac{dm}{dm-ah})^2\\[3mm]
	lobes[i] &= lobes[i-1]. 

The next problem was, that even though the results of these computations often matched the values in the corresponding fields, the accuracies in which the original values in the data were reported seemed arbitrary. We made a remark, that the values of the fields ww/dm, ww/wh, uw/dm and WER were never integers :math:`1-9` (except in a couple of exceptions which we handled separately), so we could replace the original values of the fields with integers indicating the accuracy of the result. This made the decompression phase easy, and we got the originally roughly 10-symbol values replaced with just one symbol. 

Another trick used here was using letters as special markers. For example in the three distinct diameter fields, we left the ’dm’ field as it is. For ’maxdm(1)’ and ’maxdm(2)’, we replaced the values with ’a’, if the original value was just ’dm’ rounded up. To improve even further, we replaced ’maxdm(2)’ with ’b’, if it already wasn’t replaced with ’a’, and was equal to the value of ’maxdm(1)’. In other cases, we just left the original values to the modified data.

The ’lobes’ value didn’t seem to be reproducible from the other attributes, but seemed to often be the same in consecutive records (for species with the same ’first name’). We used the markers as before, and modified the values to ’a’ if they were the same as in the previous record. 

Running bzip2 compression on this modified data revealed a much improved result: we managed to squeeze the data to less than 64kB.