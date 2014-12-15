``curve1.dat`` and ``ty.txt`` 
=============================


Model
-----

Data files ``curve1.dat`` and ``ty.txt`` consist of 2000 and 10,000 floating point numbers separated by line breaks. We plotted these as a function of the index of the number in the file, and found out that both files seem to have almost exactly similar periodic behaviour. The behaviour of the curve seems to change after the first :math:`\frac{5}{8}` of the data, so  we decided to model it in two parts.

The first part has some periodic 'bumps', and the first data point seems to be on top of one of such bumps so we started the modelling with a cosine function. As the bumps are round, but the deeps are really sharp, we took the absolute value, ranging now from :math:`0` to :math:`1`. Next, we wanted the top of the bumps to be at the same level, but the deeps to approach the :math:`x`-axis linearly. We dropped the function values by one (:math:`|\cos(x)|-1`), and multiplied with a (decreasing) linear function of the form :math:`ax+b`. Now we already achieved a considerably good fit, but the bumps were not quite wide enough. We first tried to solve this by using a higher wave and then cutting the tops of the bumps off, but later found an even better fit by squaring the :math:`|\cos(x)|-1`-part and multiplying by :math:`-1`.

In the second part of the data, we're again dealing with bumps, but this time there's two kinds of them: every other bump has equal height (at about :math:`0`), whereas every other seems to increase linearly. The deeps seem to decrease linearly in either case. We started again with a cosine function, and to achieve bumps with unequal heights we first added a constant :math:`0<h<1`, and then took the absolute value. Now we dropped the curve by :math:`1-h` to get the tops of the lower bumps to zero (to keep them equal after multiplication with a function), and finally multiplied this all with a linear function.

The final model was augmented with extra parameters for optimal fit (the tops of the bumps not exactly at zero etc.) and scaling (the period was not :math:`\pi`). The final model was of the form 

.. math::

	m(x)=\left\lbrace \begin{array}{ll}  -\:|\:ax+b\:|\cdot(|\:\cos(cx)\:|-1)^2 +d, & &\text{ if }x<\frac{5}{8}n\\
	(ex+f)(|\:\cos(gx+h)+i\:|+j)+k, & &\text{ otherwise.} \end{array} \right.

where :math:`n` is the number of data points in the file.


Implementation
--------------

Bit-juggling...

Curve1.dat
**********





Ty.txt
******
