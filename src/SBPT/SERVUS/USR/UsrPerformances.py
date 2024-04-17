#!/usr/bin/env python

########################################################################
# SBPT/SRC/UsrPerformances.py:
# This function is the Main Function of USER PERF Module
#
#  Project:        SBPT
#  File:           UsrPerformances.py
#  Date(YY/MM/DD): 20/07/21
#
#   Author: GNSS Academy
#   Copyright 2022 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
# Usage:
# i.e: UsrPerformances $SCEN_PATH

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
from UsrFunctions import computeUsrPosAndPerf
import WP3Plots  as wp3


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
CfgFile = Scen + '/CFG/usrperformances.cfg'

# Read conf file
Conf = readConf(CfgFile)
#print(dump(Conf))

# Process Configuration Parameters
Conf = processConf(Conf)

# Print 
print('------------------------------------')
print('--> RUNNING USR-PERFORMANCE ANALYSIS:')
print('------------------------------------')

# Loop over Julian Days in simulation
#-----------------------------------------------------------------------
for Jd in range(Conf["INI_DATE_JD"], Conf["END_DATE_JD"] + 1):

    # Compute Year, Month and Day in order to build input file name
    Year, Month, Day = convertJulianDay2YearMonthDay(Jd)
    
    # Estimate the Day of Year DOY
    Doy = convertYearMonthDay2Doy(Year, Month, Day)
    yearDayText = 'Y%02dD%03d' % (Year % 100, Doy)

    # Define the full path and name to the LOS INFO file to read
    UsrLosFilePath = Scen + \
        '/OUT/USR/LOS/' + 'LOS_INFO_%s_G123_%ss.dat' % \
            (yearDayText, Conf["LOS_TSTEP"])

    # Define the name of the POS Output file
    UsrPosFilePath = UsrLosFilePath.replace("LOS", "POS")

    # Define the name of the POS Output file
    UsrPerfFilePath = UsrLosFilePath.replace("LOS", "PERF")
    UsrPerfFilePath = UsrPerfFilePath.replace("INFO", "APVI")

    print('\n*** Processing Day of Year: ', Doy, '...***')
    
    print('1. Processing file: ', UsrLosFilePath)
    
    # T1. Compute USR Statistics and generate file
    computeUsrPosAndPerf(UsrLosFilePath, UsrPosFilePath, UsrPerfFilePath)
    
    print('2. Created file:', UsrPosFilePath) 

    print('3. Generating Figures...\n')
    
    # T2. Generate USR Statistic Maps figures   
    wp3.plotUsrStatsMaps(UsrPosFilePath, yearDayText)
    
    # T3. Generate USR Time figures     
    wp3.plotUsrInfoTime(UsrLosFilePath, yearDayText)   
    




#####################################################################
#END OF USR PERFORMANCES MODULE
#######################################################
