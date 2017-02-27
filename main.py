'''
@title LINT: Longitudinal Investigation of Non-Transparency
@author: Rebecca Coles
Updated on Nov 21, 2016

This program uses flats from CCDs to find the amount of dust, debris, or other contamination present on a sensor's surface. 

The code will:
    -Load flats (fits).
    -Subtract overscan and mask overscan regions (if overscanSubtractBOOL is "True")
    -Scale the flats to a common mean.
    -Stack the flats using a median.
    -Subtract the average sky value.
    -Multiply the values by -1 to make to make attenuation spots appear positive to photometry code. 
    -Run Source Extractor on the image to detect the debris.
    -Print a detailed map of the debris locations.
    -Analyze and plot histograms showing the amount of contamination.
    -Batch process data to show the accumulation of debris over time.

Programs, packages, and wrappers:
    Interpreter: python 3
    PyDev: 4.5.5.201603221110
    Numpy: 1.11.0
    Astropy: 1.3
    Python-dev: python-dev 2.7.5-5ubuntu3
    Eclipse: eclipse-platform 3.8.1-5.1
    SExtractor: 2.19.5-2
    Matplotlib: 1.5.1-1ubuntu1
    
Modules:
    testAstro: 
        Test for issues with your astropy installation.
    loadFits:
        Load fits files image data into a 3D array.
        Saves data to a fits file
    overscan:
        Subtract and remove overscan (if overscanSubtractBOOL bool is true)
    scaleAndStack:
        Scales the images using a common mean.
            (find the mean of all of the data and scale the data so that every image has that same baseline mean)
        Stack the images, using a median, into a single flat field image. 
            (median the images: meaning that the resulting value in a pixel in the final image is the median of the values in that same pixel in the input images.)
    skyValue:
        Subtracts the average sky value from the median stacked image
    callSExtractor
        Call SExtractor and send commands to process the stacked and inverted image. 
        Record the output from SExtractor.
    analyzeSExOutput
        Performs cuts to remove objects that are not debris.
            Flags: no gremlins in photometry.
            Flux: only want divots in original image.
            SNR: signal to noise ratio. Calculate the signal-to-noise ratio as FLUX_ISO / FLUXERR_ISO, that is, 
                the isophotal flux (photometry derived from the counts above the threshold minus the background) 
                divided by the RMS error for the isophotal flux; in other words, the signal divided by the noise. 
            FWHM: Full Width at Half Maximum. Very small values may be anomalous and not represent debris.
        Make histograms of:
            area of debris
            debris versus clean area
    
To do:
    -add check to make sure that images are the same size
    -add logger
    -fitting
    -histograms
    -add module to handle fpack & funpack FITS image compression
    -batch processing
    -save fig
    -auto group fits files by date
    -accept multi-extension fits files
    -add help command in optional arguments
    -check to see if dependencies are installed
    -add Try command for errors
    -mask bad pixel columns
    -test installation code
    
------------------------------------------------------------------------------------------------------------------------------
This research makes use of:
    -Astropy, a community-developed core Python package for Astronomy (Astropy Collaboration, 2013).
    -Bertin, E. & Arnouts, S. 1996: SExtractor: Software for source extraction, Astronomy & Astrophysics Supplement 317, 393
    -PyDev for Eclipse 4.5.5.201603221110 org.python.pydev.feature.feature.group Fabio Zadrozny
    -Hunter, J. D. Matplotlib: A 2D graphics environment. 2007
'''
# Import #######################################################################################
#import loadFITS, scaleAndStack, callSExtractor, analyzeSExOutput
from loadConfig import loadConfig
#from overscan import subtractOverscan
#from skyValue import subtractAverageSky
#from timeSubtraction import timeSub
from batch import processByDate

# Variables ####################################################################################

#Load LINT.config
#lintDict = loadConfig()

################################################################################################

if __name__ == '__main__':
    #Load dictionary of user inputs (from LINT.config) and begin processing. Using loadConfig to load variables from LINT.config into dictonary.
    processByDate(loadConfig())
    #Subtract overscan, and mask overscan regions, if overscanSubtractBOOL is "True"
#    fitsArrayOverscanSubtracted = subtractOverscan(lintDict['overscanSubtractBOOL'], lintDict['overscanRows'],
#                                                   lintDict['overscanColumns'], loadFITS.openFiles(loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'], lintDict['rows'], lintDict['columns']))
    #prepare the image for analysis
        #scale and stack images.
        #subtract the average sky value from the image. 
        #invert the image to make attenuation spots appear positive to photometry code.
#    invertedImage = (subtractAverageSky(scaleAndStack.stackImages(scaleAndStack.scaleToMean(fitsArrayOverscanSubtracted))))*(-1)
    #save the scaled, stacked, inverted image
#    outputName, output_folder_path = loadFITS.saveFITS(lintDict['fitsPath'], invertedImage, lintDict['outputFITS'])
    #send the scaled/stacked/inverted image to SExtractor with the user give parameter file
#    callSExtractor.sendSEImage(lintDict['fitsPath'], outputName, lintDict['SExParameterFile'])
    #read SExtractor output file, and make cuts to SExtractor output table
#    cutTable = analyzeSExOutput.cutsSExOutput(analyzeSExOutput.loadSExOutput(lintDict['SExParameterFile'], output_folder_path),
#                                              lintDict['flagLimit'], lintDict['fluxLimit'], lintDict['SNRlimit'], 
#                                              lintDict['FWHMlimit'], output_folder_path)
    #create the histogram
#    n1, bin_centers = analyzeSExOutput.createHist(cutTable, output_folder_path)
    #create a log10 plot
#    logNPlot = analyzeSExOutput.logPlot(n1, bin_centers, output_folder_path)