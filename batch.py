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
    dateList.append([filepathsAndFileNames[ii], hdulist[ii][ext].header[date]]) for ii in range(len(filepathsAndFileNames))
    #Remove the time information from the date strings, assuming standard fits date time reporting: '2016-11-27T16:10:41.041'
    dateList[jj][1].split('T', 1)[0] for ii in range(len(datelist)) #remove time
    dateList[kk][1].replace("T", "") for kk in range(len(datelist)) #remove 'T' character
    #Sort the list by date
    sorted(dateList, key=lambda x: strptime(x[1],'%Y-%m-%d')) #sort by second column
    #Add grouping column
    dateList = [ll + [0] for ll in dateList]
    #Tag each fits file with a group number
    groups = 0
    for mm in range(len(dateList)):
        if mm == 0:
            dateList[mm][2] = 0
        elif dateList[mm][1] == dateList[mm-1][1]:
            dateList[mm][2] = groups
        else:
            groups += 1
            dateList[mm][2] = groups    
    print(dateList)
    return dateList, groups
    
def processByDate(lintDict):
#Run LINT on pre-grouped (by date) fits files
    #group fits files by date
    dateList, groups = autoGroup(loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'])
    #Processing loop
    groupNumber = 0 #this will track which group is being processed by LINT
    groupList = [] #this will be filled with all of the fits file names and paths of the fits files for a given group
    for ii in range(groups):
        #Extract list of objects in a given group from dateList
        for jj in range(groups):
            if dateList[jj][2] == groupNumber:
                groupList.append(dateList[jj][0]) #add the file path for fits file in date group number "groupNumber" to list
        #Process group
        #Subtract overscan, and mask overscan regions, if overscanSubtractBOOL is "True"
        fitsArrayOverscanSubtracted = subtractOverscan(lintDict['overscanSubtractBOOL'], lintDict['overscanRows'],
                                                       lintDict['overscanColumns'], loadFITS.openFiles(groupList), 
                                                        lintDict['ext'], lintDict['rows'], lintDict['columns']))
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
        del groupList[:]
        
def timePlot(datelist):
#Plot the debris accumulation over time as: hist
#X axis: time
#Y axis: debris
    #timePlot uses autogroup's datelist to arrange data by date:
    #DATE    = '2016-11-27T16:10:41.041' / Creation Date and Time of File
    #remove text after "T"
    datelist[ii][:][2].split('T', 1)[0] for ii in range(len(datelist))
    #sort by date