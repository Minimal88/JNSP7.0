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
SatInfoIdx = dict([
    ("SoD", 0),
    ("DOY", 1),
    ("PRN", 2),
    ("SAT-X", 3),
    ("SAT-Y", 4),
    ("SAT-Z", 5),
    ("MONSTAT", 6),
    ("SRESTAT", 7),
    ("SREx", 8),
    ("SREy", 9),
    ("SREz", 10),
    ("SREb1", 11),
    ("SREW", 12),
    ("SFLT-W", 13),
    ("UDREI", 14),
    ("FC", 15),
    ("AF0", 16),
    ("AF1", 17),
    ("LTCx", 18),
    ("LTCy", 19),
    ("LTCz", 20),
    ("NRIMS", 21),
    ("RDOP", 22)
])

# Define SAT STATISTICS file Columns
SatStatsIdx = dict([
    ("PRN", 0),
    ("MON", 1),
    ("RIMS-MIN", 2),
    ("RIMS-MAX", 3),
    ("SREaRMS", 4),
    ("SREcRMS", 5),
    ("SRErRMS", 6),
    ("SREbRMS", 7),
    ("SREWRMS", 8),
    ("SREWMAX", 9),
    ("SFLTMAX", 10),
    ("SFLTMIN", 11),
    ("SIMAX", 12),
    ("FCMAX", 13),
    ("LTCbMAX", 14),
    ("LTCxMAX", 15),
    ("LTCyMAX", 16),
    ("LTCzMAX", 17),
    ("NMI", 18),
    ("NTRANS", 19)
])

# Define STATISTICS TIME file Columns (ENT-GPS)
SatStatsTimeIdx = dict([
    ("SoD", 0),         # SOD
    ("ENT-GPS", 1),     # ENT-GPS
    ("MON", 2),         # Monitored
    ("NMON", 3),        # Not Monitored
    ("DU", 4),          # Dont Use
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
StatsOutputFormat = "%s %6.2f %4d %6d %10.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %4d"


def splitLine(Line):
    """
    # FUNCTION: Split line
    """
    LineSplit = Line.split()

    return LineSplit

def readSatInfoEpoch(f):
    """
    FUNCTION: Read Sat Info Epoch
    """
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
                elif (var == "SFLTMIN"):
                    Outputs[SatLabel][var] = 1e12
                else:
                    Outputs[SatLabel][var] = 0.0

def initializeInterOutputs(InterOutputs):
    """
    Initialize intermediate outputs for each satellite and ENT-GPS.

    Parameters:
    - InterOutputs: Intermediate outputs containing information for each satellite.

    This function initializes the structure of InterOutputs for GPS and Galileo satellites
    along with ENT-GPS.
    """
    # Loop over GPS and Galileo Satellites
    for Const in ['G', 'E']:
        for Prn in range(1, 33):
            SatLabel = Const + "%02d" % Prn
            InterOutputs[SatLabel] = {
                "NSAMPS": 0,
                "SODPREV": 0,
                "MONPREV": 0,
                "SREa": 0,
                "SREb": 0,
                "SREc": 0,
                "SREr": 0,
                "SREbSUM2": 0,
                "SREaSUM2": 0,
                "SREcSUM2": 0,
                "SRErSUM2": 0,                
                "SREACRSAMPS": 0,
                "SREWSUM2": 0,
                "SREWSAMPS": 0,
                "XPREV": 0,
                "YPREV": 0,
                "ZPREV": 0
            }

    # Initialize ENT-GPS
    InterOutputs["ENT-GPS"] = 0

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
    x = float(sat_info[SatInfoIdx[ColTagX]])
    y = float(sat_info[SatInfoIdx[ColTagY]])
    z = float(sat_info[SatInfoIdx[ColTagZ]])

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
    SatLabel = SatInfo[SatInfoIdx["PRN"]]

    # Check if SatLabel exists in InterOutputs
    if SatLabel in InterOutputs:
        # Create UpdateDict with tag-value pairs for "PREV" values
        UpdateDict = {
            "SODPREV": int(SatInfo[SatInfoIdx["SoD"]]),
            "MONPREV": int(SatInfo[SatInfoIdx["MONSTAT"]]),
            "XPREV": float(SatInfo[SatInfoIdx["SAT-X"]]),
            "YPREV": float(SatInfo[SatInfoIdx["SAT-Y"]]),
            "ZPREV": float(SatInfo[SatInfoIdx["SAT-Z"]])
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

def computeEntGpsAndSREb(epochInfo, interOutputs):
    """
    This function computes and returns the ENT-GPS Offset: estimated from the SRE of the monitored satellites with SRE_STATUS OK 
    It also computes and stores in, 'interOutputs', the SREb (Satellite Residual Error Clock Component).

    - SREa (Satellite Residual Error Along Track Component)
    - SREc (Satellite Residual Error Cross Track Component)
    - SREr (Satellite Residual Error Radial Component)

    Parameters:
    - epoch_info: Information for all satellites in a single epoch.
    - interOutputs: Intermediate outputs to store computed values.

    Updates interOutputs in-place.
    """
    
    # Initialize lists to store radial component of SRE vector for each satellite
    SREb1MinusSRErList = []
    
    # Initialize variables for DeltaT, PosPrev, and Pos
    DeltaT = 0
    PosPrev = np.array([0, 0, 0])  # Assuming initial position is [0, 0, 0]
    
    for satInfo in epochInfo:
        prn = satInfo[SatInfoIdx["PRN"]]
        
        # Rejects Epoch with SRESTAT != 1
        if(satInfo[SatInfoIdx["SRESTAT"]] != '1'): continue            

        # Get the SREb1 from the Sat Info file (Satellite Residual Error Clock Bias)
        SREb1 = float(satInfo[SatInfoIdx["SREb1"]])

        # Get the sreVector and satVector
        sreVector = generateVectorFromSatInfo(satInfo, "SREx", "SREy", "SREz")
        satVector = generateVectorFromSatInfo(satInfo, "SAT-X", "SAT-Y", "SAT-Z")        
                
        # Calculate the radial component of the SRE vector        
        SREr = projectVector(sreVector, satVector)

        # Update interOutputs with computed SREr
        updateInterOutputs(interOutputs, prn, {"SREr": SREr})

        # Append (SREb1 - SREr) to the list for later computation
        SREb1MinusSRErList.append(SREb1 - SREr)

    # Compute ENT-GPS as the median of (SREb1 - SREr) for all satellites, for this specific epochInfo
    EntGps = np.median(SREb1MinusSRErList)    

    # Compute SREb = SREb1 - ent-gps, for this specific epochInfo
    for satInfo in epochInfo:        
        # Reject if SRE_STATUS IS NOT OK:
        if(satInfo[SatInfoIdx["SRESTAT"]] != '1'): continue
        
        SREb1 = float(satInfo[SatInfoIdx["SREb1"]])
        # Update interOutputs with computed SREb
        updateInterOutputs(interOutputs, satInfo[SatInfoIdx["PRN"]], {"SREb": SREb1 - EntGps})                

    return EntGps  

def countMonitoredSatsInEpoch(epochInfo):
    cntMon = 0
    cntNotMon = 0
    cntDu = 0
    for satInfo in epochInfo:
        if(satInfo[SatInfoIdx["MONSTAT"]] == '1'): 
            cntMon += 1
        elif (satInfo[SatInfoIdx["MONSTAT"]] == '0'):
            cntNotMon += 1
        elif (satInfo[SatInfoIdx["MONSTAT"]] == '-1'):
            cntDu += 1

    
    return cntMon, cntNotMon, cntDu