# LINT
Longitudinal Investigation of Non-Transparency (LINT): using flats from CCDs to find the amount of dust, debris, or other contamination present on a sensor's surface. This program uses flats from CCDs to find the amount of dust, debris, or other contamination present on a sensor's surface. 

## The code will:
* Load flats (fits).
* Subtract overscan and mask overscan regions (if overscanSubtractBOOL is "True").
* Scale the flats to a common mean.
* Stack the flats using a median.
* Subtract the average sky value.
* Multiply the values by -1 to make to make attenuation spots appear positive to photometry code. 
* Run Source Extractor on the image to detect the debris.
* Print a detailed map of the debris locations.
* Analyze and plot histograms showing the amount of contamination.
* Batch process data to show the accumulation of debris over time.

## Programs, packages, and wrappers:
* Interpreter: python 3
* PyDev: 4.5.5.201603221110
* Numpy: 1.11.0
* Astropy: 1.3
* Python-dev: python-dev 2.7.5-5ubuntu3
* Eclipse: eclipse-platform 3.8.1-5.1
* SExtractor: 2.19.5-2
* Matplotlib: 1.5.1-1ubuntu1
    
## Modules:
testAstro: 
* Test for issues with your astropy installation.

loadFits:
* Load fits files image data into a 3D array.
* Saves data to a fits file.
* Makes a directory for output products and move output products into it.
* Scans the images to insure that they are all the same size dimensionally.

loadConfig:
* Load LINT.config.

overscan:
* Subtract and remove overscan (if overscanSubtractBOOL bool is true).

scaleAndStack:
* Scales the images using a common mean (find the mean of all of the data and scale the data so that every image has that same baseline mean).
* Stack the images, using a median, into a single flat field image (median the images: meaning that the resulting value in a pixel in the final image is the median of the values in that same pixel in the input images).

skyValue:
* Subtracts the average sky value from the median stacked image.

callSExtractor
* Call SExtractor and send commands to process the stacked and inverted image. 
* Record the output from SExtractor.

analyzeSExOutput:
* Performs cuts to remove objects that are not debris.
   * Flags: no gremlins in photometry.
   * Flux: only want divots in original image.
   * SNR: signal to noise ratio. Calculate the signal-to-noise ratio as FLUX_ISO / FLUXERR_ISO, that is, the isophotal flux (photometry derived from the counts above the threshold minus the background) divided by the RMS error for the isophotal flux; in other words, the signal divided by the noise. 
   * FWHM: Full Width at Half Maximum. Very small values may be anomalous and not represent debris.
* Make histograms of:
   * Area of debris.
   * Debris versus clean area.

batch:
* Create a list that groups the fits files by date.
* Run LINT on pre-grouped (by date) fits files.
* Plot the debris accumulation over time as: scatter plot.
    
## To do:
* Add logger.
* Add help command in optional arguments.
* Check to see if dependencies are installed.
* Mask bad pixel columns.
* Test installation code.
    
------------------------------------------------------------------------------------------------------------------------------
## This research makes use of:
* Astropy, a community-developed core Python package for Astronomy (Astropy Collaboration, 2013).
* Bertin, E. & Arnouts, S. 1996: SExtractor: Software for source extraction, Astronomy & Astrophysics Supplement 317, 393
* PyDev for Eclipse 4.5.5.201603221110 org.python.pydev.feature.feature.group Fabio Zadrozny
* Hunter, J. D. Matplotlib: A 2D graphics environment. 2007
