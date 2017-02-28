'''
@title overscan
@author: Rebecca Coles
Updated on Nov 16, 2016

Subtract and remove overscan if overscanSubtractBOOL bool is true

'''
# Import
from numpy import delete, copy, zeros, array, mean, count_nonzero
from astropy.io import fits

def subtractOverscan(overscanSubtractBOOL, overscanRows, overscanColumns, fitsArrayTimeSubtraction):
#Subtract overscan if overscanSubtract is true
    if overscanSubtractBOOL == bool(1):
        print( "You have selected to subtract bias in your image using overscan")
        print( "LINT will now subtract the overscan from your image and mask the overscan regions")
        #Convert overscan strings from config file to lists (overscanRows, overscanColumns)
        rows = array(stringToList(overscanRows))
        if count_nonzero(rows) != 0: #if rows is not empty ([0]), remove the last element of the array (since numpy arrays start at row 0 not row 1)
            rows = rows[:-1].copy()
        columns = array(stringToList(overscanColumns))
        if count_nonzero(columns) != 0: #if columns is not empty ([0]), remove the last element of the array (since numpy arrays start at columns 0 not row 1)
            columns = columns[:-1].copy()
        #Initialize numpy arrays of overscan rows and columns
        overscanMeanRowGroups = zeros((fitsArrayTimeSubtraction.shape[0],rows.shape[0]))
        overscanMeanColumnGroups = zeros((fitsArrayTimeSubtraction.shape[0],columns.shape[0]))
        overscanMean = zeros((fitsArrayTimeSubtraction.shape[0]))
        subtractedArray = zeros((fitsArrayTimeSubtraction.shape[0],fitsArrayTimeSubtraction.shape[1],fitsArrayTimeSubtraction.shape[2]))
        #Copy array
        arrayCopy = copy(fitsArrayTimeSubtraction)
        #Get means of overscan sections
        for ii in range(arrayCopy.shape[0]): #########################################################################
            if count_nonzero(rows) != 0: #only proceed if rows is not empty ([0])
                for xx in range(rows.shape[0]):
                    overscanMeanRowGroups[ii,xx] = int(arrayCopy[ii,rows[xx],:].mean())
            if count_nonzero(columns) != 0: #only proceed if columns is not empty ([0])
                for yy in range(columns.shape[0]):
                    overscanMeanColumnGroups[ii,yy] = int(arrayCopy[ii,:,columns[yy]].mean())
        #Subtract overscans from array
        if (count_nonzero(rows) != 0) and (count_nonzero(columns) != 0): #rows and columns are not empty
            for jj in range(arrayCopy.shape[0]):
                overscanMean[jj] = (overscanMeanRowGroups[jj,:].mean() + overscanMeanColumnGroups[jj,:].mean())/2
                subtractedArray[jj] = arrayCopy[jj,:,:] - overscanMean[jj]
        elif (count_nonzero(rows) == 0) and (count_nonzero(columns) != 0):#rows empty
            for kk in range(arrayCopy.shape[0]):
                overscanMean[kk] = overscanMeanColumnGroups[kk,:].mean()
                subtractedArray[kk] = arrayCopy[kk,:,:] - overscanMean[kk]
        elif (count_nonzero(rows) != 0) and (count_nonzero(columns) == 0):#columns empty
            for ll in range(arrayCopy.shape[0]):
                overscanMean[ll] = overscanMeanRowGroups[ll,:].mean()
                subtractedArray[ll] = arrayCopy[ll,:,:] - overscanMean[ll]
        else:
            exit( 'Something went wrong with your overscan subtraction. Check LINT.config to see if you entered your overscan rows and/or columns correctly.')
        #Numpy delete overscan Rows (axis = 1)
        subtractedAndRemoved = delete(subtractedArray,rows,1)
        #Numpy delete overscan Columns (axis = 2)
        subtractedAndRemoved = delete(subtractedAndRemoved,columns,2)
        #Return overscan subtracted array
        print( "Overscan subtraction and masking complete")
        return subtractedAndRemoved
    else:
        return fitsArrayTimeSubtraction 
    
def stringToList(x):
#Convert overscan strings from config file to lists (overscanRows, overscanColumns)
    result = []
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)
    return result
        