'''
@title batch
@author: Rebecca Coles
Updated on Apr 11, 2016

autogroup:
Create a list that groups the fits files by date.

processByDate:
Run LINT on pre-grouped (by date) fits files

timePlot:
#Plot the debris accumulation over time as: hist
    X axis: time
    Y axis: debris
'''
# Import
import loadFITS, scaleAndStack, callSExtractor, analyzeSExOutput, datetime, os
import matplotlib.pyplot as plt
from loadConfig import loadConfig
from overscan import subtractOverscan
from skyValue import subtractAverageSky
from astropy.io import fits
from operator import itemgetter
from numpy import append, empty, amin, amax, diff

def autoGroup(filepathsAndFileNames, ext):
#Create a list of fits files from a given directory that indicates the date that the flat field image was taken
#The list will indicate which date "group" each image should be in
    #Load the header information for all of the images into a list
    hdulist = [fits.open(image) for image in filepathsAndFileNames]
    #Create list to associate the fits file with the date that it was imaged
    dateList = []
    for ii in range(len(filepathsAndFileNames)):
        dateList.append([filepathsAndFileNames[ii], hdulist[ii][ext].header['DATE']])
    #Remove the time information from the date strings, assuming standard fits date time reporting: '2016-11-27T16:10:41.041'
    for jj in range(len(dateList)):
        dateList[jj][1] = dateList[jj][1].split('T', 1)[0]  #remove time
    for kk in range(len(dateList)):
        dateList[kk][1].replace("T", "") #remove 'T' character
    #Add grouping column
    dateList = [ll + [0] for ll in dateList]
    #Determine how many groups are needed
    allPossibleDates = []
    for ll in range(len(dateList)):
        if dateList[ll][1] not in allPossibleDates:
            allPossibleDates.append(dateList[ll][1])
    #Sort the dates in ascending order
    sorted(allPossibleDates, key=lambda xx: datetime.datetime.strptime(xx,'%Y-%m-%d')) #sort by date
    #Tag each fits file with a group number
    for mm in range(len(allPossibleDates)):
        for nn in range(len(dateList)):
            if allPossibleDates[mm] == dateList[nn][1]:
                dateList[nn][2] = mm
    return dateList, allPossibleDates
    
def processByDate(lintDict):
#Run LINT on grouped (by date) fits files
    print( "Looking in directory: ", lintDict['fitsPath'])
    #test the dimensions of the images in the directory
    loadFITS.imageDimensionTest(lintDict['rows'], lintDict['columns'], loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'])
    #group fits files by date
    dateList, allPossibleDates = autoGroup(loadFITS.makeList(lintDict['fitsPath']), lintDict['ext'])
    print( "FITS files in directory: ", len(dateList))
    #LINT Processing loop
    groupList = [] #this will be filled with all of the fits file names and paths of the fits files for a given group
    #timeTable = zeros((len(allPossibleDates),int(lintDict['rows']),int(lintDict['columns'])))
    timeTable = []
    for ii in range(len(allPossibleDates)):
        #Print counter to screen
        print('\n' * 2)
        print('PROCESSING GROUP ', ii, '/', len(allPossibleDates)-1)
        #Extract list of objects in a given group from dateList
        for jj in range(len(dateList)):
            if dateList[jj][2] == ii:
                groupList.append(dateList[jj][0]) #add the file path for fits file in date group number "groupNumber" to list
        print('GROUP ', ii, 'FLATS TAKEN ON: ', allPossibleDates[ii])
        #Process group
        #Subtract overscan, and mask overscan regions, if overscanSubtractBOOL is "True"
        fitsArrayOverscanSubtracted = subtractOverscan(lintDict['overscanSubtractBOOL'], lintDict['overscanRows'],
                                                       lintDict['overscanColumns'], loadFITS.openFiles(groupList, 
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
        #add cutTable from this group to a list of numpy arrays to be used in timePlot to plot debris accumulation over time
        timeTable.append(len(cutTable))
        #empty group list for next process iteration
        del groupList[:]
    return timeTable, allPossibleDates
        
def timePlot(lintDict):
#Plot the debris accumulation over time as: hist
#X axis: time
#Y axis: debris
    timeTable, allPossibleDates = processByDate(lintDict)
    #histogram: debris over time
    fig, ax = plt.subplots()
    n1, bins1, patches1 = ax.hist(timeTable, bins=len(timeTable), facecolor='blue')
    plt.xlabel('Image Date', labelpad=20)
    plt.ylabel('Number of Dust Spots')
    plt.title('Number of Dust Spots versus Image Date')
    plt.axis([amin(timeTable), amax(timeTable), amin(n1), amax(n1)])
    plt.grid(True)
    # Label the raw counts below the x-axis...
    bin_centers = 0.5 * diff(bins1) + bins1[:-1]
    for count, x in zip(n1, bin_centers):
    # Label the raw counts
        ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
                    xytext=(0, -18), textcoords='offset points', va='top', ha='center')
    # Give ourselves some more room at the bottom of the plot
    plt.subplots_adjust(bottom=.15)
    # Save histogram to file
    fig.set_size_inches(18.5, 10.5)
    plotDir = os.path.join(os.path.dirname(lintDict['fitsPath']), os.path.pardir)
    fig.savefig(os.path.join(plotDir, 'DebrisOverTime.png'))
    #Save plot
    print( 'Debris over time histogram saved to: ', plotDir)