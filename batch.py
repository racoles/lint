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
from astropy.io import fits

def autoGroup(filepathsAndFileNames, ext):
#Create a list of fits files from a given directory that indicates the date that the flat field image was taken
#The list will indicate which date "group" each image should be in
    #Load the header information for all of the images into a list
    hdulist = [fits.open(image, ext) for image in filepathsAndFileNames]

def timePlot():
#Plot the debris accumulation over time as: hist
#X axis: time
#Y axis: debris