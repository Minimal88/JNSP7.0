#!/usr/bin/env python

########################################################################
# SatPerformances.py:
# This function is the Main Function of SAT Module
#
#  Project:        SBPT
#  File:           SatPerformances.py
#  Date(YY/MM/DD): 24/02/19
#
#   Author: Esteban Martinez Valvere
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
#   COMMON
#   SatFunctions
#   SatStatistics
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
# Add path to find all modules
import sys, os
projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, projectDir)
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy
from COMMON.Files import readDataFile, readConf, processConf
from SatFunctions import computeSatStats
from SatStatistics import SatStatsIdx, SatStatsTimeIdx
import WP1Plots  as wp1Plot
import sys, os


#----------------------------------------------------------------------
# INTERNAL FUNCTIONS
#----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide path to SCENARIO as a unique argument\n")

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
