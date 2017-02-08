'''
@title loadFITS
@author: Rebecca Coles
Updated on Apr 6, 2016

Loads the flats fits files
Saves data to a fits file
'''
# Import
import glob, os, time, datetime
from astropy.io import fits
from loadConfig import loadConfig

def outputsFolder(files_path, *default_parameters, **keyword_parameters):
#make a directory for output products and move output products into it
    #Create folder for output products named with the date
    if ('newFolder' in keyword_parameters):
        today = datetime.date.today()  # get today's date as a datetime type  
        todaystr = today.isoformat()   # get string representation: YYYY-MM-DD from a datetime type.
        output_path = os.path.dirname(os.path.dirname(files_path))
        #Make output dir. Append # to dir name if dir already exists
        if not os.path.exists(os.path.join(output_path, todaystr)):  #Folder doesn't exist
            new_folder_path = os.mkdir(os.path.join(output_path, todaystr))
        else: #Folder does exist
            folder_exist = True
            iterator = 1
            while folder_exist == True:
                if not os.path.exists(os.path.join(output_path, todaystr, '_', iterator)):
                   new_folder_path = os.mkdir(os.path.join(output_path, todaystr, '_', iterator))
                   folder_exist = False
                   iterator = iterator + 1
                return new_folder_path
    elif ('moveFileName' in keyword_parameters): #just moving files, not making a dir
        if os.path.isfile(os.path.join(os.getcwd(), keyword_parameters['moveFileName'])):
            os.rename(os.path.join(os.getcwd(), keyword_parameters['moveFileName']), os.path.join(new_path, keyword_parameters['moveFileName']))

def makeList(fileDir):
#make a list of the files in the directory
    #setting up to list files
    filepathsAndFileNames = glob.glob(fileDir + '*')
    print "Looking in directory: ", fileDir
    print "FITS files in directory: ", len(filepathsAndFileNames)
    return filepathsAndFileNames

def openFiles(filepathsAndFileNames, ext):
#load the fits file image data into a list (3D array) 
    fitsImages = [fits.getdata(image, ext) for image in filepathsAndFileNames]
    return fitsImages

def saveFITS(fitsPath, invertedImage, outputFITS):
#save an numpy array as a fits file
    #create output folder
    #set output file name
    s = ''
    seq = (outputFITS, '_scaled-stacked-inverted.fits')
    outputName = s.join(seq)
    print 'Scaled/Stacked/Inverted file: ', outputName
    #save fits
    hdu = fits.PrimaryHDU(invertedImage)
    hdu.writeto(fitsPath, clobber=True)
    f = open(os.path.join(fitsPath, outputName), 'r')
    return f.name