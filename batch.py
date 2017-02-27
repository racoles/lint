'''
@title batch
@author: Rebecca Coles
Updated on Apr 11, 2016

autogroup:
create a list that groups the fits files by date.

timePlot:
#Plot the debris accumulation over time as: hist
    X axis: time
    Y axis: debris
'''
#will be merging groups of fits files. so will need to sort and then run lint on groups

# Import #######################################################################################
import loadFITS, scaleAndStack, callSExtractor, analyzeSExOutput
from loadConfig import loadConfig
from overscan import subtractOverscan
from skyValue import subtractAverageSky
from timeSubtraction import timeSub
from astropy.io import fits

def autoGroup(filepathsAndFileNames, ext):
#Create a list of fits files from a given directory that indicates the date that the flat field image was taken
#The list will indicate which date "group" each image should be in
    #Load the header information for all of the images into a list
    hdulist = [fits.open(image, ext) for image in filepathsAndFileNames]
    #Create list to assocate the fits file with the date that it was imaged
    for ii in range(len(filepathsAndFileNames))
        dateList[ii] = [ii, filepathsAndFileNames[ii] , hdulist[ii][ext].header[date]]
    print(datelist)
    
def processByDate(lintDict):
#Run LINT on pre-grouped (by date) fits files


######
    #Subtract overscan, and mask overscan regions, if overscanSubtractBOOL is "True"
    fitsArrayOverscanSubtracted = subtractOverscan(lintDict['overscanSubtractBOOL'], lintDict['overscanRows'],
                                                   lintDict['overscanColumns'], loadFITS.openFiles(loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'], lintDict['rows'], lintDict['columns']))
    #prepare the image for analysis
        #scale and stack images.
        #subtract the average sky value from the image. 
        #invert the image to make attenuation spots appear positive to photometry code.
    invertedImage = (subtractAverageSky(scaleAndStack.stackImages(scaleAndStack.scaleToMean(fitsArrayOverscanSubtracted))))*(-1)
    #save the scaled, stacked, inverted image
    outputName, output_folder_path = loadFITS.saveFITS(lintDict['fitsPath'], invertedImage, lintDict['outputFITS'])
    #send the scaled/stacked/inverted image to SExtractor with the user give parameter file
    callSExtractor.sendSEImage(lintDict['fitsPath'], outputName, lintDict['SExParameterFile'])
    #read SExtractor output file, and make cuts to SExtractor output table
    cutTable = analyzeSExOutput.cutsSExOutput(analyzeSExOutput.loadSExOutput(lintDict['SExParameterFile'], output_folder_path),
                                              lintDict['flagLimit'], lintDict['fluxLimit'], lintDict['SNRlimit'], 
                                              lintDict['FWHMlimit'], output_folder_path)
    #create the histogram
    n1, bin_centers = analyzeSExOutput.createHist(cutTable, output_folder_path)
    #create a log10 plot
    logNPlot = analyzeSExOutput.logPlot(n1, bin_centers, output_folder_path)

def timePlot(datelist):
#Plot the debris accumulation over time as: hist
#X axis: time
#Y axis: debris
    #timePlot uses autogroup's datelist to arrange data by date:
    #DATE    = '2016-11-27T16:10:41.041' / Creation Date and Time of File
    #remove text after "T"
    datelist[ii][:][2].split('T', 1)[0] for ii in range(len(datelist))
    #sort by date