'''
@title overscan
@author: Rebecca Coles
Updated on Nov 16, 2016

Subtract and remove overscan if overscanSubtractBOOL bool is true

'''
# Import
from numpy import delete, copy, empty
def subtractOverscan(overscanSubtractBOOL, overscanRows, overscanColumns, fitsArrayTimeSubtraction):
#Subtract overscan if overscanSubtract is true
    if overscanSubtractBOOL == bool(1):
        print "You have selected to subtract bias in your image using overscan."
        print "LINT will now subtract the overscan from your image, and mask the overscan regions"
        #2D to start MAKE 3D
        #Initialize numpy lists of overscan rows and columns
        rows = empty(overscanRows)
        columns = empty(overscanColumns)
        overscanMeanRowGroups = empty((fitsArrayTimeSubtraction.shape[0],rows.shape[0]))
        overscanMeanColumnGroups = empty((fitsArrayTimeSubtraction.shape[0],columns.shape[0]))
        overscanMean = empty((fitsArrayTimeSubtraction.shape[0]))
        subtractedArray = empty((fitsArrayTimeSubtraction.shape[0],fitsArrayTimeSubtraction.shape[1],fitsArrayTimeSubtraction.shape[2]))
        #Copy array
        arrayCopy = copy(fitsArrayTimeSubtraction)
        #Get means of overscan sections
        for ii in range(arrayCopy.shape[0]):
            for xx in range(rows.shape[0]):
                overscanMeanRowGroups[ii,xx] = arrayCopy[ii,rows[xx],:].mean
            for yy in range(columns.shape[0]):
                overscanMeanColumnGroups[ii,yy] = arrayCopy[ii,:,columns[yy]].mean
        #Subtract overscans from array
        for jj in range(arrayCopy.shape[0]):
            overscanMean[jj] = (overscanMeanRowGroups[jj,:].mean + overscanMeanColumnGroups[jj,:].mean)/2
            subtractedArray[jj] = arrayCopy[jj,:,:] - overscanMean[jj]
        #Numpy delete overscan Rows (axis = 1)
        subtractedAndRemoved = delete(subtractedArray,rows,1)
        #Numpy delete overscan Columns (axis = 2)
        subtractedAndRemoved = delete(subtractedAndRemoved,columns,2)
        #Return overscan subtracted array
        return subtractedAndRemoved
    else:
        return fitsArrayTimeSubtraction
        