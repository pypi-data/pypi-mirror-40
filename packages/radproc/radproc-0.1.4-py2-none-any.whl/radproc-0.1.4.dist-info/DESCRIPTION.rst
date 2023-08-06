===================================================================================================
 Radproc - A GIS-compatible Python-Package for automated RADOLAN Composite Processing and Analysis
===================================================================================================

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1313701.svg
   :target: https://doi.org/10.5281/zenodo.1313701


Radproc is an open source Python library intended to facilitate precipitation data processing and analysis for GIS-users.
It provides functions for processing, analysis and export of RADOLAN (Radar Online Adjustment) composites and rain gauge data in MR90 format.
The German Weather Service (DWD) provides the RADOLAN RW composites for free in the Climate Data Center
but the data processing represents a big challenge for many potential users.
Radproc's goal is to lower the barrier for using these data, especially in conjunction with ArcGIS.
Therefore, radproc provides an automated ArcGIS-compatible data processing workflow based on pandas DataFrames and HDF5.
Moreover, radproc's arcgis module includes a collection of functions for data exchange between pandas and ArcGIS.


.. note:: Please cite radproc as Kreklow, J. (2018): Radproc - A GIS-compatible Python-Package for automated RADOLAN Composite Processing and Analysis. Zenodo. http://doi.org/10.5281/zenodo.1313701


Radproc's Main Features 
~~~~~~~~~~~~~~~~~~~~~~~

Raw Data Processing
-------------------

	* Support for the reanalyzed RADOLAN products RW (60 min), YW and RY (both 5 min. resolution)
	* Automatically reading in all binary RADOLAN composites from a predefined directory structure
	* Optionally clipping the composites to a study area in order to reduce data size
	* Default data structure: Monthly pandas DataFrames with full support for time series analysis and spatial location of each pixel
	* Efficient data storage in HDF5 format with fast data access and optional data compression
	* Easy downsampling of time series
	* Reading in DWD rain gauge data in MR90 format into the same data structure as RADOLAN.

Data Exchange with ArcGIS
-------------------------

	* Export of single RADOLAN composites or analysis results into projected raster datasets or ESRI grids for your study area
	* Export of all DataFrame rows into raster datasets in a new file geodatabase, optionally including several statistics rasters
	* Import of dbf tables (stand-alone or attribute tables of feature classes) into pandas DataFrames
	* Joining DataFrame columns to attribute tables
	* Extended value extraction from rasters to points (optionally including the eight surrounding cells)
	* Extended zonal statistics

Analysis
--------

	* Calculation of precipitation sums for arbitrary periods of time
	* Heavy rainfall analysis, e.g. identification, counting and export of rainfall intervals exceeding defined thresholds
	* Data quality assessment
	* Comparison of RADOLAN and rain gauge data
	* *In preparation: Erosivity analysis, e.g. calculation of monthly, seasonal or annual R-factors*

Documentation
~~~~~~~~~~~~~

The full documentation for the latest radproc version is available at http://www.pgweb.uni-hannover.de/

Most of the docs are also hosted at https://radproc.readthedocs.io which will provide support for docs of older versions in future,
but unfortunately Readthedocs doesn't seem to support sphinx autodocs for the arcpy module which is not hosted at PyPI.
Consequently, the docs for the radproc.arcgis module are missing here.
If you have any idea how to fix this issue, please let me know.

