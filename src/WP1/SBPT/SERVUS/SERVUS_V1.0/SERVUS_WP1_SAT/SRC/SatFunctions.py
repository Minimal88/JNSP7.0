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
SatIdx = OrderedDict({})
SatIdx["SoD"]=0
SatIdx["DOY"]=1
SatIdx["PRN"]=2
SatIdx["SAT-X"]=3
SatIdx["SAT-Y"]=4
SatIdx["SAT-Z"]=5
SatIdx["MONSTAT"]=6
SatIdx["SRESTAT"]=7
SatIdx["SREx"]=8
SatIdx["SREy"]=9
SatIdx["SREz"]=10
SatIdx["SREb1"]=11
SatIdx["SREW"]=12
SatIdx["SFLT-W"]=13
SatIdx["UDREI"]=14
SatIdx["FC"]=15
SatIdx["AF0"]=16
SatIdx["AF1"]=17
SatIdx["LTCx"]=18
SatIdx["LTCy"]=19
SatIdx["LTCz"]=20
SatIdx["NRIMS"]=21
SatIdx["RDOP"]=22

# Define SAT STATISTICS file Columns
SatStatsIdx = OrderedDict({})
SatStatsIdx["PRN"]=0
SatStatsIdx["MON"]=1
SatStatsIdx["RIMS-MIN"]=2

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
    Sod = LineSplit[SatIdx["SoD"]]
    SodNext = Sod

    while SodNext == Sod:
        EpochInfo.append(LineSplit)
        Pointer = f.tell()
        Line = f.readline()
        LineSplit = splitLine(Line)
        try: 
            SodNext = LineSplit[SatIdx["SoD"]]

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
    sat = SatInfo[SatIdx["PRN"]]

    # Add Number of samples
    InterOutputs[sat]["NSAMPS"] = InterOutputs[sat]["NSAMPS"] + 1

    ### IF SATELLITE IS MONITORED:
    if(SatInfo[SatIdx["MONSTAT"]] == '1'):

        # Add Satellite Monitoring if Satellite is Monitored
        Outputs[sat]["MON"] = Outputs[sat]["MON"] + 1

        ### IF SRE_STATUS IS OK:
        if(SatInfo[SatIdx["SRESTAT"]] == '1'):
    
            # Update number of samples Monitored & SRE OK
            InterOutputs[sat]["SREWSAMPS"] = InterOutputs[sat]["SREWSAMPS"] + 1


            # Update the Minimum Number of RIMS in view        
            if( int(SatInfo[SatIdx["NRIMS"]])<Outputs[sat]["RIMS-MIN"]):
                Outputs[sat]["RIMS-MIN"] = int(SatInfo[SatIdx["NRIMS"]])


        #End of if(SatInfo[SatIdx["SRESTAT"]] == '1'):

    #End of if(SatInfo[SatIdx["MONSTAT"]] == '1'):

    # KEEP CURRENT INFORMATION FOR NEXT EPOCH

    # Keep Current Monitoring Status
    InterOutputs[sat]["MONPREV"] = int(SatInfo[SatIdx["MONSTAT"]])


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
            fEntGps.write("#SOD \n")

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
                        # computeSreb(EpochInfo, InterOutputs)

                        # Write ENT-GPS Offset file
                        fEntGps.write("%5s \n" % \
                            (
                                EpochInfo[0][SatIdx["SoD"]],

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
    
########################################################################
#END OF SAT FUNCTIONS MODULE
########################################################################
