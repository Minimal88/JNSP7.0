#!/usr/bin/env python

########################################################################
# SBPT/SRC/UsrFunctions.py:
# This script defines all internal functions of UsrPerformance Module
#
#  Project:        SBPT
#  File:           UsrFunctions.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2021 GNSS Academy
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import math
import sys
import numpy as np
from COMMON.Files import readDataFile
from collections import OrderedDict
import UsrHelper  as usrHlp
from UsrHelper import UsrLosIdx, UsrPosIdx, UsrPerfIdx

# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def computeUsrPosAndPerf(UsrLosFilePath, UsrPosFilePath, UsrPerfFilePath):    
    # Define and Initialize Variables            
    UsrPosEpochOutputs = OrderedDict({})
    UsrPerfOutputs = OrderedDict({})
    UsrPerfInterOutputs = OrderedDict({})
    EndOfFile = False
    UsrLosEpochData = []
    # Initialize Outputs
    usrHlp.initializePosOutputs(UsrPosEpochOutputs)
    usrHlp.initializePerfOutputs(UsrPerfOutputs)
    usrHlp.initializeInterPerfOutputs(UsrPerfInterOutputs)

    # Open USR LOS File
    fUserLos = open(UsrLosFilePath, 'r')
    # Open Output USR POS File 
    fPosFile = open(UsrPosFilePath, 'w')
    
    # Read header line of USR LOS File
    fUserLos.readline()
    
    # Write Header of Output files                
    # header_string = usrHlp.delim.join(UsrPosIdx) + "\n"
    header_string = "#   SOD  USER-ID   ULON       ULAT     SOL-FLAG   NVS   NVS-PA    HPE        VPE        HPL        VPL        HSI        VSI        HDOP       VDOP       PDOP\n"
    fPosFile.write(header_string)    

    # LOOP over all Epochs of USR INFO file
    # ----------------------------------------------------------
    while not EndOfFile:                    
        # Read the File Epoch by Epoch
        UsrLosEpochData = usrHlp.readUsrLosEpoch(fUserLos)                
        
        # If UsrLosEpochData is not Null
        if UsrLosEpochData != []:
            # Loop over all Users Information on each Epoch  in GRID:
            # --------------------------------------------------
            usrAvlSatList = []
            usrEpochSigmaUERE2_Dict = {}
            usrEpochRangeErrors_List = []            
            HPE_Dict = {} # [usrId][HPE list array]
            VPE_Dict = {} # [usrId][VPE list array]            
            NVSPA = 0   # Number of Visible Satellites in The PA Solutions
            NVS = 0    # Number of Visible Satellites with EL > 5
            usrSatIndex = 0

            for UsrLosData in UsrLosEpochData:
                # Extract USER LOS Columns
                usrId = int(UsrLosData[UsrLosIdx["USER-ID"]])
                SOD = int(UsrLosData[UsrLosIdx["SOD"]])
                ULON = float(UsrLosData[UsrLosIdx["ULON"]])
                ULAT = float(UsrLosData[UsrLosIdx["ULAT"]])        
                PRN = int(UsrLosData[UsrLosIdx["PRN"]])
                NSats = countTotalSatsOfUsrInEpoch(usrId, UsrLosEpochData)
                usrSatIndex = usrSatIndex + 1

                # Update the UsrPosOuputs for SOD, ULON, ULAT
                usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {
                    "SOD": SOD, "ULON": ULON, "ULAT":ULAT})
                
                # Update the UsrPerfOutputs
                usrHlp.updatePerfOutputs(UsrPerfOutputs, usrId, {
                    "ULON": ULON, "ULAT":ULAT})
                
                if usrId not in HPE_Dict: 
                    HPE_Dict[usrId] = []                    

                if usrId not in VPE_Dict: 
                    VPE_Dict[usrId] = []

                # LOOP Over all Satellites, and filter them
                # ----------------------------------------------------------
                # Count Sats with ELEV angle more than 5 degree TODO: Change it to USER.MASK_ANGLE
                if (float(UsrLosData[UsrLosIdx["ELEV"]]) > 5):
                    NVS = NVS + 1

                # Consider Sats only with Flag == 1 (Consider only PA Solutions)
                if (int(UsrLosData[UsrLosIdx["FLAG"]]) == 1):
                    usrAvlSatList.append(UsrLosData)
                    NVSPA = NVSPA + 1                    

                    # Build Ranging Error Vector by adding all the different contributors                        
                    RangeError = buildRangingErrorVector(UsrLosData)
                    usrEpochRangeErrors_List.append(RangeError)

                    # Build the SigmaUERE2 in line with MOPS Standard
                    SigmaUERE2 = buildSigmaUERE2(UsrLosData)
                    usrEpochSigmaUERE2_Dict[PRN] = SigmaUERE2

                # If reached the end of satellites on the EPOCH                                 
                if (usrSatIndex == NSats):
                    usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {"NVS": NVS, "NVS-PA": NVSPA})
                    # Compute PA Solution if at least 4 Satellites are valid for solution                            
                    #----------------------------------------------------------------------
                    if NVSPA >= 4:                                
                        # Build Geometry [G] matrix in line with SBAS Standard                                
                        GPA = buildGmatrix(usrAvlSatList)

                        # Build Weighting [W] matrix in line with SBAS Standards                                
                        WPA= buildWmatrix(usrAvlSatList, usrEpochSigmaUERE2_Dict)

                        # Compute Position Errors and Protection levels. XPE, XPL                                
                        [HPE, VPE, HPL, VPL, PDOP, HDOP, VDOP, FLAG] = computeXpeXplXdops(GPA, WPA, usrEpochRangeErrors_List)       

                        HSI = computeXSI(HPE, HPL)
                        VSI = computeXSI(VPE, VPL)
                        HPE_Dict[usrId].append(HPE)
                        VPE_Dict[usrId].append(VPE)
                        
                        # Update the UsrPosOuputs for SOL-FLAG, NVSPA, HPE, Nvs5, VPE, HPL, VPL
                        usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {
                            "SOL-FLAG":FLAG, "HPE":HPE, "VPE":VPE, 
                            "HPL":HPL, "VPL":VPL, "HSI":HSI, "VSI":VSI, 
                            "PDOP":PDOP, "HDOP":HDOP, "VDOP":VDOP})
                    
                    # Reset Loop variable, for the next iteration
                    usrAvlSatList = []   
                    usrEpochSigmaUERE2_Dict = {}
                    usrEpochRangeErrors_List = []
                    NVSPA = 0
                    NVS = 0
                    usrSatIndex = 0

            # END OF LOOP For ALL Users in EPOCH

            # Write USR POS File with the all the Usrs of the EPOCH
            # ----------------------------------------------------------
            usrHlp.WriteUsrsEpochPosFile(fPosFile, UsrPosEpochOutputs)            
        else:
            EndOfFile = True
            # Close the all the open files
            fUserLos.close()
            fPosFile.close()
        # END OF LOOP over all Users Information on each Epoch:
    # END OF LOOP for all Epochs of USR LOS file

        
    # Open Output USR Performance File 
    fPerfFile = open(UsrPerfFilePath, 'w')

    # Compute all User Performance values
    for usr in UsrPerfOutputs:
        computePercentile95(HPE_Dict[usr])




    fPerfFile.close()
        

        # Compute the final Statistics
        # ----------------------------------------------------------
        # computeFinalStatistics(UsrPerfOutputs, UsrPosEpochOutputs)
       




# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def displayUsage():
    """
    FUNCTION: Display Message
    """
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")

def buildRangingErrorVector(UsrLosData):
    """
        Build Ranging Error Vector by adding all the different contributors 
        RANGEERROR = SREU + UISDE + TropoE + AirE
    """
    # SREU = UsrLosData(UsrLosIdx["SREU"])
    # UISDE = UsrLosData(UsrLosIdx["UISDE"])
    # TropoE = UsrLosData(UsrLosIdx[])
    # AirE = UsrLosData(UsrLosIdx["SREU"])
    
    return float(UsrLosData[UsrLosIdx["RERROR"]])

def buildSigmaUERE2(UsrLosData):
    """
        Build the SigmaUERE2 in line with MOPS Standard
        SigmaUERE2 = SigmaFLT2 + SigmaUIRE2 + SigmaTropo2 + SigmaAIR2
    """

    # SigmaFLT2 = float(UsrLosData(UsrLosIdx["SFLT"])) ** 2
    # SigmaUIRE2 = float(UsrLosData(UsrLosIdx[""])) ** 2
    # SigmaTropo2 = float(UsrLosData(UsrLosIdx["SIGMTROPO"])) ** 2
    # SigmaAIR2 = float(UsrLosData(UsrLosIdx["SIGMAIR"])) ** 2
    
    return float(UsrLosData[UsrLosIdx["UERE"]]) ** 2

def buildGmatrix(satList):
    """
    Build the Geometry Matrices using the satellite elevation and azimuth
    """
    if not satList: return np.array([])
    GiList = []

    # Loop over all the available satetllites
    for i in range(len(satList)):
        usrLosData = satList[i]
        satElev = float(usrLosData[UsrLosIdx["ELEV"]])
        satAz = float(usrLosData[UsrLosIdx["AZIM"]])
    
        # Calculate elements of the ith row of the Geometry Matrix (G)
        Gi = [
            -math.cos(math.radians(satElev)) * math.sin(math.radians(satAz)),
            -math.cos(math.radians(satElev)) * math.cos(math.radians(satAz)),
            -math.sin(math.radians(satElev)),
            1
        ]
        GiList.append(Gi)

    # Convert the list of Gi values into a NumPy array
    G = np.array(GiList)

    return G

def buildWmatrix(satList, SigmaUERE2List):
    """
    Build the Weighting Matrix [W] with the inverses of SigmaUERE2
    w = 1 / SigmaUERE2
    """
    # Initialize an empty list to store the Wi values
    Wi_values = []

    if not satList: return np.array([])

    # Loop over all the available satellites
    for i in range(len(satList)):
        usrLosData = satList[i]
        prn = int(usrLosData[UsrLosIdx["PRN"]])
        SigmaUERE2 = SigmaUERE2List[prn]
        Wi = 1 / SigmaUERE2
        Wi_values.append(Wi)

    # Construct the Weighting Matrix (W) as a diagonal matrix with Wi values
    W = np.diag(Wi_values)    

    return W

def computeXpeXplXdops(GPA, WPA, RangeErrors, threshold = 10000):  
    """
        Return [HPE, VPE, HPL, VPL, PDOP, HDOP, VDOP, FLAG]
    """
    # Compute PDOP (Ref.: ESA GNSS Book Vol I Section 6.1.3.2)
    PDOP = computePDOP(GPA);       

    # Check if the PDOP is below a threshold, 10000 by default
    if PDOP > threshold:        
        return [0.0, 0.0, 0.0, 0.0, PDOP, 0.0, 0.0, 0] # FLAG: 0 = "Not Used"
    
    # Compute the Position Error Vector through the LSE process
    [EPE, NPE, UPE] = computePositionErrorVector(GPA, WPA, RangeErrors)

    # Compute the HPE from EPE and NPE
    HPE = math.sqrt(EPE**2 + NPE**2)

    # Compute the Vertical Position Error (VPE) from the absolute value of UPE
    VPE = abs(UPE)

    # Compute Protection levels in line with Appendix J of MOPS
    [HPL, VPL, HDOP, VDOP] = computeProtectionLevels(GPA, WPA)

    return [HPE, VPE, HPL, VPL, PDOP, HDOP, VDOP, 1] # FLAG: 1 = "Used For PA"

def computePDOP(G):
    """
    Compute the Dilution of Precision (DOP) Matrix [Q] and Position Dilution of Precision (PDOP)

    Parameters:
    G (list of lists): Geometry Matrix (G)

    Returns:
    PDOP (float): Position Dilution of Precision (PDOP)
    """
    # Compute the Transposed Geometry Matrix ([G]T)
    GT = np.transpose(G)

    # Compute the DOP Matrix [Q] = ([G]T * G)^-1
    Q = np.linalg.inv(np.dot(GT, G))

    # Calculate the Position Dilution of Precision (PDOP) components
    qE = np.sqrt(Q[0, 0])  # East DOP
    qN = np.sqrt(Q[1, 1])  # North DOP
    qU = np.sqrt(Q[2, 2])  # Up DOP

    # Compute the total PDOP=sqrt(qE^2 + qN^2 + qU^2)
    PDOP = np.sqrt(qE**2 + qN**2 + qU**2)    

    return PDOP

def computeHVDOPs(D):
    """
    Compute Dilution of Precision (DOP) for Position Accuracy (PA) solution

    Parameters:
    D (numpy array): pseudo-inverse of the Weighted Normal Matrix (G^T W G)^-1

    Returns:
    HDOP (float): Horizontal Dilution of Precision
    VDOP (float): Vertical Dilution of Precision
    """
    # Extract the relevant elements from the pseudo-inverse matrix D
    D11 = D[0, 0]
    D22 = D[1, 1]
    D33 = D[2, 2]
    
    # Compute HDOP and VDOP
    HDOP = np.sqrt(D11 + D22)
    VDOP = np.sqrt(D33)

    return HDOP, VDOP

def computePositionErrorVector(G, W, RangeErrors):
    """
    Compute the Position Error Vector through Least Squares Estimation (LSE) process

    Parameters:
    G (numpy array): Geometry Matrix (G)
    W (numpy array): Weighting Matrix (W)
    RangeErrors (list): List of range errors

    Returns:
    pos_error_vector (numpy array): Position Error Vector [EPE, NPE, UPE]
    """

    # Compute Weighted Design Matrix X = [G]T [W]
    X = np.dot(np.transpose(G), W)

    # Compute Normal Matrix N = X [G]
    N = np.dot(X, G)

    # Compute the pseudo-inverse of the Normal Matrix
    N_pinv = np.linalg.pinv(N)

    # Compute the Position Error Vector
    pos_error_vector = np.dot(np.dot(np.dot(N_pinv, np.transpose(G)), W), RangeErrors)
    
    # Return only the first three elements {EPE, NPE, UPE}    
    return pos_error_vector[:3]  

def computeProtectionLevels(G, W):
    """
    Compute Protection Levels in line with Appendix J of MOPS

    Parameters:
    G (numpy array): Geometry Matrix
    W (numpy array): Weighting Matrix

    Returns:
    HPLPA (float): Horizontal Protection Level (HPL)
    VPLPA (float): Vertical Protection Level (VPL)
    """
    # Compute the pseudo-inverse of the Weighted Normal Matrix (G^T W G)^-1
    D = np.linalg.pinv(np.dot(np.dot(np.transpose(G), W), G))   

    # Horizontal/Vertical Dilution of Precision 
    [HDOP, VDOP] = computeHVDOPs(D)

    # Compute intermediate variables
    deast2 = D[0,0]
    dnorth2 = D[1,1]
    dEN = D[1,0]
    dEN2 = dEN**2
    dU2 = D[2,2]
    dU = np.sqrt(dU2)

    # Compute dmajor
    dmajor = np.sqrt( ((deast2 + dnorth2)/2) + np.sqrt( (((deast2 - dnorth2)/2)**2) + dEN2) )

    # Compute the Horizontal Protection Level [HPL= KHPA*dMAJOR (KHPA=6.0)]
    # HPL = 2.576 * np.sqrt(D[0, 0])
    HPL = 6 * dmajor

    # Compute the Vertical Protection Level [VPL= KV dU (KV=5.33)]
    # VPL = 2.576 * np.sqrt(D[2, 2])
    VPL = 5.33 * dU

    return HPL, VPL, HDOP, VDOP

def computeXSI(XPE, XPL):
    """
    Compute Horizontal and Vertical Safety Index (XSI) for Position Accuracy (PA) solution

    Parameters:
    XPE (float): Xorizontal Position Error
    XPL (float): Xorizontal Protection Level

    Returns:
    XSI (float): Xorizontal Safety Index
    """
    # Ensure XPL is not zero to avoid division by zero
    if XPL == 0:
        return float('inf')  # Return infinity if XPL is zero

    # Compute Xorizontal Safety Index
    XSI = XPE / XPL

    return XSI

def computePercentile95(XPE_list, resolution=0.001):
    """
    Compute HPE95% and VPE95%

    Parameters:
    XPE_list (list): List of position error values (either HPE or VPE)
    resolution (float): Resolution for defining statistical XPE bins

    Returns:
    XPE_95 (float): 95th percentile of position error
    """

    if not XPE_list: return 0.0

    # STEP 1: Define statistical XPE bins
    XPE_bins = np.arange(0, max(XPE_list) + resolution, resolution)

    # STEP 2: Count the number of samples falling into each bin
    bin_counts, _ = np.histogram(XPE_list, bins=XPE_bins)

    # STEP 3: Compute the ratio for each statistical bin
    ratios = bin_counts / len(XPE_list)

    # STEP 4: Compute the cumulative sum of the ratios
    cumulative_ratios = np.cumsum(ratios)

    # STEP 5: Find the bin corresponding to the 95th percentile
    percentile_index = np.argmax(cumulative_ratios >= 0.95)

    # Compute the 95th percentile as the upper extreme of the lowest bin
    XPE_95 = XPE_bins[percentile_index]

    return XPE_95


def countTotalSatsOfUsrInEpoch(targetId, UsrLosEpochData):
    counting = False
    totalSats = 0
    for UsrLosData in UsrLosEpochData:
        usrId = int(UsrLosData[UsrLosIdx["USER-ID"]])
        if (targetId == usrId):
            totalSats = totalSats + 1
            counting = True
        elif((targetId != usrId) and (counting == True)):
            # The user has changed, end of counting
            break
    
    return totalSats











# Not used
def updateEpochPos(UsrInfo, InterOutputs, Outputs):
    """
    Update the USR POS for the current epoch based on the LOS data.

    Parameters:
    - UsrInfo: Information for a USR in a single epoch.
    - interOutputs: Intermediate outputs to store computed values for each USR.
    - outputs: Output dictionary containing computed statistics for each USR.

    For each USR in the epoch, it calculates and updates the intermediate outputs
    such as TBD.
    """
    
    # Extract ID Column
    usrId = int(UsrInfo[UsrLosIdx["USER-ID"]])

    # Add Number of samples
    InterOutputs[usrId]["NSAMPS"] = InterOutputs[usrId]["NSAMPS"] + 1

    # Add NTRANS Monitored to Not Monitored (MtoNM) or to Don't USE (MtoDU)
    prevMon = InterOutputs[usrId]["MONPREV"]
    currMon = int(UsrInfo[UsrLosIdx["STATUS"]])
    if(((prevMon == 1) and (currMon == 0)) or ((prevMon == 1) and (currMon == -1))):
        Outputs[usrId]["NTRANS"] += 1      

    updateEpochMaxMinStatsNonMonitored(UsrInfo, usrId, Outputs)

    # Reject if USR STATUS is not OK:
    if(currMon != 1):        
        usrHlp.updatePreviousInterOutputsFromCurrentUsrInfo(InterOutputs, UsrInfo)
        return
    
    # Add Satellite Monitoring if Satellite is Monitored
    Outputs[usrId]["MON"] += 1    

    # Reject if GIVDE_STAT IS NOT OK:
    if(UsrInfo[UsrLosIdx["GIVDE_STAT"]] != '1'): 
        usrHlp.updatePreviousInterOutputsFromCurrentUsrInfo(InterOutputs, UsrInfo)        
        return
    
    # Update number of samples GIVDESAMPS
    InterOutputs[usrId]["GIVDESAMPS"] += 1

    updateEpochMaxMinStatsMonitored(UsrInfo, usrId, Outputs)

    Outputs[usrId]["BAND"] = int(UsrInfo[UsrLosIdx["BAND"]])
    Outputs[usrId]["BIT"] = int(UsrInfo[UsrLosIdx["BIT"]])
    Outputs[usrId]["LON"] = float(UsrInfo[UsrLosIdx["LON"]])
    Outputs[usrId]["LAT"] = float(UsrInfo[UsrLosIdx["LAT"]])

    # Update sum of squared GIVDE values in InterOutputs[usrId]
    InterOutputs[usrId]["GIVDESUM2"] += float(UsrInfo[UsrLosIdx["GIVDE"]])**2
    
    # Update the previous values with the current UsrInfo Values
    usrHlp.updatePreviousInterOutputsFromCurrentUsrInfo(InterOutputs, UsrInfo)

def updateEpochMaxMinStatsNonMonitored(UsrInfo, usrId, Outputs):
    # Update the Minimum Number of IPPs surrounding the USR
    NIPP = int(UsrInfo[UsrLosIdx["NIPP"]])
    if( NIPP < Outputs[usrId]["MINIPPs"]):
        Outputs[usrId]["MINIPPs"] = NIPP
    
    # Update the Maximum Number of IPPs surrounding the USR
    if( NIPP > Outputs[usrId]["MAXIPPs"]):
        Outputs[usrId]["MAXIPPs"] = NIPP        
    
    # Update the Maximun VTEC
    currVTEC = float(UsrInfo[UsrLosIdx["VTEC"]])
    if( currVTEC > Outputs[usrId]["MAXVTEC"]):
        Outputs[usrId]["MAXVTEC"] = currVTEC

def updateEpochMaxMinStatsMonitored(UsrInfo, usrId, Outputs):
    # Update the Maximun GIVD
    currGIVD = float(UsrInfo[UsrLosIdx["GIVD"]])
    if( currGIVD > Outputs[usrId]["MAXGIVD"]):
        Outputs[usrId]["MAXGIVD"] = currGIVD

    # Update the Maximun GIVE
    currGIVE = float(UsrInfo[UsrLosIdx["GIVE"]])
    if( currGIVE > Outputs[usrId]["MAXGIVE"]):
        Outputs[usrId]["MAXGIVE"] = currGIVE

    # Update the Maximun GIVEI
    currGIVEI = float(UsrInfo[UsrLosIdx["GIVEI"]])
    if( currGIVEI > Outputs[usrId]["MAXGIVEI"]):
        Outputs[usrId]["MAXGIVEI"] = currGIVEI 
    
    # Update the Maximun SI
    currSIW = float(UsrInfo[UsrLosIdx["SI-W"]])
    if( currSIW > Outputs[usrId]["MAXSI"]):
        Outputs[usrId]["MAXSI"] = currSIW
    
    # Update the Number of USR MIs (Misleading Information) NMI = SI > 1
    if(currSIW > 1):
        Outputs[usrId]["NMI"] += 1    


def computeFinalStatistics(InterOutputs, Outputs):
    for usrId in Outputs.keys():

        # Rejects Data with no samples
        if(InterOutputs[usrId]["NSAMPS"] <= 0):
            continue

        # Estimate the Monitoring percentage = Monitored epochs / Total epochs
        Outputs[usrId]["MON"] = Outputs[usrId]["MON"] * 100.0 / InterOutputs[usrId]["NSAMPS"]

        # Compute final RMS
        rmsGIVDE = usrHlp.computeUsrRmsFromInterOuputs(InterOutputs, usrId)
        Outputs[usrId]["RMSGIVDE"] = rmsGIVDE        






########################################################################
#END OF USR FUNCTIONS MODULE
########################################################################
