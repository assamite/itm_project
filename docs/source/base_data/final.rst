``final.dat`` 
=============

This data consists of data file ``final.dat`` and side information file ``final.sdat``.
Data consists of 20000 floating point numbers seprated by new lines and side 
information contains two floating point numbers for each line in data. Data and
side information was grouped line by line to form a three dimensional data points
**[x, y, z]**, where **x** contains data to compress and **y** and **z** the side 
information columns 1 and 2. For closer inspection, the data was plotted in 3D 
space as is seen in :ref:`final_1`

.. _final_1:

.. figure:: figures/final_1.png

	Figure 1. Data and side information plotted in 3D space.
	

.. _final_curve

.. figure:: figures/final_curve.png	

	Figure 2. Curve fitted to points near the maximum of Z.
	
	
.. _final_1plane

.. figure:: figures/final_1plane.png

	Figure 3. Splitting plane generated from the curve in Figure 2.
	
	
.. _final_split0_plane

.. figure:: figures/final_split0_plane.png

	Figure 4. Plane fitted to points under the splitting plane.
	
	
.. _final_split0_residuals

.. figure:: figures/final_split0_residuals.png

	Figure 5. Residuals of data points in question compared to plane in Figure 4.


.. _final_split1_plane

.. figure:: figures/final_split1_plane.png

	Figure 6. Plane fitted to points above the splitting plane.



.. _final_split1_residuals

.. figure:: figures/final_split1_residuals.png

	Figure 7. Residuals of data points in question compared to plane in Figure 6.
