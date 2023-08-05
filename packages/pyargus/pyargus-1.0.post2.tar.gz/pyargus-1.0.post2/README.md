# pyArgus

This python package aims to implement signal processing algorithms applicabe in antenna arrays. The implementation mainly focuses on the beamforming and
direction finiding algorithms.
For array synthesis and radiation pattern optimization please check the "arraytool" python package.
https://github.com/zinka/arraytool and https://zinka.wordpress.com/ by S. R. Zinka

Named after Argus the giant from the greek mitology who had hundreds of eyes.

## The package is organized as follows:

- pyArgus: Main package
	- antennaArrayPattern: Implements the radiation pattern calculation of antenna arrays
	- beamform: Implements beamformer algorithms.
	- directionEstimation: Impelmenets DOA estimation algorithms and method for estimating the spatial correlation matrix.
- test: Sub package
        Contains demonstration functions for antenna pattern plot, beamforming and direction of arrival estimation. 

The documentation of the package is written in Jupyter notebook, wich can be found on the following sites:
Github: [tamaspeto.com](https://github.com/petotamas/pyArgus) 
[tamaspeto.com](https://www.tamaspeto.com/pyargus) 
Tamás Pető 2016-2019, Hungary



