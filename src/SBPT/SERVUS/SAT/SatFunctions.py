#!/usr/bin/env python

########################################################################
# SatFunctions.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatFunctions.py
#  Date(YY/MM/DD): 24/02/19
#
#   Author: Esteban Martinez Valvere
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
#   SatStatistics
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys
from collections import OrderedDict
from COMMON.Coordinates import xyz2llh
import SatStatistics  as stat
import numpy as np
import copy

# Define SAT INFO FILE Columns
"""
SatStatsIdx is a dictionary that maps the column names of the satellite statistics file to their corresponding indices.
"""
SatInfoIdx = copy.deepcopy(stat.SatInfoIdx)

# Define SAT STATISTICS file Columns
SatStatsIdx = copy.deepcopy(stat.SatStatsIdx)

SatStatsTimeIdx = copy.deepcopy(stat.SatStatsTimeIdx)

# Define Satidistics Output file format list
StatsOutputFormatList = stat.StatsOutputFormat.split()

# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def computeSatStats(satFile, EntGpsFile, satStatsFile):
    
    # Initialize Variables
    EndOfFile = False
    EpochInfo = []
    delim = " "

    # Open SAT INFO file
    with open(satFile, 'r') as fsat:
        
        # Read header line of Sat Information file
        fsat.readline()

        # Open ENT-GPS Offset output file
        with open(EntGpsFile, 'w') as fEntGps:
            # Write Header of Output ENT-GPS file
            entGpsHeader = delim.join(SatStatsTimeIdx) + "\n"
            #fEntGps.write("#SOD\tENT-GPS\tNMON\n")
            fEntGps.write(entGpsHeader)

            # Open Output File Satellite Statistics file
            with open(satStatsFile, 'w') as fOut:
                # Define and Initialize Variables            
                Outputs = OrderedDict({})
                InterOutputs = OrderedDict({})
                
                # Initialize Outputs
                stat.initializeOutputs(Outputs)
                stat.initializeInterOutputs(InterOutputs)

                # LOOP over all Epochs of SAT INFO file
                # ----------------------------------------------------------
                while not EndOfFile:                    
                    # Read Only One Epoch
                    EpochInfo = stat.readSatInfoEpoch(fsat)
                    
                    # If EpochInfor is not Null
                    if EpochInfo != []:
                        # Compute ENT-GPS and All SREs
                        sod = EpochInfo[0][SatInfoIdx["SoD"]]
                        entGps = stat.computeEntGpsAndSREb(EpochInfo, InterOutputs)
                        cntMon, cntNotMon, cntDu = stat.countMonitoredSatsInEpoch(EpochInfo)                        
                        
                        # Write ENT-GPS Offset file
                        fEntGps.write("%5s %10.4f %d %d %d\n" % (sod,entGps,cntMon, cntNotMon, cntDu))                    
                        
                        # Loop over all Satellites Information in Epoch
                        # --------------------------------------------------
                        for SatInfo in EpochInfo:
                            # Update the Intermediate Statistics
                            updateEpochStats(SatInfo, InterOutputs, Outputs)                                            
                    
                    else:
                        EndOfFile = True
                
                # Compute the final Statistics
                # ----------------------------------------------------------
                computeFinalStatistics(InterOutputs, Outputs)
                
                # Write Statistics File
                # ----------------------------------------------------------
                # Write Header of Output files                
                header_string = delim.join(SatStatsIdx) + "\n"
                #header_string = "PRN	  MON	 RIMS-MIN	RIMS-MAX SREaRMS   SREcRMS     SRErRMS	   SREbRMS	   SREWRMS	   SREWMAX	   SFLTMAX	   SFLTMIN	   SIMAX	   FCMAX	   LTCbMAX	   LTCxMAX	   LTCyMAX	   LTCzMAX	   NMI	       NTRANS\n"
                fOut.write(header_string)

                for sat in Outputs.keys():
                    
                    # Remove 0% monitored satellites because we're not interested in them
                    if(Outputs[sat]["MON"] != 0):
                        
                        for i, result in enumerate(Outputs[sat]):
                            fOut.write(((StatsOutputFormatList[i] + delim) % Outputs[sat][result]))

                        fOut.write("\n")

                        # End of for i, result in enumerate(Outputs[sat]):
                    # End of if(Outputs[sat]["MON"] != 0):
                # End of for sat in Outputs.keys():
            # End of with open(satStatsFile, 'w') as fOut:
        # End of with open(EntGpsFile, 'w') as fEntGps:
    # End of with open(satFile, 'r') as f:

def ecefToGeodetic(xEcef, yEcef, zEcef):
    """
    Transform ECEF (Earth-Centered, Earth-Fixed) coordinates to Geodetic coordinates.

    Parameters:
    - xEcef, yEcef, zEcef: ECEF coordinates in meters.

    Returns:
    - Longitude, Latitude, h: Geodetic coordinates (longitude, latitude, height) in degrees and meters.
    """
    DataLen = len(xEcef)
    Longitude = np.zeros(DataLen)
    Latitude = np.zeros(DataLen)
    Altitude = np.zeros(DataLen)

    for index in range(DataLen):
        x = xEcef[index]
        y = yEcef[index]
        z = zEcef[index]
        Longitude[index], Latitude[index], Altitude[index] = xyz2llh(x, y, z)

    return Longitude, Latitude, Altitude

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def displayUsage():
    """
    FUNCTION: Display Message
    """
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")

def updateEpochStats(SatInfo, InterOutputs, Outputs):
    """
    Update the satellite statistics for the current epoch based on the provided information.

    Parameters:
    - SatInfo: Information for a satellite in a single epoch.
    - interOutputs: Intermediate outputs to store computed values for each satellite.
    - outputs: Output dictionary containing computed statistics for each satellite.

    For each satellite in the epoch, it calculates and updates the intermediate outputs
    such as SRE-A, SRE-B, SRE-C, SRE-R. Additionally, it updates the overall output statistics,
    including the percentage of monitored satellites, minimum and maximum number of RIMS in view,
    and RMS values of satellite residual errors along different components.    
    """
    
    # Extract PRN Column
    satPrn = SatInfo[SatInfoIdx["PRN"]]

    # Add Number of samples
    InterOutputs[satPrn]["NSAMPS"] = InterOutputs[satPrn]["NSAMPS"] + 1

    # Add NTRANS Monitored to Not Monitored (MtoNM) or to Don't USE (MtoDU)
    prevMon = InterOutputs[satPrn]["MONPREV"]
    currMon = int(SatInfo[SatInfoIdx["MONSTAT"]])
    if(((prevMon == 1) and (currMon == 0)) or ((prevMon == 1) and (currMon == -1))):
        Outputs[satPrn]["NTRANS"] += 1        

    # Reject if satellite is not MONITORED:
    if(SatInfo[SatInfoIdx["MONSTAT"]] != '1'):        
        stat.updatePreviousInterOutputsFromCurrentSatInfo(InterOutputs, SatInfo)
        return
    
    # Add Satellite Monitoring if Satellite is Monitored
    Outputs[satPrn]["MON"] += 1

    # Reject if SRE_STATUS IS NOT OK:
    if(SatInfo[SatInfoIdx["SRESTAT"]] != '1'): 
        stat.updatePreviousInterOutputsFromCurrentSatInfo(InterOutputs, SatInfo)        
        return
    
    updateEpochStatsMaxMin(SatInfo, satPrn, InterOutputs, Outputs)

    # Computes the SREa SREb SREc SREr squeared sum
    currSod = int(SatInfo[SatInfoIdx["SoD"]])
    # Reject the first Epoch
    if ( currSod == 0):         
        stat.updatePreviousInterOutputsFromCurrentSatInfo(InterOutputs, SatInfo)
        return    

    # Update number of samples Monitored & SRE OK
    InterOutputs[satPrn]["SREWSAMPS"] += 1

    # Update number of samples Monitored & SRE OK & Not First Epoch
    InterOutputs[satPrn]["SREACRSAMPS"] += 1        
    
    # # Calculate DeltaT (time difference) in seconds        
    prevSod = InterOutputs[satPrn]["SODPREV"]
    DeltaT = currSod - prevSod
    
    CurrPosVector = stat.generateVectorFromSatInfo(SatInfo, "SAT-X", "SAT-Y", "SAT-Z")    
    sreVector = stat.generateVectorFromSatInfo(SatInfo, "SREx", "SREy", "SREz")        
    PrevPosVector = np.array([InterOutputs[satPrn]["XPREV"], InterOutputs[satPrn]["YPREV"], InterOutputs[satPrn]["ZPREV"]])        

    # Call stat.computeSREaAndSREc() to compute SRE-Along and SRE-Cross
    srea, srec = stat.computeSREaAndSREc(DeltaT, PrevPosVector, CurrPosVector, sreVector)   
    sreb = InterOutputs[satPrn]["SREb"]
    srer = InterOutputs[satPrn]["SREr"]
    srew = float(SatInfo[SatInfoIdx["SREW"]])

    # Update sum of squared SRE values in InterOutputs[SatLabel]
    InterOutputs[satPrn]["SREaSUM2"] += srea**2
    InterOutputs[satPrn]["SREbSUM2"] += sreb**2
    InterOutputs[satPrn]["SREcSUM2"] += srec**2
    InterOutputs[satPrn]["SRErSUM2"] += srer**2   
    InterOutputs[satPrn]["SREWSUM2"] += srew**2   

    # Update the previous values with the current SatInfo Values
    stat.updatePreviousInterOutputsFromCurrentSatInfo(InterOutputs, SatInfo)

def updateEpochStatsMaxMin(SatInfo, satPrn, InterOutputs, Outputs):
    # Update the Minimum Number of RIMS in view        
    if( int(SatInfo[SatInfoIdx["NRIMS"]]) < Outputs[satPrn]["RIMS-MIN"]):
        Outputs[satPrn]["RIMS-MIN"] = int(SatInfo[SatInfoIdx["NRIMS"]])
    
    # Update the Maximun Number of RIMS in view        
    if( int(SatInfo[SatInfoIdx["NRIMS"]]) > Outputs[satPrn]["RIMS-MAX"]):
        Outputs[satPrn]["RIMS-MAX"] = int(SatInfo[SatInfoIdx["NRIMS"]])        

    # Update the Maximun SREw
    currSREW = float(SatInfo[SatInfoIdx["SREW"]])
    if( currSREW > Outputs[satPrn]["SREWMAX"]):
        Outputs[satPrn]["SREWMAX"] = currSREW

    # Update the Maximun SFLT
    currSFLT = float(SatInfo[SatInfoIdx["SFLT-W"]])
    if( currSFLT > Outputs[satPrn]["SFLTMAX"]):
        Outputs[satPrn]["SFLTMAX"] = currSFLT

    # Update the Minimun SFLT
    if( currSFLT < Outputs[satPrn]["SFLTMIN"]):
        Outputs[satPrn]["SFLTMIN"] = currSFLT
    
    # Compute MAX SIW - Maximum Satellite Safety Index
    # As the ratio between the SRE and the SigmaFLT at the Worst User Location
    currSIW = currSREW / (5.33 * currSFLT)

    # Update the Maximum SIMAX
    if( currSIW > Outputs[satPrn]["SIMAX"]):
        Outputs[satPrn]["SIMAX"] = currSIW

    # Update the Number of Satellite MIs (Misleading Information) - SI > 1
    if(currSIW > 1):
        Outputs[satPrn]["NMI"] += 1    
    
    # Update the Maximun Absolute Value of LTCb
    absAF0 = abs(float(SatInfo[SatInfoIdx["AF0"]]))
    if(absAF0 > Outputs[satPrn]["LTCbMAX"]):
        Outputs[satPrn]["LTCbMAX"] = absAF0

    # Update the Maximun Absolute Value of FCMAX
    absFC = abs(float(SatInfo[SatInfoIdx["FC"]]))
    if(absFC > Outputs[satPrn]["FCMAX"]):
        Outputs[satPrn]["FCMAX"] = absFC

    # Update the Maximun Absolute Value of LTCx
    absLTCx = abs(float(SatInfo[SatInfoIdx["LTCx"]]))
    if(absLTCx > Outputs[satPrn]["LTCxMAX"]):
        Outputs[satPrn]["LTCxMAX"] = absLTCx

    # Update the Maximun Absolute Value of LTCy
    absLTCy = abs(float(SatInfo[SatInfoIdx["LTCy"]]))
    if(absLTCy > Outputs[satPrn]["LTCyMAX"]):
        Outputs[satPrn]["LTCyMAX"] = absLTCy
    
    # Update the Maximun Absolute Value of LTCz
    absLTCz = abs(float(SatInfo[SatInfoIdx["LTCz"]]))
    if(absLTCz > Outputs[satPrn]["LTCzMAX"]):
        Outputs[satPrn]["LTCzMAX"] = absLTCz

def computeFinalStatistics(InterOutputs, Outputs):
    for satLabel in Outputs.keys():

        # Rejects Data with no samples
        if(InterOutputs[satLabel]["NSAMPS"] <= 0):
            continue

        # Estimate the Monitoring percentage = Monitored epochs / Total epochs
        Outputs[satLabel]["MON"] = Outputs[satLabel]["MON"] * 100.0 / InterOutputs[satLabel]["NSAMPS"]

        # Compute final RMS for all SRE        
        SREaRMS, SREbRMS,SREcRMS,SRErRMS,SREwRMS = stat.computeSatRmsSreAcrFromInterOuputs(InterOutputs, satLabel)
        Outputs[satLabel]["SREaRMS"] = SREaRMS
        Outputs[satLabel]["SREbRMS"] = SREbRMS
        Outputs[satLabel]["SREcRMS"] = SREcRMS
        Outputs[satLabel]["SRErRMS"] = SRErRMS
        Outputs[satLabel]["SREWRMS"] = SREwRMS


