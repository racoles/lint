'''
@title overscan
@author: Rebecca Coles
Updated on Nov 16, 2016

Subtract and remove overscan if overscanSubtractBOOL bool is true

'''
# Import
from numpy import delete, copy, zeros, array

from astropy.io import fits

def subtractOverscan(overscanSubtractBOOL, overscanRows, overscanColumns, fitsArrayTimeSubtraction):
#Subtract overscan if overscanSubtract is true
    if overscanSubtractBOOL == bool(1):
        print "You have selected to subtract bias in your image using overscan"
        print "LINT will now subtract the overscan from your image and mask the overscan regions"
        #Convert overscan strings from config file to lists (overscanRows, overscanColumns)
        rows = array(stringToList(overscanRows))
        columns = array(stringToList(overscanColumns))
        #Initialize numpy arrays of overscan rows and columns
        overscanMeanRowGroups = zeros((fitsArrayTimeSubtraction.shape[0],rows.shape[0]))
        overscanMeanColumnGroups = zeros((fitsArrayTimeSubtraction.shape[0],columns.shape[0]))
        overscanMean = zeros((fitsArrayTimeSubtraction.shape[0]))
        subtractedArray = zeros((fitsArrayTimeSubtraction.shape[0],fitsArrayTimeSubtraction.shape[1],fitsArrayTimeSubtraction.shape[2]))
        #Copy array
        arrayCopy = copy(fitsArrayTimeSubtraction)
        #Get means of overscan sections
        for ii in range(arrayCopy.shape[0]): #########################################################################
            if rows.all() == True: #only proceed if rows is not empty ([0])
                for xx in range(rows.shape[0]):
                    overscanMeanRowGroups[ii,xx] = int(arrayCopy[ii,rows[xx],:].mean())
            if columns.all() == True: #only proceed if columns is not empty ([0])
                for yy in range(columns.shape[0]):
                    overscanMeanColumnGroups[ii,yy] = int(arrayCopy[ii,:,columns[yy]].mean())
        #Subtract overscans from array
        if (rows.all() == True) and (columns.all() == True): #rows and columns are not empty
            for jj in range(arrayCopy.shape[0]):
                overscanMean[jj] = (overscanMeanRowGroups[jj,:].mean() + overscanMeanColumnGroups[jj,:].mean())/2
                subtractedArray[jj] = arrayCopy[jj,:,:] - overscanMean[jj]
        elif (rows.all() == False) and (columns.all() == True):#rows empty
            for kk in range(arrayCopy.shape[0]):
                overscanMean[kk] = overscanMeanColumnGroups[kk,:].mean()
                subtractedArray[kk] = arrayCopy[kk,:,:] - overscanMean[kk]
        elif (rows.all() == True) and (columns.all() == False):#columns empty
            for ll in range(arrayCopy.shape[0]):
                overscanMean[ll] = overscanMeanRowGroups[ll,:].mean()
                subtractedArray[ll] = arrayCopy[jj,:,:] - overscanMean[ll]
        else:
            print 'Something went wrong with your overscan subtraction. Check LINT.config to see if you entered your overscan rows and/or columns correctly.'
            return arrayCopy
        #Numpy delete overscan Rows (axis = 1)
        subtractedAndRemoved = delete(subtractedArray,rows,1)
        #Numpy delete overscan Columns (axis = 2)
        subtractedAndRemoved = delete(subtractedAndRemoved,columns,2)
        #Return overscan subtracted array
        print "Overscan subtraction and masking complete"
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
        