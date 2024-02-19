#!/usr/bin/env python

########################################################################
# SBPT/SRC/IgpPerformances.py:
# This function is the Main Function of IGP PERF Module
#
#  Project:        SBPT/SERVUS
#  File:           IgpPerforamnces.py
#  Date(YY/MM/DD): 24/02/19
#
#   Author: Esteban Martinez Valvere
#   Copyright 2021 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
# Usage:
# i.e: IgpPerformances $SCEN_PATH

# Internal dependencies:
#   COMMON
########################################################################

# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, projectDir)
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy
from COMMON.Files import readDataFile, readConf, processConf
from IgpFunctions import computeIgpStats


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
CfgFile = Scen + '/CFG/igpperformances.cfg'

# Read conf file
Conf = readConf(CfgFile)
#print(dump(Conf))

# Process Configuration Parameters
Conf = processConf(Conf)

# Print 
print('------------------------------------')
print('--> RUNNING IGP-PERFORMANCE ANALYSIS:')
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
    IgpInfoFilePath = Scen + \
        '/OUT/IGP/' + 'IGP_INFO_%s_G123_%ss.dat' % \
            (yearDayText, Conf["TSTEP"])

    # Define the name of the RIMS file
    RimsFilePath = Scen + \
        '/INP/RIMS/' + 'RIMS_REF_POSITIONS_%s.dat' % \
            (Year)

    # Define the name of the Output file Statistics
    IgpStatsFile = IgpInfoFilePath.replace("INFO", "STAT")

    # Display Message
    print('\n*** Processing Day of Year: ', Doy, '...***')

    # Display Message
    print('1. Processing file:', IgpInfoFilePath)
    
    # T1. Compute IGP Statistics and generate file
    computeIgpStats(IgpInfoFilePath, IgpStatsFile)






#####################################################################
#END OF IGP PERFORMANCES MODULE
#######################################################
