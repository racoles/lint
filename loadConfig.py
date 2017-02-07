'''
@title loadConfig
@author: Rebecca Coles
Updated on Nov 21, 2016

Load variables from LINT.config and insert into dictionary
'''
# Import
import os, ConfigParser
from json import loads

def loadConfig():
#Load config.txt
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = os.path.join(__location__, 'LINT.config');
    configParser.read(configFilePath)
    #Retrieve user specifications from LINT.config and create dictionary
    lintDict = {'fitsPath': configParser.get('fitsDir', 'fitsPath'),
                'ext': int(configParser.get('extension', 'ext')),
                'outputFITS': configParser.get('output', 'outputFITS'),
                'overscanSubtractBOOL': bool(configParser.get('overscan', 'overscanSubtractBOOL')), 
                #'overscanSubtractLocation': int(configParser.get('overscan', 'overscanSubtractLocation')),
                #'overscanRemoveBOOL': bool(configParser.get('overscan', 'overscanRemoveBOOL')), 
                #'overscanTopRows': int(configParser.get('overscan', 'overscanTopRows')),
                #'overscanBottomRows': int(configParser.get('overscan', 'overscanBottomRows')),
                #'overscanLeftColumns': int(configParser.get('overscan', 'overscanLeftColumns')),
                #'overscanRightColumns': int(configParser.get('overscan', 'overscanRightColumns')),
                'overscanRows': loads(configParser.get('overscan', 'overscanRows')),
                'overscanColumns': loads(configParser.get('overscan', 'overscanColumns')),
                'flagLimit': float(configParser.get('SExCuts', 'flagLimit')),
                'fluxLimit': float(configParser.get('SExCuts', 'fluxLimit')),
                'SNRlimit': float(configParser.get('SExCuts', 'SNRlimit')),
                'FWHMlimit': float(configParser.get('SExCuts', 'FWHMlimit')),
                'SExParameterFile': configParser.get('SExParam', 'SExParameterFile')}
    return lintDict