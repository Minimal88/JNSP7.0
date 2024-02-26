#!/usr/bin/env python

########################################################################
# SBPT/SRC/IgpFunctions.py:
# This script defines all internal functions of IgpPerformance Module
#
#  Project:        SBPT
#  File:           IgpFunctions.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2021 GNSS Academy
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys
import numpy as np
from COMMON.Files import readDataFile
from collections import OrderedDict
import IgpStatistics  as stat
from IgpStatistics import IgpInfoIdx, IgpStatsIdx


# Define Satidistics Output file format list
StatsOutputFormatList = stat.StatsOutputFormat.split()

# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def computeIgpStats(igpInfoFile, igpStatsFile):
    
    # Initialize Variables
    EndOfFile = False
    EpochInfo = []
    delim = " "

    # Open IGP INFO file
    with open(igpInfoFile, 'r') as fsat:
        
        # Read header line of Sat Information file
        fsat.readline()

        # Open Output File Satellite Statistics file
        with open(igpStatsFile, 'w') as fOut:
            # Define and Initialize Variables            
            Outputs = OrderedDict({})
            InterOutputs = OrderedDict({})
            
            # Initialize Outputs
            stat.initializeOutputs(Outputs)
            stat.initializeInterOutputs(InterOutputs)

            # LOOP over all Epochs of IGP INFO file
            # ----------------------------------------------------------
            while not EndOfFile:                    
                # Read Only One Epoch
                EpochInfo = stat.readIgpInfoEpoch(fsat)
                
                # If EpochInfor is not Null
                if EpochInfo != []:
                    # sod = EpochInfo[0][IgpInfoIdx["SoD"]]
                    
                    # Loop over all Satellites Information in Epoch
                    # --------------------------------------------------
                    for IgpInfo in EpochInfo:
                        # Update the Intermediate Statistics
                        updateEpochStats(IgpInfo, InterOutputs, Outputs)                                            
                
                else:
                    EndOfFile = True
            
            # Compute the final Statistics
            # ----------------------------------------------------------
            computeFinalStatistics(InterOutputs, Outputs)
            
            # Write Statistics File
            # ----------------------------------------------------------
            # Write Header of Output files                
            #header_string = delim.join(IgpStatsIdx) + "\n"
            header_string = "ID   BAND BIT   LON       LAT      MON    MINIPPs MAXIPPs NTRANS  RMSGIVDE MAXGIVD  MAXGIVE  MAXGIVEI  MAXVTEC  MAXSI     NMI\n"
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
    # End of with open(igpInfoFile, 'r') as f:





# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def displayUsage():
    """
    FUNCTION: Display Message
    """
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")

def updateEpochStats(IgpInfo, InterOutputs, Outputs):
    """
    Update the IGP statistics for the current epoch based on the provided information.

    Parameters:
    - IgpInfo: Information for a IGP in a single epoch.
    - interOutputs: Intermediate outputs to store computed values for each IGP.
    - outputs: Output dictionary containing computed statistics for each IGP.

    For each IGP in the epoch, it calculates and updates the intermediate outputs
    such as SRE-A, SRE-B, SRE-C, SRE-R. Additionally, it updates the overall output statistics,
    including the percentage of monitored IGPs, minimum and maximum number of RIMS in view,
    and RMS values of IGP residual errors along different components.    
    """
    
    # Extract ID Column
    igpId = int(IgpInfo[IgpInfoIdx["ID"]])

    # Add Number of samples
    InterOutputs[igpId]["NSAMPS"] = InterOutputs[igpId]["NSAMPS"] + 1

    # Add NTRANS Monitored to Not Monitored (MtoNM) or to Don't USE (MtoDU)
    prevMon = InterOutputs[igpId]["MONPREV"]
    currMon = int(IgpInfo[IgpInfoIdx["STATUS"]])
    if(((prevMon == 1) and (currMon == 0)) or ((prevMon == 1) and (currMon == -1))):
        Outputs[igpId]["NTRANS"] += 1      

    updateEpochMaxMinStatsNonMonitored(IgpInfo, igpId, Outputs)

    # Reject if IGP STATUS is not OK:
    if(currMon != 1):        
        stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)
        return
    
    # Add Satellite Monitoring if Satellite is Monitored
    Outputs[igpId]["MON"] += 1    

    # Reject if GIVDE_STAT IS NOT OK:
    if(IgpInfo[IgpInfoIdx["GIVDE_STAT"]] != '1'): 
        stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)        
        return
    
    # Update number of samples GIVDESAMPS
    InterOutputs[igpId]["GIVDESAMPS"] += 1

    updateEpochMaxMinStatsMonitored(IgpInfo, igpId, Outputs)

    Outputs[igpId]["BAND"] = int(IgpInfo[IgpInfoIdx["BAND"]])
    Outputs[igpId]["BIT"] = int(IgpInfo[IgpInfoIdx["BIT"]])
    Outputs[igpId]["LON"] = float(IgpInfo[IgpInfoIdx["LON"]])
    Outputs[igpId]["LAT"] = float(IgpInfo[IgpInfoIdx["LAT"]])

    # Update sum of squared GIVDE values in InterOutputs[igpId]
    InterOutputs[igpId]["GIVDESUM2"] += float(IgpInfo[IgpInfoIdx["GIVDE"]])**2
    
    # Update the previous values with the current IgpInfo Values
    stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)

def updateEpochMaxMinStatsNonMonitored(IgpInfo, igpId, Outputs):
    # Update the Minimum Number of IPPs surrounding the IGP
    NIPP = int(IgpInfo[IgpInfoIdx["NIPP"]])
    if( NIPP < Outputs[igpId]["MINIPPs"]):
        Outputs[igpId]["MINIPPs"] = NIPP
    
    # Update the Maximum Number of IPPs surrounding the IGP
    if( NIPP > Outputs[igpId]["MAXIPPs"]):
        Outputs[igpId]["MAXIPPs"] = NIPP        
    
    # Update the Maximun VTEC
    currVTEC = float(IgpInfo[IgpInfoIdx["VTEC"]])
    if( currVTEC > Outputs[igpId]["MAXVTEC"]):
        Outputs[igpId]["MAXVTEC"] = currVTEC

def updateEpochMaxMinStatsMonitored(IgpInfo, igpId, Outputs):
    # Update the Maximun GIVD
    currGIVD = float(IgpInfo[IgpInfoIdx["GIVD"]])
    if( currGIVD > Outputs[igpId]["MAXGIVD"]):
        Outputs[igpId]["MAXGIVD"] = currGIVD

    # Update the Maximun GIVE
    currGIVE = float(IgpInfo[IgpInfoIdx["GIVE"]])
    if( currGIVE > Outputs[igpId]["MAXGIVE"]):
        Outputs[igpId]["MAXGIVE"] = currGIVE

    # Update the Maximun GIVEI
    currGIVEI = float(IgpInfo[IgpInfoIdx["GIVEI"]])
    if( currGIVEI > Outputs[igpId]["MAXGIVEI"]):
        Outputs[igpId]["MAXGIVEI"] = currGIVEI 
    
    # Update the Maximun SI
    currSIW = float(IgpInfo[IgpInfoIdx["SI-W"]])
    if( currSIW > Outputs[igpId]["MAXSI"]):
        Outputs[igpId]["MAXSI"] = currSIW
    
    # Update the Number of IGP MIs (Misleading Information) NMI = SI > 1
    if(currSIW > 1):
        Outputs[igpId]["NMI"] += 1    


def computeFinalStatistics(InterOutputs, Outputs):
    for igpId in Outputs.keys():

        # Rejects Data with no samples
        if(InterOutputs[igpId]["NSAMPS"] <= 0):
            continue

        # Estimate the Monitoring percentage = Monitored epochs / Total epochs
        Outputs[igpId]["MON"] = Outputs[igpId]["MON"] * 100.0 / InterOutputs[igpId]["NSAMPS"]

        # Compute final RMS
        rmsGIVDE = stat.computeIgpRmsFromInterOuputs(InterOutputs, igpId)
        Outputs[igpId]["RMSGIVDE"] = rmsGIVDE        






########################################################################
#END OF IGP FUNCTIONS MODULE
########################################################################
