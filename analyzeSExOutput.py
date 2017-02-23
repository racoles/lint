'''
@title analyzeSExOutput
@author: Rebecca Coles
Updated on Apr 13, 2016

Performs cuts to remove objects that are not debris:
    Flags: no gremlins in photometry.
    Flux: only want divots in original image.
    SNR: signal to noise ratio. Calculate the signal-to-noise ratio as FLUX_ISO / FLUXERR_ISO, that is, 
        the isophotal flux (photometry derived from the counts above the threshold minus the background) 
        divided by the RMS error for the isophotal flux; in other words, the signal divided by the noise. 
Make histograms of:
    area of debris
    debris versus clean area
'''
# Import
from loadFITS import outputsFolder

from astropy.io.ascii import SExtractor, write
from numpy import logical_not, pi, amin, amax, arange, diff, log10, column_stack, poly1d, polyfit
from re import search
import matplotlib.pyplot as plt

def loadSExOutput(parameterFile, output_folder_path):
#Load SExtractor output to table    
    #Find name of SExtractor output file from parameter file
    with open(parameterFile, 'r') as inF:
        for line in inF:
            if 'CATALOG_NAME' in line:
                result = search('CATALOG_NAME(.*)#', line)
    sexOutputFileName = str.strip(result.group(1))
    print('SExtractor output file:', sexOutputFileName)
    #Read SExtractor output file
    so = SExtractor()
    sexOutput = so.read(sexOutputFileName)
    #move Sextractor output cataloge to output products file
    outputsFolder(output_folder_path, moveFileName=sexOutputFileName)
    #move Sextractor output check image to output products file (if there is one and it has the default name)
    outputsFolder(output_folder_path, moveFileName='aper.fits')
    return sexOutput

def cutsSExOutput(output, flagLimit, fluxLimit, SNRlimit, FWHMlimit, output_folder_path):
#Make cuts to data as decided by user
    #print original data object number
    print( 'Number of object identified extracted by SExtractor: ', len(output))
    #Flag cut
    cutFlags = output[logical_not(output['FLAGS'] > flagLimit)]
    print( 'Number of objects remaining after Flags cut:', len(cutFlags))
    #Flux cut
    cutFlux = cutFlags[logical_not(cutFlags['FLUX_AUTO'] < fluxLimit)]
    print( 'Number of objects remaining after Flux cut:', len(cutFlux))
    #SNR cut
    SNRcut = cutFlux[logical_not((cutFlux['FLUX_AUTO']/cutFlux['FLUXERR_AUTO']) < SNRlimit)]
    print( 'Number of objects remaining after SNR cut:', len(SNRcut))
    #FWHM cut
    FWHMcut = SNRcut[logical_not(SNRcut['FWHM_IMAGE'] < FWHMlimit)]
    print( 'Number of objects remaining after FWHM cut:', len(FWHMcut))
    #print number of remaining objects
    print( 'Number of objects remaining after all cuts: ', len(FWHMcut))
    #save list of data that survived the cuts to a file
    write(FWHMcut, 'SExtractor_output_after_cuts.csv')
    print('A list of the objects that survived the cuts: SExtractor_output_after_cuts.csv')
    #move Sextractor output file to output products file
    outputsFolder(output_folder_path ,moveFileName='SExtractor_output_after_cuts.csv')
    return FWHMcut

def createHist(cutTable, output_folder_path):
#Creates histograms from the SExtracted data
    #Computed obscured area by calculating pi*A*B, the product of semi-major times semi-minor axes.
    #These variables are referred to as A_IMAGE and B_IMAGE
    areaList = [(pi)*cutTable['A_IMAGE']*cutTable['B_IMAGE']]
    #histogram: obscured area
    fig, ax = plt.subplots()
    n1, bins1, patches1 = ax.hist(areaList, bins=20, facecolor='green')
    plt.xlabel('Areas of Dust Spot (square pixels)', labelpad=20)
    plt.ylabel('Number of Dust Spots')
    plt.title('Areas of Dust Spot versus Number of Dust Spots')
    plt.axis([amin(areaList), amax(areaList), amin(n1), amax(n1)])
    plt.grid(True)
    #plt.xticks(arange(amin(areaList), amax(areaList)+1, 10.0))
    #plt.yticks(arange(amin(n1), amax(n1)+1, 100))
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
    fig.savefig('hist.png')
    # Move hist to output folder
    outputsFolder(output_folder_path ,moveFileName='hist.png')
    print( 'Histogram saved to: ', output_folder_path)
    return n1, bin_centers
    
def logPlot(n1, bin_centers, output_folder_path):
#Hists typically look like a power law, where number of spots between A and A+dA scales as (spot area)^(-n).
    #remove zeros from n1
        #first combine lists
    stacked = column_stack((bin_centers, n1))
        #now remove zeros
    no_zeros = stacked[stacked[:,1] != 0]
    #log plot (as scatter)
    fig, ax = plt.subplots()
    ax.scatter(no_zeros[:,0], log10(no_zeros[:,1]))
    #add text with the fit function to the plot
    fit = polyfit(no_zeros[:,0], log10(no_zeros[:,1]),1)
    text = "y = %1.3f x + %1.3f" % (fit[0], fit[1])
    plt.text(0.17, 0.95, text, ha='center', va='center', transform=ax.transAxes)
    #plot best fit line
    plt.plot(no_zeros[:,0], poly1d(polyfit(no_zeros[:,0], log10(no_zeros[:,1]), 1))(no_zeros[:,0]),'r')
    plt.xlabel('Areas of Dust Spot (square pixels)', labelpad=10)
    plt.ylabel('Log10 Number of Dust Spots')
    plt.title('Areas of Dust Spot versus Log10 Number of Dust Spots')
    plt.gca().set_ylim(bottom=0)
    plt.gca().set_xlim(left=0)
    # Save plot to file
    #plt.show()
    fig.savefig('logplot.png')
    # Move logplot to output folder
    outputsFolder(output_folder_path ,moveFileName='logplot.png')
    print( 'Logplot saved to: ', output_folder_path)