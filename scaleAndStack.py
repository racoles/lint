'''
@title scaleAndStack
@author: Rebecca Coles
Updated on Apr 8, 2016

scaleToMean:
Scale using a common mean:
    1)Find the mean value for all of the images (baseline).
    2)Find the means for each of the individual images.
    3)Scale the data such the the means of the individual images equal the baseline.
    
stackImages:    
Stacks the images into a single image using a median.
    median the images: the resulting value in a pixel in the final image is the median 
    of the values in that same pixel in the input images. The advantage of median combining 
    the images is that when one image has a very discrepant value (i.e. from a cosmic ray) 
    this doesn't dramatically affect the resultant value (a median is more resistant to one 
    discrepant value than an average). If you've taken at least three images, then this will 
    reject almost all cosmic ray events. Note that when there are an even number of input 
    values to a median, then it will average the two middle values (thus the motivation for 
    taking an odd number of images to combine).
'''
# Import
from numpy import mean, median

def scaleToMean(fitsArrayOverscan):
#Scale the images so that they all have the same mean
    #find the means of all of the image information in total
    baseline=mean(fitsArrayOverscan)
    #find the means of the individual images
    meansOfImages=[mean(x) for x in fitsArrayOverscan]
    print( 'Means of images: ',meansOfImages)
    print( 'Baseline for scale: ',baseline)
    #get the scale factor list
    scaleFactorList = meansOfImages - baseline
    #scale images
    scaledImages = [y+z for y,z in zip(fitsArrayOverscan,scaleFactorList)]
    return scaledImages

def stackImages(scaledImages):
#Stack the images into a single skyflat by median
    medianStack = median(scaledImages, axis=0)
    print( 'Scaled/Stacked/Inverted image dimensions (xpixels, ypixels):', medianStack.shape)
    return medianStack
