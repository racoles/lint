'''
@title callSExtractor
@author: Rebecca Coles
Updated on Apr 11, 2016

Call SExtractor and send commands to process the stacked and inverted image. 
Record the output from SExtractor.
'''
# Import
from os import system

def sendSEImage(fitsDir, outputName, parameterFile):
#Send image file and parameters to SExtractor
    #print contents of parameter file file to screen
    print 'Using SExtractor parameter file: ',parameterFile
    pf = open(parameterFile)
    #create SExtractor input command
    s = ' '
    seq = ('sextractor',outputName,'-c',pf.name)
    sexCommand = s.join(seq)
    print 'Talking to SExtractor'
    print 'Sending SExtractor command: ',sexCommand
    #call SExtractor and send image and parameter file
    system(sexCommand) #system waits until SExtractor is complete to continue