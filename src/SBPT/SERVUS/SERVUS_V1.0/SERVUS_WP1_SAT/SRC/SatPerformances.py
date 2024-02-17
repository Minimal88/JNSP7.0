#!/usr/bin/env python

########################################################################
# SatPerformances.py:
# This function is the Main Function of SAT Module
#
#  Project:        SBPT
#  File:           SatPerformances.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
# Usage:
# i.e: SatPerformances.py $SCEN_PATH
# 
# Internal dependencies:
#   SatFunctions.py
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
from COMMON.Dates import convertYearMonthDay2JulianDay
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy
from SatFunctions import computeSatStats, readDataFile
from SatStatistics import SatStatsIdx, SatStatsTimeIdx, SatInfoIdx
from collections import OrderedDict
import WP1Plots  as wp1Plot
from yaml import dump
import sys, os


#----------------------------------------------------------------------
# INTERNAL FUNCTIONS
#----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide path to SCENARIO as a unique argument\n")

# Function to read the configuration file
def readConf(CfgFile):
    Conf = OrderedDict({})
    with open(CfgFile, 'r') as f:
        # Read file
        Lines = f.readlines()

        # Read each configuration parameter which is compound of a key and a value
        for Line in Lines:
            if "#" in Line: continue
            if not Line.strip(): continue
            LineSplit = Line.split('=')
            try:
                LineSplit = list(filter(None, LineSplit))
                Conf[LineSplit[0].strip()] = LineSplit[1].strip()

            except:
                sys.stderr.write("ERROR: Bad line in conf: %s\n" % Line)

    return Conf

def processConf(Conf):
    ConfCopy = Conf.copy()
    for Key in ConfCopy:
        Value = ConfCopy[Key]
        if Key == "INI_DATE" or Key == "END_DATE":
            ParamSplit = Value.split('/')

            # Compute Julian Day
            Conf[Key + "_JD"] = \
                int(round(
                    convertYearMonthDay2JulianDay(
                        int(ParamSplit[2]),
                        int(ParamSplit[1]),
                        int(ParamSplit[0]))
                    )
                )

    return Conf

#######################################################
# MAIN BODY
#######################################################

# Check Input Arguments
if len(sys.argv) != 2:
    displayUsage()
    sys.exit()

# Extract the arguments
Scen = sys.argv[1]

# Select the conf file name
CfgFile = Scen + '/CFG/satperformances.cfg'

# Read conf file
Conf = readConf(CfgFile)
#print(dump(Conf))

# Process Configuration Parameters
Conf = processConf(Conf)

# Print 
print('------------------------------------')
print('--> RUNNING SAT-PERFORMANCE ANALYSIS:')
print('------------------------------------')

# Loop over Julian Days in simulation
#-----------------------------------------------------------------------
for Jd in range(Conf["INI_DATE_JD"], Conf["END_DATE_JD"] + 1):

    # Compute Year, Month and Day in order to build input file name
    Year, Month, Day = convertJulianDay2YearMonthDay(Jd)
    
    # Estimate the Day of Year DOY
    Doy = convertYearMonthDay2Doy(Year, Month, Day)
    yearDayText = 'Y%02dD%03d' % (Year % 100, Doy)

    # Define the full path and name to the SAT INFO file to read
    SatInfoFilePath = Scen + \
        '/OUT/SAT/' + 'SAT_INFO_%s_G123_%ss.dat' % \
            (yearDayText, Conf["TSTEP"])

    # Define the name of the ENT-GPS instantaneous file
    EntGpsFilePath = Scen + \
        '/OUT/SAT/' + 'ENTGPS_%s_G123_%ss.dat' % \
            (yearDayText, Conf["TSTEP"])
    
    # Define the name of the RIMS file
    RimsFilePath = Scen + \
        '/INP/RIMS/' + 'RIMS_REF_POSITIONS_%s.dat' % \
            (Year)

    # Define the name of the Output file Statistics
    SatStatsFile = SatInfoFilePath.replace("INFO", "STAT")

    # Display Message
    print('\n*** Processing Day of Year: ', Doy, '...***')

    # Display Message
    print('1. Processing file:', SatInfoFilePath)
    
    # T3. Compute Satellite Statistics  FILE
    computeSatStats(SatInfoFilePath, EntGpsFilePath, SatStatsFile)

    # Display Creation message
    print('2. Created files:','\n', SatStatsFile,'\n', EntGpsFilePath)
    
    # Display Reading Message
    print('3. Reading file:', SatStatsFile)    
    # Read Statistics file    
    satStatsData = readDataFile(SatStatsFile, SatStatsIdx.values())

    # Display Reading Message
    print('4. Reading file:', SatInfoFilePath)
    # Read Sat Info file    
    satStatsTimeData = readDataFile(EntGpsFilePath, SatStatsTimeIdx.values())

    # Display Generating figures Message
    print('5. Generating Figures...\n')
    
    # T4. Generate Satellite RIMS figures   
    wp1Plot.plotRims(RimsFilePath, yearDayText)
    
    # T5. Generate Satellite Statistics figures   
    wp1Plot.plotSatStats(satStatsData, yearDayText)
    
    # T6. Generate Satellite Time and Info figures    
    wp1Plot.plotSatStatsTime(satStatsTimeData, SatInfoFilePath, yearDayText)


print('------------------------------------')
print('--> END OF SAT-PERFORMANCE ANALYSIS:')
print('------------------------------------')

print('Check figures at the Output folder /OUT/SAT/FIGURES/')


#######################################################
#END OF SAT PERFORMANCES MODULE
#######################################################
