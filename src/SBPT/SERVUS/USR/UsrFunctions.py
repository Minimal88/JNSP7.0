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
def computeUsrPosAndPerf(UsrLosFilePath, UsrPosFilePath, UsrPerfFilePath, Conf):
    # Define and Initialize Variables            
    UsrPosEpochOutputs = OrderedDict({})
    UsrPerfOutputs = OrderedDict({})
    UsrPerfInterOutputs = OrderedDict({})
    EndOfFile = False
    UsrLosEpochData = []
    # Initialize Outputs
    usrHlp.initializePosEpochOutputs(UsrPosEpochOutputs)
    usrHlp.initializePerfOutputs(UsrPerfOutputs)
    usrHlp.initializeInterPerfOutputs(UsrPerfInterOutputs)

    # Open USR LOS File
    fUserLos = open(UsrLosFilePath, 'r')
    # Open Output USR POS File 
    fPosFile = open(UsrPosFilePath, 'w')
    
    # Read header line of USR LOS File
    fUserLos.readline()
    
    # Write Header of POS file
    # header_string = usrHlp.delim.join(UsrPosIdx) + "\n"
    header_string = "#   SOD  USER-ID   ULON       ULAT     SOL-FLAG   NVS   NVS-PA    HPE        VPE        HPL        VPL        HSI        VSI        PDOP       HDOP       VDOP\n"
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
            usrEpochRangeErrors_Vector = []
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
                NSatsOfUsrInEpoch = countTotalSatsOfUsrInEpoch(usrId, UsrLosEpochData)
                usrSatIndex = usrSatIndex + 1

                # Update the UsrPosOuputs for SOD, ULON, ULAT
                usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {
                    "SOD": SOD, "ULON": ULON, "ULAT":ULAT})

                # Update the UsrPerfOutputs
                usrHlp.updatePerfOutputs(UsrPerfOutputs, usrId, {
                    "ULON": ULON, "ULAT":ULAT})

                # LOOP Over all Satellites, and filter them
                # ----------------------------------------------------------
                # Count Sats with ELEV angle more than 5 degree
                if (float(UsrLosData[UsrLosIdx["ELEV"]]) > int(Conf["USER_MASK"])):
                    NVS = NVS + 1

                    # Consider Sats only with Flag == 1 (Consider only PA Solutions)
                    if (int(UsrLosData[UsrLosIdx["FLAG"]]) == 1):
                        usrAvlSatList.append(UsrLosData)
                        NVSPA = NVSPA + 1

                        # Build Ranging Error Vector by adding all the different contributors
                        RangeError = computeRangingError(UsrLosData)
                        usrEpochRangeErrors_Vector.append(RangeError)

                        # Build the SigmaUERE2 in line with MOPS Standard
                        SigmaUERE2 = computeSigmaUERE2(UsrLosData)
                        usrEpochSigmaUERE2_Dict[PRN] = SigmaUERE2


                # If reached the end of satellites on the EPOCH for the current user
                if (usrSatIndex == NSatsOfUsrInEpoch):
                    usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {"NVS": NVS, "NVS-PA": NVSPA})
                    SOL_FLAG = PDOP = HDOP = VDOP = HPE = VPE = HPL = VPL = HSI = VSI = 0

                    # Compute PA Solution if at least 4 Satellites are valid for solution                    
                    if NVSPA >= 4:                                
                        # Build Geometry [G] matrix in line with SBAS Standard                                
                        GPA = buildGmatrix(usrAvlSatList)

                        # Compute PDOP (Ref.: ESA GNSS Book Vol I Section 6.1.3.2)
                        [PDOP, HDOP, VDOP] = computeXDOPs(GPA);

                        # Check if the PDOP is under the UsrConf threshold (10000)
                        if PDOP <= int(Conf["PDOP_MAX"]):        
                            # Build Weighting [W] matrix in line with SBAS Standards                                
                            WPA= buildWmatrix(usrAvlSatList, usrEpochSigmaUERE2_Dict)

                            # Compute Position Errors and Protection levels. XPE, XPL                                
                            [HPE, VPE, HPL, VPL] = computeXpeXpl(GPA, WPA, usrEpochRangeErrors_Vector)

                            HSI = computeXSI(HPE, HPL)
                            VSI = computeXSI(VPE, VPL)
                            SOL_FLAG = 1
                        
                    # Update the UsrPosOuputs for SOL-FLAG, NVSPA, HPE, Nvs5, VPE, HPL, VPL
                    usrHlp.updatePosOutputs(UsrPosEpochOutputs, usrId, {
                        "SOL-FLAG":SOL_FLAG, "HPE":HPE, "VPE":VPE, 
                        "HPL":HPL, "VPL":VPL, "HSI":HSI, "VSI":VSI, 
                        "PDOP":PDOP, "HDOP":HDOP, "VDOP":VDOP})
                    
                    # Reset Loop variable, for the next iteration
                    usrAvlSatList = []   
                    usrEpochSigmaUERE2_Dict = {}
                    usrEpochRangeErrors_Vector = []
                    NVSPA = 0
                    NVS = 0
                    usrSatIndex = 0                    

            # END OF LOOP For ALL Users in the current EPOCH

            # Write USR POS File with the all the Usrs of the EPOCH            
            usrHlp.WriteUsrsEpochPosFile(fPosFile, UsrPosEpochOutputs)
            
            computeUsrEpochPerfomances(UsrPosEpochOutputs, UsrPerfOutputs, UsrPerfInterOutputs)

        else:
            EndOfFile = True
            # Close the all the open files
            fUserLos.close()
            fPosFile.close()
        # END OF LOOP over all Users Information on each Epoch:
    # END OF LOOP for all Epochs of USR LOS file      
    del UsrPosEpochOutputs
    computeUsrFinalPerformances(UsrPerfOutputs, UsrPerfInterOutputs)

    # Open Output USR Perf File 
    fPerfFile = open(UsrPerfFilePath, 'w')    
    # Write Header of PERF file
    # header_string = usrHlp.delim.join(UsrPerfIdx) + "\n"
    header_string = "USER-ID     ULON       ULAT    SOLSAMP  NVS-MIN NVS-MAX    AVAILSAMP AVAILABILITY   HPE-RMS    VPE-RMS    HPE-95     VPE-95     HPE-MAX    VPE-MAX    HSI-MAX    VSI-MAX   HPL-MAX    VPL-MAX    HPL-MIN    VPL-MIN     HDOP-MAX   VDOP-MAX   PDOP-MAX\n"
    fPerfFile.write(header_string)

    # Write the USR PERF file with all the data from UsrPerfOutputs
    usrHlp.WriteAllUsrPerfFile(fPerfFile, UsrPerfOutputs)
    fPerfFile.close()  



# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def displayUsage():
    """
    FUNCTION: Display Message
    """
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")

def computeRangingError(UsrLosData):
    """
        Compute Ranging Error by adding all the different contributors 
        RANGEERROR = SREU + UISDE + TropoE + AirE
    """
    SREU = float(UsrLosData[UsrLosIdx["SREU"]])
    UISDE = float(UsrLosData[UsrLosIdx["UISDE"]])
    TropoE = float(UsrLosData[UsrLosIdx["STROPOE"]])
    AirE = float(UsrLosData[UsrLosIdx["AIRERR"]])

    return SREU + UISDE + TropoE + AirE

def computeSigmaUERE2(UsrLosData):
    """
        Build the SigmaUERE2 in line with MOPS Standard
        SigmaUERE2 = SigmaFLT2 + SigmaUIRE2 + SigmaTropo2 + SigmaAIR2
    """

    SigmaFLT2 = float(UsrLosData[UsrLosIdx["SFLT"]]) ** 2
    SigmaUIRE2 = float(UsrLosData[UsrLosIdx["UIRE"]]) ** 2
    SigmaTropo2 = float(UsrLosData[UsrLosIdx["SIGMTROPO"]]) ** 2
    SigmaAIR2 = float(UsrLosData[UsrLosIdx["SIGMAIR"]]) ** 2
    
    return SigmaFLT2 + SigmaUIRE2 + SigmaTropo2 + SigmaAIR2

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

def computeXpeXpl(GPA, WPA, RangeErrors):  
    """
        Return [HPE, VPE, HPL, VPL]
    """    
    
    # Compute the Position Error Vector through the LSE process
    [EPE, NPE, UPE] = computePositionErrorVector(GPA, WPA, RangeErrors)

    # Compute the HPE from EPE and NPE
    HPE = math.sqrt(EPE**2 + NPE**2)

    # Compute the Vertical Position Error (VPE) from the absolute value of UPE
    VPE = abs(UPE)

    # Compute Protection levels in line with Appendix J of MOPS
    [HPL, VPL] = computeProtectionLevels(GPA, WPA)

    return [HPE, VPE, HPL, VPL]

def computeXDOPs(G):
    """
    Compute the Position/Horizontal/Vertical Dilution of Precision

    Parameters:
    G (list of lists): Geometry Matrix (G)

    Returns:
    PDOP (float): Position Dilution of Precision (PDOP)
    HDOP (float): Horizontal Dilution of Precision (HDOP)
    VDOP (float): Vertical Dilution of Precision (VDOP)
    """
    # Compute the Transposed Geometry Matrix ([G]T)
    GT = np.transpose(G)

    # Compute the DOP Matrix [Q] = ([G]T * G)^-1
    Q = np.linalg.inv(np.dot(GT, G))

    # Compute the Position Dilution of Precision (PDOP) components
    qE = np.sqrt(Q[0, 0])  # East DOP
    qN = np.sqrt(Q[1, 1])  # North DOP
    qU = np.sqrt(Q[2, 2])  # Up DOP

    # Compute the total PDOP=sqrt(qE^2 + qN^2 + qU^2)
    PDOP = np.sqrt(qE**2 + qN**2 + qU**2)    

    # Compute Horizontal Dilution of Precision (HDOP)
    HDOP = np.sqrt(qE**2 + qN**2)

    # Compute Vertical Dilution of Precision (VDOP)
    VDOP = qU

    return PDOP, HDOP, VDOP

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

    return HPL, VPL

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


def computeRmsFromList(List):
    """
    Compute the Root Mean Square (RMS)

    Parameters:
    - List: NumPy array or list of values.

    Returns:
    - RMS: RMS value from the List of samples.
    """
    if len(List) == 0:
        return 0

    # Calculate RMS value
    RMS = np.sqrt(np.mean(np.square(List)))

    return RMS

def computeUsrEpochPerfomances(UsrPosEpochOutputs, UsrPerfOutputs, UsrPerfInterOutputs):
    HAL = 40
    VAL = 50

    # Loop over all the Users in the current EPOCH 
    for UsrPosData in UsrPosEpochOutputs.values():
        usrId = UsrPosData["USER-ID"]
        solFlag = UsrPosData["SOL-FLAG"]
        NVSPA = UsrPosData["NVS-PA"]
        HPE = UsrPosData["HPE"]
        VPE = UsrPosData["VPE"]
        HPL = UsrPosData["HPL"]
        VPL = UsrPosData["VPL"]
        HDOP = UsrPosData["HDOP"]
        VDOP = UsrPosData["VDOP"]
        PDOP = UsrPosData["PDOP"]
        HSI = UsrPosData["HSI"]
        VSI = UsrPosData["VSI"]
        
        UsrPerfInterOutputs[usrId]["TotalSamples"] = UsrPerfInterOutputs[usrId]["TotalSamples"] + 1

        if (solFlag == 1):
            UsrPerfOutputs[usrId]["SOLSAMP"] = UsrPerfOutputs[usrId]["SOLSAMP"] + 1
            
            if (UsrPerfOutputs[usrId]["NVS-MAX"] < NVSPA):
                UsrPerfOutputs[usrId]["NVS-MAX"] = NVSPA

            if (UsrPerfOutputs[usrId]["NVS-MIN"] > NVSPA):
                UsrPerfOutputs[usrId]["NVS-MIN"] = NVSPA
            
            if (UsrPerfOutputs[usrId]["HSI-MAX"] < HSI):
                UsrPerfOutputs[usrId]["HSI-MAX"] = HSI
            
            if (UsrPerfOutputs[usrId]["VSI-MAX"] < VSI):
                UsrPerfOutputs[usrId]["VSI-MAX"] = VSI

            if (HPL < HAL) and (VPL < VAL) and (HPL > 0) and (VPL > 0) and (NVSPA >= 4):
                UsrPerfOutputs[usrId]["AVAILSAMP"] = UsrPerfOutputs[usrId]["AVAILSAMP"] + 1

                UsrPerfInterOutputs[usrId]["HPE_list"].append(HPE)
                UsrPerfInterOutputs[usrId]["VPE_list"].append(VPE)

                if (UsrPerfOutputs[usrId]["HPE-MAX"] < HPE):
                    UsrPerfOutputs[usrId]["HPE-MAX"] = HPE
                
                if (UsrPerfOutputs[usrId]["VPE-MAX"] < VPE):
                    UsrPerfOutputs[usrId]["VPE-MAX"] = VPE

                if (UsrPerfOutputs[usrId]["HPL-MAX"] < HPL):
                    UsrPerfOutputs[usrId]["HPL-MAX"] = HPL
                
                if (UsrPerfOutputs[usrId]["VPL-MAX"] < VPL):
                    UsrPerfOutputs[usrId]["VPL-MAX"] = VPL

                if (UsrPerfOutputs[usrId]["HPL-MIN"] > HPL):
                    UsrPerfOutputs[usrId]["HPL-MIN"] = HPL
                
                if (UsrPerfOutputs[usrId]["VPL-MIN"] > VPL):
                    UsrPerfOutputs[usrId]["VPL-MIN"] = VPL
                
                if (UsrPerfOutputs[usrId]["HDOP-MAX"] < HDOP):
                    UsrPerfOutputs[usrId]["HDOP-MAX"] = HDOP

                if (UsrPerfOutputs[usrId]["VDOP-MAX"] < VDOP):
                    UsrPerfOutputs[usrId]["VDOP-MAX"] = VDOP
                
                if (UsrPerfOutputs[usrId]["PDOP-MAX"] < PDOP):
                    UsrPerfOutputs[usrId]["PDOP-MAX"] = PDOP

def computeUsrFinalPerformances(UsrPerfOutputs, UsrPerfInterOutputs):
    for usrId in UsrPerfOutputs.keys():
        HPE_List = UsrPerfInterOutputs[usrId]["HPE_list"]
        VPE_List = UsrPerfInterOutputs[usrId]["VPE_list"]
        
        if (len(HPE_List) > 0) and ((len(VPE_List) > 0)):
            HPERMS = computeRmsFromList(HPE_List)
            VPERMS = computeRmsFromList(VPE_List)
            UsrPerfOutputs[usrId]["HPE-RMS"] = HPERMS
            UsrPerfOutputs[usrId]["VPE-RMS"] = VPERMS

            HPE95 = np.percentile(HPE_List, 95)
            VPE95 = np.percentile(VPE_List, 95)
            UsrPerfOutputs[usrId]["HPE-95"] = HPE95
            UsrPerfOutputs[usrId]["VPE-95"] = VPE95
        
        HPL_MIN = UsrPerfOutputs[usrId]["HPL-MIN"]
        if(UsrPerfOutputs[usrId]["HPL-MIN"] == 1000000000000):
            UsrPerfOutputs[usrId]["HPL-MIN"] = 0
        
        if(UsrPerfOutputs[usrId]["VPL-MIN"] == 1000000000000):
            UsrPerfOutputs[usrId]["VPL-MIN"] = 0
        
        if(UsrPerfOutputs[usrId]["NVS-MIN"] == 1000000000000):
            UsrPerfOutputs[usrId]["NVS-MIN"] = 0
        
        TotalSamples = UsrPerfInterOutputs[usrId]["TotalSamples"]
        if (TotalSamples != 0):
            UsrPerfOutputs[usrId]["AVAILABILITY"] = (UsrPerfOutputs[usrId]["AVAILSAMP"] / TotalSamples) * 100


########################################################################
#END OF USR FUNCTIONS MODULE
########################################################################
