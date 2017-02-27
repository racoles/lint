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
# Import
import loadFITS, scaleAndStack, callSExtractor, analyzeSExOutput
from datetime import strptime
from loadConfig import loadConfig
from overscan import subtractOverscan
from skyValue import subtractAverageSky
from timeSubtraction import timeSub
from astropy.io import fits
from operator import itemgetter

def autoGroup(filepathsAndFileNames, ext):
#Create a list of fits files from a given directory that indicates the date that the flat field image was taken
#The list will indicate which date "group" each image should be in
    #Load the header information for all of the images into a list
    hdulist = [fits.open(image, ext) for image in filepathsAndFileNames]
    #Create list to associate the fits file with the date that it was imaged
    dateList = []
    for ii in range(len(filepathsAndFileNames)):
        dateList.append([filepathsAndFileNames[ii], hdulist[ii][ext].header[date]])
    #Remove the time information from the date strings
    for jj in range(len(dateList)):
        dateList[jj][1] = dateList[jj][1].split('T', 1)[0] #remove time
        dateList[jj][1] = dateList[jj][1].replace("T", "") #remove 'T' character
    #Sort the list by date
    sorted(dateList, key=lambda x: strptime(x[1],'%Y-%m-%d')) #sort by second column
    #Add grouping column
    dateList = [kk + [0] for kk in dateList]
    #Tag each fits file with a group number
    ittr = 0
    for ll in range(len(dateList)):
        if ll == 0:
            dateList[ll][2] = 0
        elif dateList[ll][1] == dateList[ll-1][1]:
            dateList[ll][2] = ittr
        else:
            ittr += 1
            dateList[ll][2] = ittr    
    print(dateList)
    return dateList
    
def processByDate(lintDict):
#Run LINT on pre-grouped (by date) fits files
    #group fits files by date
    dateList = autoGroup(loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'])
    #Processing loop
    #Extract list of objects in a given group
    #Process group
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