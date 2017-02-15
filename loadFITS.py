'''
@title loadFITS
@author: Rebecca Coles
Updated on Apr 6, 2016

Makes a directory for output products and move output products into it
Loads the flats fits files
Saves data to a fits file
'''
# Import
import glob, os, time, datetime
from astropy.io import fits
from loadConfig import loadConfig

def outputsFolder(files_path, *default_parameters, **keyword_parameters):
#make a directory for output products and move output products into it
####################################################################################
#Optional parameters: 
#    'newFolder': indicates that you want to create a new output product folder 
#        (in the same directory as the fits files folder)
#    'moveFileName' = filename:  indicates that you want to move the named file into 
#        the output product folder
#Note: if you are making a new dir (newFolder): files_path is the fits files location.
#      if you are moving files to the output folder (moveFileName): files_path is the 
#        location of the output folder.
####################################################################################
#'newFolder'
    #Create folder for output products named with the date
    if ('newFolder' in keyword_parameters):
        today = datetime.date.today()  # get today's date as a datetime type  
        output_path = os.path.dirname(os.path.dirname(files_path)) #Here files_path is fits files location
        output_folder_name = 'LINT_Output_' + today.isoformat()
        #Make output dir. Append # to dir name if dir already exists
        if not os.path.exists(os.path.join(output_path, output_folder_name)):  #Folder doesn't exist
            os.mkdir(os.path.join(output_path, output_folder_name))
            new_folder_path = os.path.join(output_path, output_folder_name)
            print('New folder created for output products: ', new_folder_path)
            return new_folder_path
        else: #Folder does exist
            folder_exist = True
            iterator = 1
            while folder_exist == True:
                output_product_folder_name = output_folder_name + '_' + str(iterator)
                if not os.path.exists(os.path.join(output_path, output_product_folder_name)):
                   os.mkdir(os.path.join(output_path, output_product_folder_name))
                   new_folder_path = os.path.join(output_path, output_product_folder_name)
                   folder_exist = False
                iterator += 1
            print('New folder created for output products (in directory that contains fits files directory): ', new_folder_path)
            return new_folder_path
#'moveFileName'
    #Just moving files, not making a dir. Here, files_path is where you want to move the files to
    elif ('moveFileName' in keyword_parameters):
        if os.path.isfile(os.path.join(os.getcwd(), keyword_parameters['moveFileName'])):
            os.rename(os.path.join(os.getcwd(), keyword_parameters['moveFileName']), os.path.join(files_path, keyword_parameters['moveFileName']))

def makeList(fileDir):
#make a list of the files in the directory
    #setting up to list files
    filepathsAndFileNames = glob.glob(fileDir + '*')
    print( "Looking in directory: ", fileDir)
    print( "FITS files in directory: ", len(filepathsAndFileNames))
    return filepathsAndFileNames

def openFiles(filepathsAndFileNames, ext):
#load the fits file image data into a list (3D array)
    fitsImages = [fits.getdata(image, ext) for image in filepathsAndFileNames]
    #print('Unknown Compression. LINT accepts files of types: fits, fits.fz')
    return fitsImages

def saveFITS(fitsPath, invertedImage, outputFITS):
#save an numpy array as a fits file
    #create output dir
    output_folder_path = outputsFolder(fitsPath, newFolder=True)
    #name for output fits file
    outputName = outputFITS + '_scaled-stacked-inverted.fits'
    print( 'Scaled/Stacked/Inverted file: ', outputName)
    #save fits
    hdu = fits.PrimaryHDU(invertedImage)
    hdu.writeto(output_folder_path + '/' + outputName, overwrite=True)
    f = open(output_folder_path + '/' + outputName, 'r')
    return f.name, output_folder_path

def imageSizeTest(fitsImages):
#Scan the images in the array to insure that they are all the same size dimensionally.
#If an image is not the proper size, it will be removed from the array.
#The first image in the array will be used to set the standard size.
    #get dimensions of first image
    dimensions = [len(fitsImages[0]),len(fitsImages[0][0])]
    print('LINT will now make sure that all of the flat images have the same dimensions.')
    print('Dimension of first image is: ', dimensions)
    print('Removing all images that do not have dimensions: ', dimensions)
    #check dimensions
    for ii in range(len(fitsImages)-1):
        