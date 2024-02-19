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
from IgpStatistics import IgpInfoIdx, IgpStatsIdx, RimsIdx 


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
            header_string = "ID BAND BIT   LON       LAT      MON    MINIPPs MAXIPPs NTRANS  RMSGIVDE MAXGIVD  MAXGIVE  MAXGIVEI  MAXVTEC  MAXSI    NMI\n"
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

    updateEpochMaxMinStatsNonMonitored(IgpInfo, igpId, Outputs)

    # Reject if IGP STATUS is not OK:
    if(IgpInfo[IgpInfoIdx["STATUS"]] != '1'):        
        # stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)
        return
    
    # Add Satellite Monitoring if Satellite is Monitored
    Outputs[igpId]["MON"] += 1    

    # Reject if GIVDE_STAT IS NOT OK:
    if(IgpInfo[IgpInfoIdx["GIVDE_STAT"]] != '1'): 
        # stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)        
        return
    
    # Update number of samples GIVDESAMPS
    InterOutputs[igpId]["GIVDESAMPS"] += 1

    Outputs[igpId]["BAND"] = int(IgpInfo[IgpInfoIdx["BAND"]])
    Outputs[igpId]["BIT"] = int(IgpInfo[IgpInfoIdx["BIT"]])
    Outputs[igpId]["LON"] = float(IgpInfo[IgpInfoIdx["LON"]])
    Outputs[igpId]["LAT"] = float(IgpInfo[IgpInfoIdx["LAT"]])

    # # Reject the first Epoch
    # if ( currSod == 0):         
    #     stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)
    #     return    
   
    # Update sum of squared GIVDE values in InterOutputs[igpId]
    InterOutputs[igpId]["GIVDESUM2"] += float(IgpInfo[IgpInfoIdx["GIVDE"]])**2
    
    # Update the previous values with the current IgpInfo Values
    # stat.updatePreviousInterOutputsFromCurrentIgpInfo(InterOutputs, IgpInfo)

def updateEpochMaxMinStatsNonMonitored(IgpInfo, igpId, Outputs):
    # Update the Minimum Number of IPPs surrounding the IGP
    NIPP = int(IgpInfo[IgpInfoIdx["NIPP"]])
    if( NIPP < Outputs[igpId]["MINIPPs"]):
        Outputs[igpId]["MINIPPs"] = NIPP
    
    # Update the Maximum Number of IPPs surrounding the IGP
    if( NIPP > Outputs[igpId]["MAXIPPs"]):
        Outputs[igpId]["MAXIPPs"] = NIPP        

    # Update the Maximun SREw
    # currSREW = float(IgpInfo[IgpInfoIdx["SREW"]])
    # if( currSREW > Outputs[igpId]["SREWMAX"]):
    #     Outputs[igpId]["SREWMAX"] = currSREW

    # # Update the Maximun SFLT
    # currSFLT = float(IgpInfo[IgpInfoIdx["SFLT-W"]])
    # if( currSFLT > Outputs[igpId]["SFLTMAX"]):
    #     Outputs[igpId]["SFLTMAX"] = currSFLT

    # # Update the Minimun SFLT
    # if( currSFLT < Outputs[igpId]["SFLTMIN"]):
    #     Outputs[igpId]["SFLTMIN"] = currSFLT
    
    # # Compute MAX SIW - Maximum Satellite Safety Index
    # # As the ratio between the SRE and the SigmaFLT at the Worst User Location
    # currSIW = currSREW / (5.33 * currSFLT)

    # # Update the Maximum SIMAX
    # if( currSIW > Outputs[igpId]["SIMAX"]):
    #     Outputs[igpId]["SIMAX"] = currSIW

    # # Update the Number of Satellite MIs (Misleading Information) - SI > 1
    # if(currSIW > 1):
    #     Outputs[igpId]["NMI"] += 1    
    
    # # Update the Maximun Absolute Value of LTCb
    # absAF0 = abs(float(IgpInfo[IgpInfoIdx["AF0"]]))
    # if(absAF0 > Outputs[igpId]["LTCbMAX"]):
    #     Outputs[igpId]["LTCbMAX"] = absAF0

    # # Update the Maximun Absolute Value of FCMAX
    # absFC = abs(float(IgpInfo[IgpInfoIdx["FC"]]))
    # if(absFC > Outputs[igpId]["FCMAX"]):
    #     Outputs[igpId]["FCMAX"] = absFC

    # # Update the Maximun Absolute Value of LTCx
    # absLTCx = abs(float(IgpInfo[IgpInfoIdx["LTCx"]]))
    # if(absLTCx > Outputs[igpId]["LTCxMAX"]):
    #     Outputs[igpId]["LTCxMAX"] = absLTCx

    # # Update the Maximun Absolute Value of LTCy
    # absLTCy = abs(float(IgpInfo[IgpInfoIdx["LTCy"]]))
    # if(absLTCy > Outputs[igpId]["LTCyMAX"]):
    #     Outputs[igpId]["LTCyMAX"] = absLTCy
    
    # # Update the Maximun Absolute Value of LTCz
    # absLTCz = abs(float(IgpInfo[IgpInfoIdx["LTCz"]]))
    # if(absLTCz > Outputs[igpId]["LTCzMAX"]):
    #     Outputs[igpId]["LTCzMAX"] = absLTCz

def computeFinalStatistics(InterOutputs, Outputs):
    for igpId in Outputs.keys():

        # Rejects Data with no samples
        if(InterOutputs[igpId]["NSAMPS"] <= 0):
            continue

        # Estimate the Monitoring percentage = Monitored epochs / Total epochs
        Outputs[igpId]["MON"] = Outputs[igpId]["MON"] * 100.0 / InterOutputs[igpId]["NSAMPS"]

        # Compute final RMS for all SRE        
        # SREaRMS, SREbRMS,SREcRMS,SRErRMS,SREwRMS = stat.computeSatRmsSreAcrFromInterOuputs(InterOutputs, igpId)
        # Outputs[igpId]["SREaRMS"] = SREaRMS        






########################################################################
#END OF IGP FUNCTIONS MODULE
########################################################################
