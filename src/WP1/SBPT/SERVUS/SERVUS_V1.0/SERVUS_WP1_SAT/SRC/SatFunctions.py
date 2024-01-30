#!/usr/bin/env python

########################################################################
# SatFunctions.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatFunctions.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON import GnssConstants
from math import sqrt
import numpy as np

# Define SAT INFO FILE Columns
SatInfoIdx = OrderedDict({})
SatInfoIdx["SoD"]=0
SatInfoIdx["DOY"]=1
SatInfoIdx["PRN"]=2
SatInfoIdx["SAT-X"]=3
SatInfoIdx["SAT-Y"]=4
SatInfoIdx["SAT-Z"]=5
SatInfoIdx["MONSTAT"]=6
SatInfoIdx["SRESTAT"]=7
SatInfoIdx["SREx"]=8
SatInfoIdx["SREy"]=9
SatInfoIdx["SREz"]=10
SatInfoIdx["SREb1"]=11
SatInfoIdx["SREW"]=12
SatInfoIdx["SFLT-W"]=13
SatInfoIdx["UDREI"]=14
SatInfoIdx["FC"]=15
SatInfoIdx["AF0"]=16
SatInfoIdx["AF1"]=17
SatInfoIdx["LTCx"]=18
SatInfoIdx["LTCy"]=19
SatInfoIdx["LTCz"]=20
SatInfoIdx["NRIMS"]=21
SatInfoIdx["RDOP"]=22

# Define SAT STATISTICS file Columns
SatStatsIdx = OrderedDict({})
SatStatsIdx["PRN"]=0
SatStatsIdx["MON"]=1
SatStatsIdx["RIMS-MIN"]=2
# SatStatsIdx["RIMS-MAX"]=3
# SatStatsIdx["SREaRMS"]=4
# SatStatsIdx["SREcRMS"]=5
# SatStatsIdx["SRErRMS"]=6
# SatStatsIdx["SREbRMS"]=7
# SatStatsIdx["SREWRMS"]=8
# SatStatsIdx["SREWMAX"]=9
# SatStatsIdx["SFLTMAX"]=10
# SatStatsIdx["SFLTMIN"]=11
# SatStatsIdx["SIMAX"]=12
# SatStatsIdx["FCMAX"]=13
# SatStatsIdx["LTCbMAX"]=14
# SatStatsIdx["LTCxMAX"]=15
# SatStatsIdx["LTCyMAX"]=16
# SatStatsIdx["LTCzMAX"]=17
# SatStatsIdx["NMI"]=18
# SatStatsIdx["NTRANS"]=19

# FUNCTION: Display Message
#-----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")


# FUNCTION: Split line
#-----------------------------------------------------------------------

def splitLine(Line):
    LineSplit = Line.split()

    return LineSplit


# FUNCTION: Read Sat Info Epoch
#-----------------------------------------------------------------------

def readSatInfoEpoch(f):
    EpochInfo = []
    
    # Read one line
    Line = f.readline()
    if(not Line):
        return []
    LineSplit = splitLine(Line)
    Sod = LineSplit[SatInfoIdx["SoD"]]
    SodNext = Sod

    while SodNext == Sod:
        EpochInfo.append(LineSplit)
        Pointer = f.tell()
        Line = f.readline()
        LineSplit = splitLine(Line)
        try: 
            SodNext = LineSplit[SatInfoIdx["SoD"]]

        except:
            return EpochInfo

    f.seek(Pointer)

    return EpochInfo

# FUNCTION: Initialized Output Statistics
#-----------------------------------------------------------------------

def initializeOutputs(Outputs):
    
    # Loop over GPS and Galileo Satellites
    for Const in ['G', 'E']:
        
        # Loop over all satelliteds of each constellation 
        for Prn in range(1,33):
            SatLabel = Const + "%02d" % Prn
            
            Outputs[SatLabel] = OrderedDict({})
            for var in SatStatsIdx.keys():
                
                if (var == "PRN"):
                    Outputs[SatLabel][var] = SatLabel
                
                elif (var == "RIMS-MIN"):
                    Outputs[SatLabel][var] = 1e12

                else:
                    Outputs[SatLabel][var] = 0.0

# FUNCTION: Initialize Intermediate Outputs
#-----------------------------------------------------------------------

def initializeInterOutputs(InterOutputs):
    
    # Loop over GPS and Galileo Satellites
    for Const in ['G', 'E']:
        
        for Prn in range(1,33):
            
            SatLabel = Const + "%02d" % Prn
            InterOutputs[SatLabel] = OrderedDict({})
            InterOutputs[SatLabel]["NSAMPS"] = 0
            InterOutputs[SatLabel]["SODPREV"] = 0
            InterOutputs[SatLabel]["MONPREV"] = 0
            InterOutputs[SatLabel]["SREb"] = 0
            InterOutputs[SatLabel]["SREbSUM2"] = 0
            InterOutputs[SatLabel]["SREaSUM2"] = 0
            InterOutputs[SatLabel]["SREcSUM2"] = 0
            InterOutputs[SatLabel]["SRErSUM2"] = 0
            InterOutputs[SatLabel]["SREACRSAMPS"] = 0
            InterOutputs[SatLabel]["SREWSUM2"] = 0
            InterOutputs[SatLabel]["SREWSAMPS"] = 0
            InterOutputs[SatLabel]["XPREV"] = 0
            InterOutputs[SatLabel]["YPREV"] = 0
            InterOutputs[SatLabel]["ZPREV"] = 0

    InterOutputs["ENT-GPS"] = 0

    return

# FUNCTION: Project a vector into a given direction
def projectVector(Vector, Direction):
    
    # Compute the Unitary Vector
    UnitaryVector = Direction / np.linalg.norm(Direction)

    return Vector.dot(UnitaryVector)

# FUNCTION: Estimate SRE-Along/Cross/Radial
#-----------------------------------------------------------------------

def computeSreAcr(DeltaT, PosPrev, Pos, Sre):

    # Compute Velocity computation deriving the position
    
    
    # Add Earth's Rotation Effect on the Reference frame
    

    # Compute unitary vectors
    

    # Compute SRE in ACR frame by projecting the SRE in XYZ
    SreA = 0.0;
    SreC = 0.0;
    SreR = 0.0;

    return SreA, SreC, SreR

# FUNCTION: Update Statistics Information
#-----------------------------------------------------------------------

def updateEpochStats(SatInfo, InterOutputs, Outputs):
    
    # Extract PRN Column
    sat = SatInfo[SatInfoIdx["PRN"]]

    # Add Number of samples
    InterOutputs[sat]["NSAMPS"] = InterOutputs[sat]["NSAMPS"] + 1

    ### IF SATELLITE IS MONITORED:
    if(SatInfo[SatInfoIdx["MONSTAT"]] == '1'):

        # Add Satellite Monitoring if Satellite is Monitored
        Outputs[sat]["MON"] = Outputs[sat]["MON"] + 1

        ### IF SRE_STATUS IS OK:
        if(SatInfo[SatInfoIdx["SRESTAT"]] == '1'):
    
            # Update number of samples Monitored & SRE OK
            InterOutputs[sat]["SREWSAMPS"] = InterOutputs[sat]["SREWSAMPS"] + 1


            # Update the Minimum Number of RIMS in view        
            if( int(SatInfo[SatInfoIdx["NRIMS"]])<Outputs[sat]["RIMS-MIN"]):
                Outputs[sat]["RIMS-MIN"] = int(SatInfo[SatInfoIdx["NRIMS"]])


        #End of if(SatInfo[SatIdx["SRESTAT"]] == '1'):

    #End of if(SatInfo[SatIdx["MONSTAT"]] == '1'):

    # KEEP CURRENT INFORMATION FOR NEXT EPOCH

    # Keep Current Monitoring Status
    InterOutputs[sat]["MONPREV"] = int(SatInfo[SatInfoIdx["MONSTAT"]])


# END OF FUNCTION: def updateEpochStats(SatInfo, InterOutputs, Outputs):


# FUNCTION: Compute the final Statistics
#-----------------------------------------------------------------------
def computeFinalStatistics(InterOutputs, Outputs):
    for sat in Outputs.keys():

        # Estimate the Monitoring Percentage
        if(InterOutputs[sat]["NSAMPS"] != 0):

            # Monitoring percentage = Monitored epochs / Total epochs
            Outputs[sat]["MON"] = Outputs[sat]["MON"] * 100.0 / InterOutputs[sat]["NSAMPS"]

# END OF FUNCTION: def computeFinalStatistics(InterOutputs, Outputs):


# FUNCTION: Function to compute the Satellite Statistics
#-----------------------------------------------------------------------

def computeSatStats(satFile, EntGpsFile, satStatsFile):
    
    # Initialize Variables
    EndOfFile = False
    EpochInfo = []

    # Open SAT INFO file
    with open(satFile, 'r') as fsat:
        
        # Read header line of Sat Information file
        fsat.readline()

        # Open ENT-GPS Offset output file
        with open(EntGpsFile, 'w') as fEntGps:

            # Write Header of Output files
            fEntGps.write("#SOD\tENT-GPS\n")

            # Open Output File Satellite Statistics file
            with open(satStatsFile, 'w') as fOut:
                
                # Write Header of Output files
                fOut.write("#PRN  MON minRIMS\n")

                # Define and Initialize Variables            
                Outputs = OrderedDict({})
                InterOutputs = OrderedDict({})
                
                # Initialize Outputs
                initializeOutputs(Outputs)
                initializeInterOutputs(InterOutputs)

                # LOOP over all Epochs of SAT INFO file
                # ----------------------------------------------------------
                while not EndOfFile:
                    
                    # Read Only One Epoch
                    EpochInfo = readSatInfoEpoch(fsat)
                    
                    # If EpochInfor is not Null
                    if EpochInfo != []:
                        # Compute SRE b
                        ent_gps = computeENTGPS(EpochInfo, InterOutputs)

                        # Write ENT-GPS Offset file
                        fEntGps.write("%5s %10.4f\n" % \
                            (
                                EpochInfo[0][SatInfoIdx["SoD"]],
                                ent_gps,

                            ))

                        # Loop over all Satellites Information in Epoch
                        # --------------------------------------------------
                        for SatInfo in EpochInfo:
                            
                            # Update the Output Statistics
                            updateEpochStats(SatInfo, InterOutputs, Outputs)
                            
                        #End of for SatInfo in EpochInfo:
                                            
                    # end if EpochInfo != []:
                    else:
                        EndOfFile = True

                    #End of if EpochInfo != []:
                    
                # End of while not EndOfFile:

                # Compute the final Statistics
                # ----------------------------------------------------------
                computeFinalStatistics(InterOutputs, Outputs)
                
                # Write Statistics File
                # ----------------------------------------------------------
                
                # Define Output file format
                Format = "%s %6.2f %4d "
                FormatList = Format.split()

                for sat in Outputs.keys():
                    
                    # Remove 0% monitored satellites because we're not interested in them
                    if(Outputs[sat]["MON"] != 0):
                        
                        for i, result in enumerate(Outputs[sat]):
                            fOut.write(((FormatList[i] + " ") % Outputs[sat][result]))

                        fOut.write("\n")

                        # End of for i, result in enumerate(Outputs[sat]):
                    # End of if(Outputs[sat]["MON"] != 0):
                # End of for sat in Outputs.keys():
            # End of with open(satStatsFile, 'w') as fOut:
        # End of with open(EntGpsFile, 'w') as fEntGps:
    # End of with open(satFile, 'r') as f:

#End of def computeSatStats(satFile, satStatsFile):


def computeENTGPS(epoch_info, inter_outputs):
    """
    Compute the ENT-GPS Offset: estimated from the SRE of the monitored satellites with SRE_STATUS OK 
    and the SREb (Satellite Residual Error Clock component).

    Parameters:
    - epoch_info: Information for all satellites in a single epoch.
    - inter_outputs: Intermediate outputs to store computed values.

    Updates inter_outputs in-place.
    """
    
    # Initialize lists to store radial component of SRE vector for each satellite
    sre_b_minus_r_list = []

    for sat_info in epoch_info:
        prn = sat_info[SatInfoIdx["PRN"]]
        
        sreStatus = sat_info[SatInfoIdx["SRESTAT"]]
        
        # Consider only SRE STATUS == 1
        if (sreStatus=='0'): 
            continue

        # Get the SREb1 from the Sat Info file (Satellite Residual Error Clock Bias)
        sreb1 = float(sat_info[SatInfoIdx["SREb1"]])

        # Store intermediate output
        inter_outputs[prn]["SREb"] = sreb1

        # Get the Components of the SRE vector
        sre_x = float(sat_info[SatInfoIdx["SREx"]])
        sre_y = float(sat_info[SatInfoIdx["SREy"]])
        sre_z = float(sat_info[SatInfoIdx["SREz"]])

        # Get the Position vector of the satellite
        sat_x = float(sat_info[SatInfoIdx["SAT-X"]])
        sat_y = float(sat_info[SatInfoIdx["SAT-Y"]])
        sat_z = float(sat_info[SatInfoIdx["SAT-Z"]])

        # Calculate the unit vector in the radial direction
        sre_vector = np.array([sre_x, sre_y, sre_z])
        sat_vector = np.array([sat_x, sat_y, sat_z])
        
        # Calculate the radial component of the SRE vector        
        radial_component = projectVector(sre_vector, sat_vector)

        sre_b_minus_r = sreb1 - radial_component 
        
        # Append ENT-GPS to the list for later computation
        sre_b_minus_r_list.append(sre_b_minus_r)

     # Compute ENT-GPS as the median of (SREb1 - RadialComponent) for all satellites
    ent_gps = np.median(sre_b_minus_r_list)

    return ent_gps

    # Update inter_outputs with computed SREb
    


    
########################################################################
#END OF SAT FUNCTIONS MODULE
########################################################################
