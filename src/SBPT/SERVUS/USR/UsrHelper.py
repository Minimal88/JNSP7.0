#!/usr/bin/env python

########################################################################
# UsrHelper.py:
# This script defines all internal functions of UsrPerformance Module
#
#  Project:        SBPT
#  File:           UsrHelper.py
#  Date(YY/MM/DD): 24/03/19
#
#   Author: Esteban Martinez Valvere
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
from collections import OrderedDict
from COMMON.Plots import generatePlot
from COMMON import GnssConstants
from math import sqrt
import numpy as np
import sys

# Define USR LOS INFO FILE Columns
UsrLosIdx = dict([
    ("SOD", 0),
    ("DOY", 1),
    ("USER-ID", 2),
    ("ULON", 3),
    ("ULAT", 4),
    ("FLAG", 5),
    ("SYSID", 6),
    ("PRN", 7),
    ("ELEV", 8),
    ("AZIM", 9),
    ("IPPLON", 10),
    ("IPPLAT", 11),
    ("RERROR1", 12),
    ("UERE1", 13),
    ("SI1", 14),
    ("RERROR", 15),
    ("UERE", 16),
    ("SI", 17),
    ("SREU", 18),
    ("UDREI", 19),
    ("SFLT", 20),
    ("STROPOE", 21),
    ("SIGMTROPO", 22),
    ("AIRERR", 23),
    ("SIGMAIR", 24),
    ("UISDE", 25),
    ("UIRE", 26),
    ("UISD", 27),
    ("SIGMAMP", 28),
    ("SIGMANOISE", 29),
])

# Define User Pos file Columns
UsrPosIdx = dict([
    ("SOD", 0),
    ("USER-ID", 1),
    ("ULON", 2),
    ("ULAT", 3),
    ("SOL-FLAG", 4),
    ("NVS-5", 5),
    ("NVS-PA", 6),
    ("HPE", 7),
    ("VPE", 8),
    ("HPL", 9),
    ("VPL", 10),
    ("HSI", 11),
    ("VSI", 12),
    ("HDOP", 13),
    ("VDOP", 14),
    ("PDOP", 15)    
])

# Define Usr POS file format list
UsrPosOutputFormat = "%7d %6d %10.3f %10.3f %7d %9d %10d %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f"
PosFileOutputFormatList = UsrPosOutputFormat.split()

# Define User Performance file Columns
UsrPerfIdx = dict([
    ("USER-ID", 0),
    ("ULON", 1),
    ("ULAT", 2),
    ("TOTALSAMP", 3),
    ("NVS-MIN", 4),
    ("NVS-MAX", 5),
    ("SAMP-AVL ", 6),
    ("AVAILABILITY", 7),
    ("HPE-RMS", 8),
    ("VPE-RMS", 9),
    ("HPE-95", 10),
    ("VPE-95", 11),
    ("HPE-MAX", 12),
    ("VPE-MAX", 13),
    ("HSI-MAX", 14),
    ("VSI-MAX", 15),
    ("HPL-MAX", 16),
    ("VPL-MAX", 17),
    ("HPL-MIN", 18),
    ("VPL-MIN", 19),
    ("HDOP-MAX", 20),
    ("VDOP-MAX", 21),
    ("PDOP-MAX", 22)
])

# Define Satidistics Output file format list
UsrPerfOutputFormat = "%d %f %f %d %d %d %d %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f"
PerfFileOutputFormatList =UsrPerfOutputFormat.split()

delim = " "


def splitLine(Line):
    """
    # FUNCTION: Split line
    """
    LineSplit = Line.split()

    return LineSplit

def readUsrLosEpoch(f):
    """
    FUNCTION: Read Usr Los Epoch
    """
    EpochUsrLos = []
    
    # Read one line
    Line = f.readline()
    if(not Line):
        return []
    LineSplit = splitLine(Line)
    Sod = LineSplit[UsrLosIdx["SOD"]]
    SodNext = Sod

    while SodNext == Sod:
        EpochUsrLos.append(LineSplit)
        Pointer = f.tell()
        Line = f.readline()
        LineSplit = splitLine(Line)
        try: 
            SodNext = LineSplit[UsrLosIdx["SOD"]]

        except:
            return EpochUsrLos

    f.seek(Pointer)

    return EpochUsrLos

def initializePosOutputs(PosOutputs):    
    # Loop over all 294 USRs of the GRID
    for usrId in range(1,294):            
        PosOutputs[usrId] = OrderedDict({})
        for var in UsrPosIdx.keys():                
            if (var == "USER-ID"):
                PosOutputs[usrId][var] = int(usrId)            
            else:
                PosOutputs[usrId][var] = 0.0

def initializePerfOutputs(PerfOutputs):
    """
    Initialize Performance outputs for each USR

    Parameters:
    - PerfOutputs: Intermediate outputs for each USR's performance.
    
    """    
    # Loop over all 287 USRs of each constellation 
    for usrId in range(1,288):
        PerfOutputs[usrId] = {
            "NMI": 0,     
            "NSAMPS": 0,
            "MONPREV": 0,
            "GIVDESUM2": 0,
            "GIVDESAMPS": 0,
            "LATPREV": 0,
            "LONPREV": 0            
        }

    return

def WriteLineUsrPosfile(fOut, UsrPosEpochOutputs):
     for usr in UsrPosEpochOutputs.keys():        
        for i, result in enumerate(UsrPosEpochOutputs[usr]):
            fOut.write(((PosFileOutputFormatList[i] + delim) % UsrPosEpochOutputs[usr][result]))

        fOut.write("\n")    

def updatePosOutputs(PosOutputs, usrId, UpdateDict):
    """
    Update the intermediate outputs for a specific satellite with the provided tag-value pairs.

    Parameters:
    - PosOutputs: Intermediate outputs containing information for each satellite.
    - usrId: USER-ID for the user.
    - UpdateDict: Dictionary containing tag-value pairs to update in PosOutputs[usrId].

    Example:
    UpdatePosOutputs(PosOutputs, "188", {"SOD": 0, "MONPREV": 1, "XPREV": 100})
    """
    # Check if usrId exists in PosOutputs
    if usrId not in PosOutputs: PosOutputs[usrId] = {}        

    # Update or add tag-value pairs in PosOutputs[usrId]
    for tag, value in UpdateDict.items():
        PosOutputs[usrId][tag] = value

def updateInterOutputs(InterOutputs, SatLabel, UpdateDict):
    """
    Update the intermediate outputs for a specific satellite with the provided tag-value pairs.

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each satellite.
    - SatLabel: Label (identifier) for the satellite.
    - UpdateDict: Dictionary containing tag-value pairs to update in InterOutputs[SatLabel].

    Example:
    UpdateInterOutputs(InterOutputs, "G01", {"SODPREV": 10, "MONPREV": 1, "XPREV": 100})
    """
    # Check if SatLabel exists in InterOutputs
    if SatLabel not in InterOutputs:
        InterOutputs[SatLabel] = {}

    # Update or add tag-value pairs in InterOutputs[SatLabel]
    for tag, value in UpdateDict.items():
        InterOutputs[SatLabel][tag] = value

def updatePreviousInterOutputsFromCurrentUsrInfo(InterOutputs, UsrInfo):
    """
    Update the previous values in InterOutputs[SatLabel] using the current values from UsrInfo.
    SODPREV -> SoD;    MONPREV -> MONSTAT;    XPREV -> SAT-X;    YPREV -> SAT-X;    ZPREV -> SAT-X

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each satellite.
    - UsrInfo: Information for a specific satellite, including current values.
    """
    # Extract USR ID from UsrInfo
    usrId = int(UsrInfo[UsrLosIdx["ID"]])

    # Check if usrId exists in InterOutputs
    if usrId in InterOutputs:
        # Create UpdateDict with tag-value pairs for "PREV" values
        UpdateDict = {
            "SODPREV": int(UsrInfo[UsrLosIdx["SOD"]]),
            "MONPREV": int(UsrInfo[UsrLosIdx["STATUS"]])            
        }

        # Call the UpdateInterOutputs function with the UpdateDict
        updateInterOutputs(InterOutputs, usrId, UpdateDict)

def computeUsrRmsFromInterOuputs(interOutputs, usrId):
    """
    Compute the Root Mean Square of the GIVD error (GIVDE) in meters.

    Parameters:
    - interOutputs: Intermediate outputs.
    - usrId: Identifier) for the USR.

    Returns:
    - rmsGIVDE: RMS of the GIVD error.
    """
    usrData = interOutputs[usrId]
    
    # Update sample counts
    givdeSamps = usrData["GIVDESAMPS"]   
    if(givdeSamps == 0): return 0

    # Calculate RMS values
    rmsGIVDE = sqrt(usrData["GIVDESUM2"] / (givdeSamps))

    return rmsGIVDE


