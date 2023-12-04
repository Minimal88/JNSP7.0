#!/usr/bin/env python

## Copyright (C) GNSS ACADEMY 
##
## Name          : receiver_analysis.py
## Purpose       : WP0 Takss: Plot Receiver SPP Analyses
## Project       : WP0-JSNP
## Component     : 
## Author        : GNSS Academy
## Creation date : 2021
## File Version  : 1.0
##

import sys, os

# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)

from collections import OrderedDict
from interfaces import LOS_IDX, POS_IDX
from pandas import read_csv
from yaml import dump
import SatFunctions
import IonoFunctions
import TropoFunctions
import MeasFunctions
import PosFunctions

#######################################################
# INTERNAL FUNCTIONS 
#######################################################

def displayUsage():
    sys.stderr.write("ERROR: Please provide path to SCENARIO as a unique \nargument\n")

def readConf(CfgFile):
    Conf = OrderedDict({})
    with open(CfgFile, 'r') as f:
        # Read file
        Lines = f.readlines()

        # Read each configuration parameter which is compound of a key and a value
        for Line in Lines:
            if "#" in Line or Line.isspace(): continue
            LineSplit = Line.split('=')
            try:
                LineSplit = list(filter(None, LineSplit))
                Conf[LineSplit[0].strip()] = LineSplit[1].strip()

            except:
                sys.stderr.write("ERROR: Bad line in conf: %s\n" % Line)

    return Conf

#######################################################
# MAIN PROCESSING
#######################################################

print( '-----------------------------')
print( 'RUNNING RECEIVER ANALYSES ...')
print( '-----------------------------')

if len(sys.argv) != 2:
    displayUsage()
    sys.exit()

# Take the arguments
Scen = sys.argv[1]

# Path to conf
CfgFile = Scen + '/CFG/receiver_analysis.cfg'

# Read conf file
Conf = readConf(CfgFile)

# Print 
print('Reading Configuration file',CfgFile)

#print(dump(Conf))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>> LOS FILE ANALYSES
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Get LOS file full path
LosFile = Scen + '/OUT/LOS/' + Conf["LOS_FILE"]
PosFile = Scen + '/OUT/POS/' + Conf["POS_FILE"]


#-----------------------------------------------------------------------
# PLOT SATELLITE ANALYSES
#-----------------------------------------------------------------------

# T2.1 Plot Satellite Visibility figures
if(Conf["PLOT_SATVIS"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["PRN"],LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellite Visibility image Periods ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatVisibility(PosData)

# T2.2 Plot Satellite Geometrical Ranges figures
if(Conf["PLOT_SATRNG"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["RANGE[m]"],LOS_IDX["ELEV"]])

    print( 'Ploting the Satellite Geometrical image Ranges ...')
    
    # Configure plot and call plot generation function
    SatFunctions.plotSatGeomRnge(PosData)

# T2.3 Plot Satellite Tracks figures
if(Conf["PLOT_SATTRK"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],
    LOS_IDX["SAT-X[m]"],
    LOS_IDX["SAT-Y[m]"],
    LOS_IDX["SAT-Z[m]"],
    LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellite Tracks image ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatTracks(PosData)

# 2.4 Plot Satellite Velocity figures
if(Conf["PLOT_SATVEL"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],
    LOS_IDX["PRN"],
    LOS_IDX["VEL-X[m/s]"],
    LOS_IDX["VEL-Y[m/s]"],
    LOS_IDX["VEL-Z[m/s]"],
    LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellite Velocities image ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatVelocities(PosData)

# T2.5 NAV Satellite Clock
if(Conf["PLOT_SATCLK"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["SV-CLK[m]"],LOS_IDX["ELEV"],LOS_IDX["PRN"]])
    
    print( 'Ploting the Satellite Clock image ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatClock(PosData)

#T2.6 Satellite Clock
if(Conf["PLOT_SAT_CORRECTEDCLK"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["SV-CLK[m]"],LOS_IDX["DTR[m]"],LOS_IDX["TGD[m]"],LOS_IDX["PRN"]])
    
    print( 'Ploting the Satellite Corrected image Clock ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatCorrectedClock(PosData)

# T2.7 Satellite TGD
if(Conf["PLOT_SATTGD"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["TGD[m]"],LOS_IDX["PRN"]])
    
    print( 'Ploting the Satellite TGD image ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatTGD(PosData)

# T2.8 Satellite DTR
if(Conf["PLOT_SATDTR"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["DTR[m]"],LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellite DTR image ...')

    # Configure plot and call plot generation function
    SatFunctions.plotSatDTR(PosData)

# T3.1 STEC vs TIME (ELEV)
if(Conf["PLOT_IONO_STEC_ELEV"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["STEC[m]"],LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellite STEC vs TIME (ELEV) image ...')

    # Configure plot and call plot generation function
    IonoFunctions.plotSatIonoStecElev(PosData)

# T3.2 PRN vs TIME (STEC)
if(Conf["PLOT_IONO_PRN_STEC"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["STEC[m]"],LOS_IDX["PRN"]])
    
    print( 'Ploting the Satellites PRN vs TIME (STEC) image ...')

    # Configure plot and call plot generation function
    IonoFunctions.plotSatIonoPrnStec(PosData)

# T3.3 VTEC vs. Time
if(Conf["PLOT_IONO_VTEC_TIME"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["VTEC[m]"],LOS_IDX["ELEV"]])
    
    print( 'Ploting the Satellites VTEC vs TIME (Elev) image ...')

    # Configure plot and call plot generation function
    IonoFunctions.plotSatIonoVtecTimeElev(PosData)
    
# T3.4 PRN vs. TIME (VTEC)
if(Conf["PLOT_IONO_PRN_VTEC"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["VTEC[m]"],LOS_IDX["PRN"]])
    
    print( 'Ploting the Satellites PRN vs TIME (VTEC) image ...')

    # Configure plot and call plot generation function
    IonoFunctions.plotSatIonoPrnVtec(PosData)

# T4.1 STD vs. Time (Elevation)
if(Conf["PLOT_TROPO_STD_ELEV"] == '1'):
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["TROPO[m]"],LOS_IDX["ELEV"]])
    
    print( 'Ploting the Slant Tropospheric Delay (STD) image ...')

    # Configure plot and call plot generation function
    TropoFunctions.plotSatTropoStdElev(PosData)

# T4.2 ZTD vs. Time (Elevation)
if(Conf["PLOT_TROPO_ZTD_ELEV"] == '1'): #TODO: Fix this plot
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["TROPO[m]"],LOS_IDX["ELEV"],LOS_IDX["MPP[elev]"]])
    
    print( 'Ploting the Zenith Tropo Delay (ZTD) image ...')

    # Configure plot and call plot generation function
    TropoFunctions.plotSatTropoZtdElev(PosData)

# T5.1 PSR vs Time
if(Conf["PLOT_MSR_PSR_ELEV"] == '1'): 
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["MEAS[m]"],LOS_IDX["ELEV"]])
    
    # Configure plot and call plot generation function
    MeasFunctions.plotSatMeasPsrElev(PosData)

# T5.2 TAU vs Time
if(Conf["PLOT_MSR_TAU_ELEV"] == '1'): 
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["MEAS[m]"],LOS_IDX["ELEV"]])
    
    # Configure plot and call plot generation function
    MeasFunctions.plotSatMeasTauElev(PosData)

# T5.3 ToF vs Time
if(Conf["PLOT_MSR_TOF_ELEV"] == '1'): 
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],LOS_IDX["TOF[ms]"],LOS_IDX["ELEV"]])
    
    # Configure plot and call plot generation function
    MeasFunctions.plotSatMeasTofElev(PosData)

# T5.4 Doppler Frequency
if(Conf["PLOT_MSR_DOPPLER_ELEV"] == '1'): 
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],
             LOS_IDX["SAT-X[m]"],
             LOS_IDX["SAT-Y[m]"],
             LOS_IDX["SAT-Z[m]"],
             LOS_IDX["VEL-X[m/s]"],
             LOS_IDX["VEL-Y[m/s]"],
             LOS_IDX["VEL-Z[m/s]"],
             LOS_IDX["ELEV"]])

    # Get Receiver coordinates from Configuration file
    X_RCVR = float(Conf["X_RCVR"])
    Y_RCVR = float(Conf["Y_RCVR"])
    Z_RCVR = float(Conf["Z_RCVR"])

    # Configure plot and call plot generation function
    MeasFunctions.plotSatMeasDopplerElev(PosData, X_RCVR, Y_RCVR, Z_RCVR)

# T5.5 Residuals C1
if(Conf["PLOT_MSR_RESIDUALS_ELEV"] == '1'): 
    # Read the cols we need from LOS file
    PosData = read_csv(LosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[LOS_IDX["SOD"],
             LOS_IDX["MEAS[m]"],
             LOS_IDX["RANGE[m]"],             
             LOS_IDX["SV-CLK[m]"],
             LOS_IDX["VTEC[m]"],
             LOS_IDX["TROPO[m]"],             
             LOS_IDX["TGD[m]"], 
             LOS_IDX["DTR[m]"], 
             LOS_IDX["PRN"]])
    
    # Configure plot and call plot generation function
    MeasFunctions.plotSatMeasResidualsElev(PosData)

# T6.1. Satellites Used in PVT
if(Conf["PLOT_POS_NUM_SAT"] == '1'): #TODO: Fix this plot Configuration
    # Read the cols we need from LOS file
    PosData = read_csv(PosFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[POS_IDX["SOD"],
             POS_IDX["NSATS"]])
    
    # Configure plot and call plot generation function
    PosFunctions.plotNumberOfSats(PosData)

