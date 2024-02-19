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


# Define RIMS file Columns 
RimsIdx = dict([
    ("SF", 0),          # Selection flag [0:OFF/1:ON]
    ("SNA", 1),         # Station Name Acronym [%4s]
    ("SID", 2),         # Station Number ID [%2d]
    ("LON", 3),         # Longitude [deg]
    ("LAT", 4),         # Latitude [deg]
    ("HEI", 5),         # Height [meters]
    ("MA", 6),          # Mask Angle [deg]
    ("AT", 7),          # Acquisition Time [minutes]
    ("SITE", 8),        # Site [%s] 
    ("COUNTRY", 9)      # Country [%s]
])

# Define Satidistics Output file format list
StatsOutputFormat = "%3d %3d %3d %8.2f %8.2f %8.2f %6d %6d %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"


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
            "GIVDESUM2": 0,
            "GIVDESAMPS": 0,
            "LATPREV": 0,
            "LONPREV": 0            
        }

    return

def projectVector(Vector, Direction):
    """
    Project a vector onto a given direction.

    Parameters:
    - Vector: The vector to be projected.
    - Direction: The direction onto which the vector is projected.

    Returns:
    - The projection of the vector onto the given direction.
    """    
    assert any(Direction) == True, "Empty Direction Vector Array"

    # Compute the Unitary Vector
    UnitaryVector = Direction / np.linalg.norm(Direction)

    return Vector.dot(UnitaryVector)

def generateVectorFromSatInfo(sat_info, ColTagX, ColTagY, ColTagZ):
    """
    This function generates a vector given the column tags.

    Parameters:
    sat_info (dict): The dictionary containing satellite information.    
    ColTagX (str): The column tag for the x-component.
    ColTagY (str): The column tag for the y-component.
    ColTagZ (str): The column tag for the z-component.

    Returns:
    np.array: The generated vector.
    """

    # Get the components of the vector
    x = float(sat_info[IgpInfoIdx[ColTagX]])
    y = float(sat_info[IgpInfoIdx[ColTagY]])
    z = float(sat_info[IgpInfoIdx[ColTagZ]])

    # Get the vector
    vector = np.array([x, y, z])

    return vector

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

def updatePreviousInterOutputsFromCurrentSatInfo(InterOutputs, SatInfo):
    """
    Update the previous values in InterOutputs[SatLabel] using the current values from SatInfo.
    SODPREV -> SoD;    MONPREV -> MONSTAT;    XPREV -> SAT-X;    YPREV -> SAT-X;    ZPREV -> SAT-X

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each satellite.
    - SatInfo: Information for a specific satellite, including current values.
    """
    # Extract satellite label (PRN) from SatInfo
    SatLabel = SatInfo[IgpInfoIdx["PRN"]]

    # Check if SatLabel exists in InterOutputs
    if SatLabel in InterOutputs:
        # Create UpdateDict with tag-value pairs for "PREV" values
        UpdateDict = {
            "SODPREV": int(SatInfo[IgpInfoIdx["SoD"]]),
            "MONPREV": int(SatInfo[IgpInfoIdx["MONSTAT"]]),
            "XPREV": float(SatInfo[IgpInfoIdx["SAT-X"]]),
            "YPREV": float(SatInfo[IgpInfoIdx["SAT-Y"]]),
            "ZPREV": float(SatInfo[IgpInfoIdx["SAT-Z"]])
        }

        # Call the UpdateInterOutputs function with the UpdateDict
        updateInterOutputs(InterOutputs, SatLabel, UpdateDict)

def computeSatRmsSreAcrFromInterOuputs(interOutputs, satLabel):
    """
    Compute the Root Mean Square of Satellite Orbit Error Components (SRE-A, SRE-B, SRE-C, SRE-R).

    Parameters:
    - interOutputs: Intermediate outputs containing SRE components for each satellite.    
    - satLabel: Label (identifier) for the satellite.

    Returns:
    - rmsSreA: RMS of Satellite Residual Error Along-Track component.
    - rmsSreB: RMS of Satellite Residual Error Clock component.
    - rmsSreC: RMS of Satellite Residual Error Cross-Track component.
    - rmsSreR: RMS of Satellite Residual Error Radial component.
    """
    satData = interOutputs[satLabel]
    
    # Update sample counts
    srewSamps = satData["SREWSAMPS"]
    sreacrSamps = satData["SREACRSAMPS"]
    assert sreacrSamps == srewSamps, "Samples are not equal"

    # Calculate RMS values
    rmsSreA = sqrt(satData["SREaSUM2"] / (sreacrSamps))
    rmsSreB = sqrt(satData["SREbSUM2"] / (sreacrSamps))
    rmsSreC = sqrt(satData["SREcSUM2"] / (sreacrSamps))
    rmsSreR = sqrt(satData["SRErSUM2"] / (sreacrSamps))
    rmsSreW = sqrt(satData["SREWSUM2"] / (srewSamps))

    return rmsSreA, rmsSreB,rmsSreC,rmsSreR,rmsSreW

def computeSREaAndSREc(deltaT, prevPosVector, currPosVector, sreVector): 
    """
    Estimate the SRE-Along/Cross.

    Parameters:
    - deltaT: Time difference between PosPrev and Pos.
    - prevPosVector: Previous position vector.
    - currPosVector: Current position vector.
    - sreVector: Satellite Residual Error vector in XYZ.

    Returns:
    - SREa: SRE-Along.
    - SREc: SRE-Cross.    
    """
    # Compute the Satellite Velocity deriving the position and 
    # Adding Earth's Rotation effect on the reference frame
    omega_vector = np.array([0,0,GnssConstants.OMEGA_EARTH])
    satVelVector = ( (currPosVector - prevPosVector) / deltaT) +  np.cross(omega_vector, currPosVector)

    # Compute the Satellite Velocity unitary vector
    Uv = satVelVector / np.linalg.norm(satVelVector)

    # Compute the Radial Unitary Vector
    Ur = currPosVector / np.linalg.norm(currPosVector)
    
    # Compute the Cross Track Unitary Vector
    Uc = np.cross(Ur,Uv)

    # Compute the Along Track Unitary Vector
    Ua = np.cross(Uc,Ur)

    assert any(Ua) == True, "Empty Ua Array"
    assert any(Uc) == True, "Empty Uc Array"        

    # Compute SRE in ACR frame by projecting the SRE in XYZ
    SREa = projectVector(sreVector, Ua)  
    SREc = projectVector(sreVector, Uc)      

    return SREa, SREc



