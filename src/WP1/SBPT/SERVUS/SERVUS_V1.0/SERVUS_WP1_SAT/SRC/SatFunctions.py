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

# Define Earth's rotation rate (rad/sec)
OMEGA_EARTH = 7.2921151467e-5

# Define Satidistics Output file format list
StatsOutputFormat = "%s %6.2f %4d %6d %10.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %4d"
StatsOutputFormatList = StatsOutputFormat.split()

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
                "SREbCOUNT": 0,
                "SREaCOUNT": 0,
                "SREcCOUNT": 0,
                "SRErCOUNT": 0,                
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
    # Compute the Unitary Vector
    UnitaryVector = Direction / np.linalg.norm(Direction)

    return Vector.dot(UnitaryVector)

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
    satVelVector = ( (currPosVector - prevPosVector) / deltaT) + OMEGA_EARTH * currPosVector

    # Compute the Satellite Velocity unitary vector
    Uv = satVelVector / np.linalg.norm(satVelVector)

    # Compute the Radial Unitary Vector
    Ur = currPosVector / np.linalg.norm(currPosVector)
    
    # Compute the Cross Track Unitary Vector
    Uc = np.cross(Ur,Uv)

    # Compute the Along Track Unitary Vector
    Ua = np.cross(Uc,Ur)

    # Compute SRE in ACR frame by projecting the SRE in XYZ
    SREa = projectVector(sreVector, Ua)  
    SREc = projectVector(sreVector, Uc)      

    return SREa, SREc

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

def updateEpochStats(epochInfo, interOutputs, outputs):
    """
    Update the satellite statistics for the current epoch based on the provided information.

    Parameters:
    - epochInfo: Information for all satellites in a single epoch.
    - interOutputs: Intermediate outputs to store computed values for each satellite.
    - outputs: Output dictionary containing computed statistics for each satellite.

    For each satellite in the epoch, it calculates and updates the intermediate outputs
    such as SRE-A, SRE-B, SRE-C, SRE-R, and other relevant parameters. These intermediate
    outputs are later used to compute the final statistics.

    Additionally, the function updates the overall output statistics, including the percentage
    of monitored satellites, minimum and maximum number of RIMS in view, and RMS values of
    satellite residual errors along different components.    
    """

    # Loop over all Satellites Information in Epoch
    for satInfo in epochInfo:        
        currSod = int(satInfo[SatInfoIdx["SoD"]])
        # Reject the first Epoch
        if ( currSod == 0): 
            # Update the previous values with the current Values
            updatePreviousInterOutputsFromCurrentSatInfo(interOutputs, satInfo)
            continue           

        # Reject if satellite is not MONITORED:
        if(satInfo[SatInfoIdx["MONSTAT"]] != '1'): continue

        # Reject if SRE_STATUS IS NOT OK:
        if(satInfo[SatInfoIdx["SRESTAT"]] != '1'): continue
        
        # Extract PRN Column
        satLabel = satInfo[SatInfoIdx["PRN"]]

        # Add Number of samples
        interOutputs[satLabel]["NSAMPS"] = interOutputs[satLabel]["NSAMPS"] + 1

        # Add Satellite Monitoring Output
        outputs[satLabel]["MON"] = 1
    
        # Update number of samples Monitored & SRE OK
        interOutputs[satLabel]["SREWSAMPS"] = interOutputs[satLabel]["SREWSAMPS"] + 1

        # Update the Minimum Number of RIMS in view        
        if( int(satInfo[SatInfoIdx["NRIMS"]])<outputs[satLabel]["RIMS-MIN"]):
            outputs[satLabel]["RIMS-MIN"] = int(satInfo[SatInfoIdx["NRIMS"]])
        
        # Update the Maximun Number of RIMS in view        
        if( int(satInfo[SatInfoIdx["NRIMS"]])>outputs[satLabel]["RIMS-MAX"]):
            outputs[satLabel]["RIMS-MAX"] = int(satInfo[SatInfoIdx["NRIMS"]])        
        
        # # Calculate DeltaT (time difference) in seconds        
        DeltaT = currSod - interOutputs[satLabel]["SODPREV"]
        
        CurrPosVector = generateVectorFromSatInfo(satInfo, "SAT-X", "SAT-Y", "SAT-Z")    
        sreVector = generateVectorFromSatInfo(satInfo, "SREx", "SREy", "SREz")        
        PrevPosVector = np.array([interOutputs[satLabel]["XPREV"], interOutputs[satLabel]["YPREV"], interOutputs[satLabel]["ZPREV"]])        

        # Call computeSREaAndSREc() to compute SRE-Along and SRE-Cross
        srea, srec = computeSREaAndSREc(DeltaT, PrevPosVector, CurrPosVector, sreVector)   
        
        # Update sum of squared SRE values in InterOutputs[SatLabel]
        interOutputs[satLabel]["SREaSUM2"] += srea**2
        interOutputs[satLabel]["SREbSUM2"] += interOutputs[satLabel]["SREb"]**2
        interOutputs[satLabel]["SREcSUM2"] += srec**2
        interOutputs[satLabel]["SRErSUM2"] += interOutputs[satLabel]["SREr"]**2   

        # Update the Counts        
        interOutputs[satLabel]["SREaCOUNT"] += 1
        interOutputs[satLabel]["SREbCOUNT"] += 1
        interOutputs[satLabel]["SREcCOUNT"] += 1
        interOutputs[satLabel]["SRErCOUNT"] += 1

        # Update the previous values with the current SatInfo Values
        updatePreviousInterOutputsFromCurrentSatInfo(interOutputs, satInfo)


# END OF FUNCTION: def updateEpochStats(SatInfo, InterOutputs, Outputs):

def computeSreRmsFromSatLabel(interOutputs, satLabel):
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
    sre_a_samps = satData["SREaCOUNT"]
    sre_b_samps = satData["SREbCOUNT"]
    sre_c_samps = satData["SREcCOUNT"]
    sre_r_samps = satData["SRErCOUNT"]

    # Calculate RMS values
    rmsSreA = sqrt(satData["SREaSUM2"] / sre_a_samps) if sre_a_samps > 0 else 0
    rmsSreB = sqrt(satData["SREbSUM2"] / sre_b_samps) if sre_b_samps > 0 else 0
    rmsSreC = sqrt(satData["SREcSUM2"] / sre_c_samps) if sre_c_samps > 0 else 0
    rmsSreR = sqrt(satData["SRErSUM2"] / sre_r_samps) if sre_r_samps > 0 else 0

    return rmsSreA, rmsSreB,rmsSreC,rmsSreR


# FUNCTION: Compute the final Statistics
#-----------------------------------------------------------------------
def computeFinalStatistics(InterOutputs, Outputs):
    for satLabel in Outputs.keys():

        # Estimate the Monitoring Percentage
        if(InterOutputs[satLabel]["NSAMPS"] != 0):

            # Monitoring percentage = Monitored epochs / Total epochs
            Outputs[satLabel]["MON"] = Outputs[satLabel]["MON"] * 100.0 / InterOutputs[satLabel]["NSAMPS"]
        
        # Compute final RMS for all SRE        
        SREaRMS, SREbRMS,SREcRMS,SRErRMS = computeSreRmsFromSatLabel(InterOutputs, satLabel)
        Outputs[satLabel]["SREaRMS"] = SREaRMS
        Outputs[satLabel]["SREbRMS"] = SREbRMS
        Outputs[satLabel]["SREcRMS"] = SREcRMS
        Outputs[satLabel]["SRErRMS"] = SRErRMS

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

            # Write Header of Output ENT-GPS file
            fEntGps.write("#SOD\tENT-GPS\n")

            # Open Output File Satellite Statistics file
            with open(satStatsFile, 'w') as fOut:
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
                        # Compute ENT-GPS and All SREs
                        ent_gps = computeEntGpsAndSREb(EpochInfo, InterOutputs)
                        sod = EpochInfo[0][SatInfoIdx["SoD"]]
                        
                        # Write ENT-GPS Offset file
                        fEntGps.write("%5s %10.4f\n" % (sod,ent_gps))                    
                        
                        # Update the Intermediate Statistics
                        updateEpochStats(EpochInfo, InterOutputs, Outputs)                                            
                    
                    else:
                        EndOfFile = True
                
                # Compute the final Statistics
                # ----------------------------------------------------------
                computeFinalStatistics(InterOutputs, Outputs)
                
                # Write Statistics File
                # ----------------------------------------------------------
                # Write Header of Output files
                #header_string = "\t".join(SatStatsIdx) + "\n"
                header_string = "PRN	  MON	 RIMS-MIN	RIMS-MAX SREaRMS   SREcRMS     SRErRMS	   SREbRMS	   SREWRMS	   SREWMAX	   SFLTMAX	   SFLTMIN	   SIMAX	   FCMAX	   LTCbMAX	   LTCxMAX	   LTCyMAX	   LTCzMAX	   NMI	       NTRANS\n"
                fOut.write(header_string)

                for sat in Outputs.keys():
                    
                    # Remove 0% monitored satellites because we're not interested in them
                    if(Outputs[sat]["MON"] != 0):
                        
                        for i, result in enumerate(Outputs[sat]):
                            fOut.write(((StatsOutputFormatList[i] + "\t") % Outputs[sat][result]))

                        fOut.write("\n")

                        # End of for i, result in enumerate(Outputs[sat]):
                    # End of if(Outputs[sat]["MON"] != 0):
                # End of for sat in Outputs.keys():
            # End of with open(satStatsFile, 'w') as fOut:
        # End of with open(EntGpsFile, 'w') as fEntGps:
    # End of with open(satFile, 'r') as f:

#End of def computeSatStats(satFile, satStatsFile):


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

def computeEntGpsAndSREb(epochInfo, interOutputs):
    """
    This function computes and returns the ENT-GPS Offset: estimated from the SRE of the monitored satellites with SRE_STATUS OK 
    It also computes and stores in, 'inter_outputs', the SREb (Satellite Residual Error Clock Component).

    - SREa (Satellite Residual Error Along Track Component)
    - SREc (Satellite Residual Error Cross Track Component)
    - SREr (Satellite Residual Error Radial Component)

    Parameters:
    - epoch_info: Information for all satellites in a single epoch.
    - inter_outputs: Intermediate outputs to store computed values.

    Updates inter_outputs in-place.
    """
    
    # Initialize lists to store radial component of SRE vector for each satellite
    SREb1MinusSRErList = []
    
    # Initialize variables for DeltaT, PosPrev, and Pos
    DeltaT = 0
    PosPrev = np.array([0, 0, 0])  # Assuming initial position is [0, 0, 0]
    
    #for sat_info in epoch_info:
    for satInfo in epochInfo:
        prn = satInfo[SatInfoIdx["PRN"]]

        sreStatus = satInfo[SatInfoIdx["SRESTAT"]]
        
        # Rejects Epoch with SRE STATUS == 0
        if (sreStatus=='0'): continue            

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
        prn = satInfo[SatInfoIdx["PRN"]]

        # Update interOutputs with computed SREb
        updateInterOutputs(interOutputs, prn, {"SREb": SREb1 - EntGps})        

    return EntGps



    # Update inter_outputs with computed SREb
    
    # Update inter_outputs with computed SREb
    


    
########################################################################
#END OF SAT FUNCTIONS MODULE
########################################################################
