'''
@title overscan
@author: Rebecca Coles
Updated on Nov 16, 2016

Subtract and remove overscan if overscanSubtractBOOL bool is true

'''
# Import
from numpy import delete, copy, zeros, array
def subtractOverscan(overscanSubtractBOOL, overscanRows, overscanColumns, fitsArrayTimeSubtraction):
#Subtract overscan if overscanSubtract is true
    if overscanSubtractBOOL == bool(1):
        print "You have selected to subtract bias in your image using overscan"
        print "LINT will now subtract the overscan from your image, and mask the overscan regions"
        #Convert overscan strings from config file to lists (overscanRows, overscanColumns)
        rows = array(stringToList(overscanRows))
        columns = array(stringToList(overscanColumns))
        #Initialize numpy lists of overscan rows and columns
        overscanMeanRowGroups = zeros((fitsArrayTimeSubtraction.shape[0],rows.shape[0]))
        overscanMeanColumnGroups = zeros((fitsArrayTimeSubtraction.shape[0],columns.shape[0]))
        overscanMean = zeros((fitsArrayTimeSubtraction.shape[0]))
        subtractedArray = zeros((fitsArrayTimeSubtraction.shape[0],fitsArrayTimeSubtraction.shape[1],fitsArrayTimeSubtraction.shape[2]))
        #Copy array
        arrayCopy = copy(fitsArrayTimeSubtraction)
        #Get means of overscan sections
        for ii in range(arrayCopy.shape[0]):
            for xx in range(rows.shape[0]):
                overscanMeanRowGroups[ii,xx] = int(arrayCopy[ii,rows[xx],:].mean())
            for yy in range(columns.shape[0]):
                overscanMeanColumnGroups[ii,yy] = int(arrayCopy[ii,:,columns[yy]].mean())
        #Subtract overscans from array
        for jj in range(arrayCopy.shape[0]):
            overscanMean[jj] = (overscanMeanRowGroups[jj,:].mean() + overscanMeanColumnGroups[jj,:].mean())/2
            subtractedArray[jj] = arrayCopy[jj,:,:] - overscanMean[jj]
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
    result = [0]
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
    #else:
        #a = int(part)
        #result.append(a)
    return result
        