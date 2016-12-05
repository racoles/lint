'''
@title skyValue
@author: Rebecca Coles
Updated on Apr 11, 2016

subtractAverageSky:
Subtracts the average sky value from the median stacked image
'''
# Import
from numpy import average

def subtractAverageSky(medianStack):
#Find the average sky value and subtract it from the stacked image
    #subtract the average sky value from the image
    skySubtracted =  medianStack - average(medianStack)
    return skySubtracted