'''
@title overscan
@author: Rebecca Coles
Updated on Nov 16, 2016

Subtract overscan if overscanSubtractBOOL bool is true

Remove overscan if overscanRemoveBOOL bool is true
'''
# Import
from numpy import delete, array

def subtractOverscan(overscanSubtractBOOL, overscanSubtractLocation, overscanTopRows, overscanBottomRows, overscanLeftColumns, overscanRightColumns, fitsArrayTimeSubtraction):
#Subtract overscan if overscanSubtract is true
    if overscanSubtractBOOL == bool(1):
        print "You have selected to subtract bias in your image using overscan."
        #Initalize array to hold the means for each area of overscan for each image in fitsArrayTimeSubtraction
        overscanMeans = [[] for ii in range(fitsArrayTimeSubtraction.shape[0])]
        #find the means of all of the overscan regions: top, right, bottom, left
        for xx in range(0, fitsArrayTimeSubtraction.shape[0]-1):
            overscanMeans[xx] = [fitsArrayTimeSubtraction[xx,0:overscanTopRows-1,:].mean(),
                                fitsArrayTimeSubtraction[xx,:,(fitsArrayTimeSubtraction.shape[2]-overscanRightColumns):].mean(), 
                                fitsArrayTimeSubtraction[xx,(fitsArrayTimeSubtraction.shape[1]-overscanBottomRows):,:].mean(), 
                                fitsArrayTimeSubtraction[xx,:,0:overscanLeftColumns-1].mean()]
        #Subtract bias from the image using the mean of the overscan region that the user specified
        for yy in range(0, fitsArrayTimeSubtraction.shape[0]-1):
            if overscanSubtractLocation == 1:
                fitsArrayTimeSubtraction[yy,:,:] = fitsArrayTimeSubtraction[yy,:,:] - overscanMeans[yy][0] #top
            elif overscanSubtractLocation == 2:
                fitsArrayTimeSubtraction[yy,:,:] = fitsArrayTimeSubtraction[yy,:,:] - overscanMeans[yy][1] #right
            elif overscanSubtractLocation == 3:
                fitsArrayTimeSubtraction[yy,:,:] = fitsArrayTimeSubtraction[yy,:,:] - overscanMeans[yy][2] #bottom
            elif overscanSubtractLocation == 4:
                fitsArrayTimeSubtraction[yy,:,:] = fitsArrayTimeSubtraction[yy,:,:] - overscanMeans[yy][3] #left
            else:
                print 'Warning: the overscan bias subtraction has failed. The "overscanSubtractLocation" parameter was out of bounds. This can be set in the config file.'
        #print location of overscan used for subtraction
        subRegion = overscanLocation(overscanSubtractLocation)
        print 'Subtracted bias using ', subRegion, ' overscan region'
        return fitsArrayTimeSubtraction
    else:
        return fitsArrayTimeSubtraction    

def removeOverscan(overscanRemoveBOOL, overscanTopRows, overscanBottomRows, overscanLeftColumns, overscanRightColumns, fitsArrayOverscanSubtracted):
#Remove overscan if overscanRemove is true
    if overscanRemoveBOOL == bool(1):
        #create list of rows to be removed
        rowList = range(0, overscanTopRows) + range(fitsArrayOverscanSubtracted.shape[0]-overscanBottomRows, fitsArrayOverscanSubtracted.shape[0])
        #remove rows
        removedRows = array([delete(xx,(rowList), axis=0) for xx in fitsArrayOverscanSubtracted])
        #create list of columns to be removed
        columnList = range(0, overscanLeftColumns) + range(removedRows.shape[1]-overscanRightColumns, removedRows.shape[1])
        #remove columns
        removedColumns = array([delete(yy,(columnList), axis=1) for yy in removedRows])
        #print location of overscan that was removed
        print 'Removed overscan (rows):','\n','From top: ',overscanTopRows,' from bottom: ',overscanBottomRows
        print 'Removed overscan (columns):', '\n', 'From left: ',overscanLeftColumns,' from right: ',overscanRightColumns
        return removedColumns
    else:
        return fitsArrayOverscanSubtracted
    
def overscanLocation(x): return {1: 'TOP', 2: 'RIGHT', 3: 'BOTTOM', 4: 'LEFT', 5: 'CUSTOM'}.get(x, 2)