'''
@title timeSubtraction
@author: Rebecca Coles
Updated on Apr 26, 2016

Subtract a fits file from a later exposure to remove artifacts.
'''
# Import
from loadFITS import makeList, openFiles
from numpy import delete, array

def timeSub(fileDir, ext):
#Subtract a fits file from a later exposure to remove artifacts.
    #load the fits file image data into a list (3D array)
    filepathsAndFileNames = makeList(fileDir)     
    files = openFiles(filepathsAndFileNames, ext)
    #Convert to 3D numpy array
    numpyArray = array(files)
    #subtract the last file from all of the preceding ones
    #delete the fits that was used for the subtraction
    #return delete(files-files[-1], [len(filepathsAndFileNames)-1], 0)
    return numpyArray