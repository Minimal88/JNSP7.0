#!/usr/bin/env python

########################################################################
# SatStatistics.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatStatistics.py
#  Date(YY/MM/DD): 24/02/19
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

# Define SAT INFO FILE Columns
"""
SatStatsIdx is a dictionary that maps the column names of the satellite statistics file to their corresponding indices.
"""
IgpInfoIdx = dict([
    ("SoD", 0),
    ("DOY", 1),
    ("ID", 2),
    ("BAND", 3),
    ("BIT", 4),
    ("LON", 5),
    ("LAT", 6),
    ("STATUS", 7),
    ("GIVEI", 8),
    ("GIVE", 9),
    ("GIVD", 10),
    ("GIVDE_STAT", 11),
    ("GIVDE", 12),
    ("SI-W", 13),
    ("VTEC", 14),
    ("NIPP", 15),
    ("MMFLAG", 16),
    ("IONMMRATIO", 17)    
])

# Define SAT STATISTICS file Columns
IgpStatsIdx = dict([
    ("ID", 0),
    ("BAND", 1),
    ("BIT", 2),
    ("LON", 3),
    ("LAT", 4),
    ("MON", 5),
    ("MINIPPs", 6),
    ("MAXIPPs", 7),
    ("NTRANS", 8),
    ("RMSGIVDE", 9),
    ("MAXGIVD", 10),
    ("MAXGIVE", 11),
    ("MAXGIVEI", 12),
    ("MAXVTEC", 13),
    ("MAXSI", 14),
    ("NMI", 15)    
])

# Define Satidistics Output file format list
StatsOutputFormat = "%3d %3d %5d %8.2f %8.2f %8.2f %6d %6d %6d %10.4f %8.3f %8.3f %8d %8.3f %8.4f %6d"


def splitLine(Line):
    """
    # FUNCTION: Split line
    """
    LineSplit = Line.split()

    return LineSplit

def readIgpInfoEpoch(f):
    """
    FUNCTION: Read Igp Info Epoch
    """
    EpochInfo = []
    
    # Read one line
    Line = f.readline()
    if(not Line):
        return []
    LineSplit = splitLine(Line)
    Sod = LineSplit[IgpInfoIdx["SoD"]]
    SodNext = Sod

    while SodNext == Sod:
        EpochInfo.append(LineSplit)
        Pointer = f.tell()
        Line = f.readline()
        LineSplit = splitLine(Line)
        try: 
            SodNext = LineSplit[IgpInfoIdx["SoD"]]

        except:
            return EpochInfo

    f.seek(Pointer)

    return EpochInfo

def initializeOutputs(Outputs):    
    # Loop over all 287 IGPs of each constellation 
    for igpId in range(1,288):            
        Outputs[igpId] = OrderedDict({})
        for var in IgpStatsIdx.keys():                
            if (var == "ID"):
                Outputs[igpId][var] = int(igpId)
            elif (var == "MINIPPs"):
                Outputs[igpId][var] = 1e12            
            else:
                Outputs[igpId][var] = 0.0

def initializeInterOutputs(InterOutputs):
    """
    Initialize intermediate outputs for each IGP

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each IGP.
    
    """    
    # Loop over all 287 IGPs of each constellation 
    for igpId in range(1,288):
        InterOutputs[igpId] = {
            "NMI": 0,     
            "NSAMPS": 0,
            "MONPREV": 0,
            "GIVDESUM2": 0,
            "GIVDESAMPS": 0,
            "LATPREV": 0,
            "LONPREV": 0            
        }

    return

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

def updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo):
    """
    Update the previous values in InterOutputs[SatLabel] using the current values from IgpInfo.
    SODPREV -> SoD;    MONPREV -> MONSTAT;    XPREV -> SAT-X;    YPREV -> SAT-X;    ZPREV -> SAT-X

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each satellite.
    - IgpInfo: Information for a specific satellite, including current values.
    """
    # Extract IGP ID from IgpInfo
    igpId = int(IgpInfo[IgpInfoIdx["ID"]])

    # Check if igpId exists in InterOutputs
    if igpId in InterOutputs:
        # Create UpdateDict with tag-value pairs for "PREV" values
        UpdateDict = {
            "SODPREV": int(IgpInfo[IgpInfoIdx["SoD"]]),
            "MONPREV": int(IgpInfo[IgpInfoIdx["STATUS"]])            
        }

        # Call the UpdateInterOutputs function with the UpdateDict
        updateInterOutputs(InterOutputs, igpId, UpdateDict)

def computeIgpRmsFromInterOuputs(interOutputs, igpId):
    """
    Compute the Root Mean Square of the GIVD error (GIVDE) in meters.

    Parameters:
    - interOutputs: Intermediate outputs.
    - igpId: Identifier) for the IGP.

    Returns:
    - rmsGIVDE: RMS of the GIVD error.
    """
    igpData = interOutputs[igpId]
    
    # Update sample counts
    givdeSamps = igpData["GIVDESAMPS"]   
    if(givdeSamps == 0): return 0

    # Calculate RMS values
    rmsGIVDE = sqrt(igpData["GIVDESUM2"] / (givdeSamps))

    return rmsGIVDE


