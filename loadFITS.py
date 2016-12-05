'''
@title loadFITS
@author: Rebecca Coles
Updated on Apr 6, 2016

Loads the flats fits files
Saves data to a fits file
'''
# Import
import glob
from astropy.io import fits

def makeList(fileDir):
#make a list of the files in the directory
    #setting up to list files
    filepathsAndFileNames = glob.glob(fileDir + '*')
    print "Looking in directory: ", fileDir
    print "FITS Files in directory: ", len(filepathsAndFileNames)
    return filepathsAndFileNames

def openFiles(filepathsAndFileNames, ext):
#load the fits file image data into a list (3D array) 
    fitsImages = [fits.getdata(image, ext) for image in filepathsAndFileNames]
    return fitsImages

def saveFITS(fitsDir, invertedImage, outputFITS):
#save an numpy array as a fits file
    #set output file name
    s = ''
    seq = (outputFITS, '_scaled-stacked-inverted.fits')
    outputName = s.join(seq)
    print 'Scaled/Stacked/Inverted file: ', outputName
    #save fits
    hdu = fits.PrimaryHDU(invertedImage)
    hdu.writeto(fitsDir + outputName, clobber=True)
    f = open(fitsDir + outputName, 'r')
    return f.name