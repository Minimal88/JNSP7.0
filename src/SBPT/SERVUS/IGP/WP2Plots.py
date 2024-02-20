#!/usr/bin/env python

########################################################################
# WP2Plots.py:
# This script defines all internal functions of IgpPerformance Module
#
#  Project:        SBPT
#  File:           WP2Plots.py
#  Date(YY/MM/DD): 24/02/19
#
#   Author: Esteban Martinez Valvere
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
#   IgpStatistics
#   IgpFunctions
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys
import numpy as np
import COMMON.Plots as plt
from COMMON import GnssConstants
from COMMON.Coordinates import xyz2llh
from COMMON.Files import readDataFile
import IgpFunctions as sft
from IgpStatistics import IgpStatsIdx, IgpInfoIdx

# Define relative path
RelativePath = '/OUT/IGP/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def plotMaps(IgpStatsFile, yearDayText):
    
    #Fecth all the columns
    IgpStatsData = readDataFile(IgpStatsFile, IgpStatsIdx.values(), 1)

    # Display the network of RIMS configured in the Scenario
    plotIgpMapMon(IgpStatsData, yearDayText)
    
    return
    

def plotSatStats(satStatsData, yearDayText):
    """
    Plot various satellite statistics based on the provided satellite statistics data.

    Parameters:
        satStatsData (DataFrame): DataFrame containing satellite statistics data.
        yearDayText (str): Year day text for including in plot titles.

    Returns:
        None
    """
    # Plot Satellite Monitoring Percentage
    plotMonPercentage(satStatsData, yearDayText)

    # Plot Number of RIMS
    plotNRIMS(satStatsData, yearDayText)

    # Plot RMS SRE ACR
    plotRmsSreAcr(satStatsData, yearDayText)

    # Plot RMS SREB
    plotRmsSreb(satStatsData, yearDayText)

    # Plot MAX AND RMS SREW
    plotMaxAndRmsSREW(satStatsData, yearDayText)

    # Plot SFLT
    plotMaxMinSFLT(satStatsData, yearDayText)

    # Plot SIW
    plotMaxSIW(satStatsData, yearDayText)
    
    # Plot MAX FC and LTCb
    plotMaxFcAndLTCb(satStatsData, yearDayText)

    # Plot MAX LTCxyz
    plotMaxLTCxyz(satStatsData, yearDayText)

    # Plot MAX NMI
    plotNMI(satStatsData, yearDayText)

    # Plot Number of Transitions
    plotNTRANS(satStatsData, yearDayText)
    
def plotSatStatsTime(SatStatsTimeData, SatInfoFilePath, yearDayText):
    """
    Plot Satellite Statistics against time.

    Parameters:
        SatStatsTimeData (DataFrame): DataFrame containing satellite information data.
        SatInfoFilePath (str): File Path
        yearDayText (str): Year day text for including in plot titles.

    Returns:
        None
    """
    SatInfoData = readDataFile(SatInfoFilePath,[
        IgpInfoIdx["SoD"], IgpInfoIdx["PRN"], IgpInfoIdx["MONSTAT"],IgpInfoIdx["NRIMS"],
        IgpInfoIdx["SREW"], IgpInfoIdx["SFLT-W"], IgpInfoIdx["RDOP"], IgpInfoIdx["SRESTAT"],
        IgpInfoIdx["SAT-X"],IgpInfoIdx["SAT-Y"],IgpInfoIdx["SAT-Z"]])        
    
    # Plot the instantaneous number of satellites monitored as a function of the hour of the day 
    plotMON1(SatStatsTimeData, yearDayText)    

    # Plot the satellites monitoring windows as a function of the hour of the day   
    plotMON2(SatInfoData, yearDayText)
    
    # Plot the satellites ground tracks on a map during monitoring periods    
    plotMON3(SatInfoData, yearDayText)

    # Plot the SREW for all satellites as a function of the hour of the day. PRN in the color bar.
    plotSREWvsPRN(SatInfoData, yearDayText)

    # Plot the SREW for all satellites as a function of the hour of the day. RIMS in the color bar.
    plotSREWvsRIMS(SatInfoData, yearDayText)

    # Plot the SigmaFLT for all satellites as a function of the hour of the day. Inverse Radial DOP in the color bar
    plotSigmaFLTvsIDOP(SatInfoData, yearDayText)

    # Plot the SigmaFLT for all satellites as a function of the hour of the day. Number of RIMS in the color bar
    plotSigmaFLTvsNRIMS(SatInfoData, yearDayText)

    # Plot the SI for all satellites as a function of the hour of the day. PRN in the color bar.
    plotSIvsPRN(SatInfoData, yearDayText)

    #Plot the ENT-GPS Offset along the day
    plotEntGpsOffset(SatStatsTimeData, yearDayText)

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

# Generate a plot with Map for the Monitired Percentage
def plotIgpMapMon(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MON_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: IGP Monitoring Percentage [%] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MON = IgpStatsData[IgpStatsIdx["MON"]]
    MONINT = [int(x) for x in MON]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MON,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"Monitoring [%]", # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MONINT)           # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)
    

def plotMonPercentage(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON_PERCENTAGE_{yearDayText}_G123_50s.png' 
    title = f"Satellite Monitoring Percentage {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    MON = StatsData[IgpStatsIdx["MON"]]
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [MON], "GPS-PRN", ["MON [%]"], ['y'],'upper left' , [-2,6]))

def plotNTRANS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NTRANS_{yearDayText}_G123_50s.png' 
    title = f"Number of Transitions MtoNM or MtoDU {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    NTRANS = StatsData[IgpStatsIdx["NTRANS"]]
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [NTRANS], "GPS-PRN", ["Number of Transitions"], ['y'],'upper right' , [-2,1]))
    
def plotNRIMS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NRIMS_{yearDayText}_G123_50s.png' 
    title = f"Minimun and Maximumgit  Number of RIMS in view {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    RIMSMIN = StatsData[IgpStatsIdx["RIMS-MIN"]]
    RIMSMAX = StatsData[IgpStatsIdx["RIMS-MAX"]]    
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [RIMSMAX,RIMSMIN], "GPS-PRN", ["MAX-RIMS","MIN-RIMS"], ['y','g'],'upper left', [0,10] ))

def plotRmsSreAcr(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_ACR_{yearDayText}_G123_50s.png' 
    title = f"RMS of SREW Along/Cross/Radial along the day {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    SREaRMS = StatsData[IgpStatsIdx["SREaRMS"]]
    SREcRMS = StatsData[IgpStatsIdx["SREcRMS"]]
    SRErRMS = StatsData[IgpStatsIdx["SRErRMS"]]    
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREaRMS,SREcRMS,SRErRMS], 
        "GPS-PRN", ["RMS SRE-A[m]","RMS SRE-C[m]","RMS SRE-R[m]"], 
        ['y','g','r'],'upper left',[0,1]))

def plotRmsSreb(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_B_{yearDayText}_G123_50s.png' 
    title = f"RMS of SRE-B Clock Error Component {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    SREbRMS = StatsData[IgpStatsIdx["SREbRMS"]]       
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREbRMS], 
        "GPS-PRN", ["RMS SRE-B[m]"], 
        ['y'],'upper left',[-0.2,0.1]))

def plotMaxAndRmsSREW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_RMS_SREW_{yearDayText}_G123_50s.png' 
    title = f"RMS and Maximumgit  Value of SRE at the WUL {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    SREWRMS = StatsData[IgpStatsIdx["SREWRMS"]]
    SREWMAX = StatsData[IgpStatsIdx["SREWMAX"]]    
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SREWMAX,SREWRMS], "GPS-PRN", ["MAX SREW[m]","RMS SREW[m]"], ['y','b'],'upper left', [-0.5,0.4] ))

def plotMaxMinSFLT(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_MIN_SigmaFLT_{yearDayText}_G123_50s.png' 
    title = f"Maximumgit  and Minimun SigmaFLT (=SigmaUDRE) {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]
    SFLTMIN = StatsData[IgpStatsIdx["SFLTMIN"]]
    SFLTMAX = StatsData[IgpStatsIdx["SFLTMAX"]]    
    
    plt.generatePlot(plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SFLTMAX,SFLTMIN], "GPS-PRN", ["MAX SFLT[m]","MIN SFLT[m]"], ['y','b'],'upper left', [-0.6,0.7] ))

def plotMaxSIW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_SIW_{yearDayText}_G123_50s.png' 
    title = f"Maximumgit  Satellite Safety Index SI at WUL SREW/5.33UDRE {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')
    
    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]    
    SIMAX = StatsData[IgpStatsIdx["SIMAX"]]    
    SILIM = [1 for l in SIMAX]
    
    PlotConf = plt.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SIMAX,SILIM], 
        "GPS-PRN", ["MAX SI[m]","LIMIT"], 
        ['y','b'],'upper left', [-0.2,0.2] )
    
    PlotConf["Twin"] = {                
        "yLim" : PlotConf["yLim"] ,
        "Label" : "LIMIT"    # Must match with one yLabel        
        }

    plt.generatePlot(PlotConf)

def plotMaxFcAndLTCb(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_FC_LTCb_{yearDayText}_G123_50s.png' 
    title = f"Maximumgit  Satellite Clock Fast and Long Term Corrections {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]    
    FCMAX = StatsData[IgpStatsIdx["FCMAX"]]
    LTCbMAX = StatsData[IgpStatsIdx["LTCbMAX"]]
    
    plt.generatePlot(plt.createPlotConfig2DLines(
        filePath, title, 
        PRN, [FCMAX,LTCbMAX], 
        "GPS-PRN", ["MAX FC[m]","MAX LTCb[m]"], 
        ['y','b'], ['s','s'],
        'upper left', [-0.5,0.7] ))

def plotMaxLTCxyz(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_LTCxyz_{yearDayText}_G123_50s.png' 
    title = f"Maximumgit  Satellite LTC-XYZ {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]    
    LTCxMAX = StatsData[IgpStatsIdx["LTCxMAX"]]
    LTCyMAX = StatsData[IgpStatsIdx["LTCyMAX"]]
    LTCzMAX = StatsData[IgpStatsIdx["LTCzMAX"]]
    
    plt.generatePlot(plt.createPlotConfig2DLines(
        filePath, title, 
        PRN, [LTCxMAX,LTCyMAX,LTCzMAX], 
        "GPS-PRN", ["MAX LTCx[m]","MAX LTCy[m]","MAX LTCz[m]"], 
        ['y','b','g'], ['s','s','s'],
        'upper right', [-0.5,0.7] ))

def plotNMI(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NMIs_{yearDayText}_G123_50s.png' 
    title = f"Number of MIs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[IgpStatsIdx["PRN"]]    
    NMI = StatsData[IgpStatsIdx["NMI"]]    
    
    plt.generatePlot(plt.createPlotConfig2DLines(
        filePath, title, 
        PRN, [NMI], 
        "GPS-PRN", ["NMIs"], 
        ['y'], ['_'],
        'upper right', [-0.05,1] ))

def plotMON1(SatStatsTimeData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON1_{yearDayText}_G123_50s.png' 
    title = f"Number of Satellites Monitored EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatStatsTimeData[IgpStatsTimeIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    MON = SatStatsTimeData[IgpStatsTimeIdx["MON"]]    
    NMON = SatStatsTimeData[IgpStatsTimeIdx["NMON"]]   
    DU = SatStatsTimeData[IgpStatsTimeIdx["DU"]]   
    
    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD, [MON,NMON,DU], 
        "Hour of Day", ["MON","NOT-MON","DONT USE"], 
        ['y','g','b'], [',',',',','],
        'upper right', [-0.1,5] )
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    plt.generatePlot(PlotConf)


# Plot the satellites monitoring windows as a function of the hour of the day
def plotMON2(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON2_{yearDayText}_G123_50s.png' 
    title = f"Satellites Monitoring EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    FilterCond = SatInfoData[IgpInfoIdx["MONSTAT"]] == 1
    xData = SatInfoData[IgpInfoIdx["SoD"]][FilterCond] / GnssConstants.S_IN_H
    yData = [int(s[1:]) for s in SatInfoData[IgpInfoIdx["PRN"]][FilterCond]]    
    zData = SatInfoData[IgpInfoIdx["NRIMS"]][FilterCond]

    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        xData, yData, zData,                            # xData, yData, zData 
        "Hour of Day", "GPS-PRN", "Number of RIMS",     # xLabel, yLabel, zLabel 
        '|' , False)                                    # marker, applyLimits
    
    PlotConf["LineWidth"] = 2
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["yTicks"] = range(0,33)
    PlotConf["yLim"] = [0, 32]    
    
    plt.generatePlot(PlotConf)

# Plot the satellites ground tracks on a map during monitoring periods
def plotMON3(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON3_{yearDayText}_G123_50s.png' 
    title = f"Satellites Tracks during Monitoring Periods EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MONSTAT = SatInfoData[IgpInfoIdx["MONSTAT"]]    
    NRIMS = SatInfoData[IgpInfoIdx["NRIMS"]]

    # Transform ECEF to Geodetic
    SatInfoData[IgpInfoIdx["SAT-X"]].to_numpy()                       
    SatInfoData[IgpInfoIdx["SAT-Y"]].to_numpy()
    SatInfoData[IgpInfoIdx["SAT-Z"]].to_numpy()

    LONG = np.array([])
    LAT = np.array([])
    NRIMS_FILT = np.array([])

    for index in range(len(SatInfoData[IgpInfoIdx["SAT-X"]])):
        mon = MONSTAT[index]
        if (mon != 1): # Discard data where monstat is not good
            continue            
        x = SatInfoData[IgpInfoIdx["SAT-X"]][index] * 1000
        y = SatInfoData[IgpInfoIdx["SAT-Y"]][index] * 1000
        z = SatInfoData[IgpInfoIdx["SAT-Z"]][index] * 1000        
        long, lat, alt = xyz2llh(x, y, z)
        LONG = np.append(LONG, long)
        LAT = np.append(LAT, lat)
        NRIMS_FILT = np.append(NRIMS_FILT, NRIMS[index])
    
    PlotConf = plt.createPlotConfig2DLinesColorBar(filePath, title, 
        LONG, LAT, NRIMS_FILT,                                  # xData, yData, zData 
        "LON [deg]", "LAT [deg]", "Number of RIMS",             # xLabel, yLabel, zLabel 
        '.' , False)                                            # marker, applyLimits
    
    PlotConf["Map"] = True    
    PlotConf["LonMin"] = -135
    PlotConf["LonMax"] = 135
    PlotConf["LatMin"] = -70
    PlotConf["LatMax"] = 90
    PlotConf["LonStep"] = 15
    PlotConf["LatStep"] = 10
    PlotConf["xTicks"] = range(PlotConf["LonMin"],PlotConf["LonMax"]+1,15)
    PlotConf["xLim"] = [PlotConf["LonMin"], PlotConf["LonMax"]]
    PlotConf["yTicks"] = range(PlotConf["LatMin"],PlotConf["LatMax"]+1,10)
    PlotConf["yLim"] = [PlotConf["LatMin"], PlotConf["LatMax"]]
    
    plt.generatePlot(PlotConf)

# Plot the SREW for all satellites as a function of the hour of the day. PRN in the color bar.
def plotSREWvsPRN(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SREW_PRN_{yearDayText}_G123_50s.png' 
    title = f"Satellites SREW vs PRN EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    PRN = SatInfoData[IgpInfoIdx["PRN"]]  
    SREW = SatInfoData[IgpInfoIdx["SREW"]]    
    PRN_NUM = [int(s[1:]) for s in PRN]    

    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        HOD, SREW, PRN_NUM,                             # xData, yData, zData 
        "Hour of Day", "SREW [m]", "GPS-PRN",           # xLabel, yLabel, zLabel 
        '.' , False)                                    # marker, applyLimits
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["ColorBarTicks"] = range(max(PRN_NUM))
    
    plt.generatePlot(PlotConf)

# Plot the SREW for all satellites as a function of the hour of the day. RIMS in the color bar.
def plotSREWvsRIMS(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SREW_RIMS_{yearDayText}_G123_50s.png' 
    title = f"Satellites SREW vs RIMS EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    SREW = SatInfoData[IgpInfoIdx["SREW"]]          
    NRIMS = SatInfoData[IgpInfoIdx["NRIMS"]]    

    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        HOD, SREW, NRIMS,                            # xData, yData, zData 
        "Hour of Day", "SREW [m]", "NUM - RIMS",     # xLabel, yLabel, zLabel 
        '.' , False)                                 # marker, applyLimits
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]    
    
    plt.generatePlot(PlotConf)


# Plot the SigmaFLT for all satellites as a function of the hour of the day
# Inverse Radial DOP in the color bar
def plotSigmaFLTvsIDOP(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SFLT_IDOP_{yearDayText}_G123_50s.png' 
    title = f"Satellites SigmaFLT at WUL IR-DOP EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    RDOP = SatInfoData[IgpInfoIdx["RDOP"]]
    SFLTW = SatInfoData[IgpInfoIdx["SFLT-W"]]    
    
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        HOD, SFLTW, RDOP,                                              # xData, yData, zData 
        "Hour of Day", "SigmaFLT [m]", "Inverse Radial DOP",           # xLabel, yLabel, zLabel 
        '.' , False)                                                   # marker, applyLimits
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]   
    PlotConf["ColorBarMin"] = 0
    PlotConf["ColorBarMax"] = 100
    
    plt.generatePlot(PlotConf)

# Plot the SigmaFLT for all satellites as a function of the hour of the day
# Number of RIMS in the color bar
def plotSigmaFLTvsNRIMS(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SFLT_NRIMS_{yearDayText}_G123_50s.png' 
    title = f"Satellites SigmaFLT at WUL vs NRIMS EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    SFLTW = SatInfoData[IgpInfoIdx["SFLT-W"]]    
    NRIMS = SatInfoData[IgpInfoIdx["NRIMS"]]    

    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        HOD, SFLTW, NRIMS,                                             # xData, yData, zData 
        "Hour of Day", "SigmaFLT [m]", "RIMS",                         # xLabel, yLabel, zLabel 
        '.' , False)                                                   # marker, applyLimits
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    
    plt.generatePlot(PlotConf)

# Plot the SI for all satellites as a function of the hour of the day. PRN in the color bar.
def plotSIvsPRN(SatInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SI_PRN_{yearDayText}_G123_50s.png' 
    title = f"Satellites SREW/5.33S igmaFLT at WUL EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    PRN = SatInfoData[IgpInfoIdx["PRN"]]  
    SREW = SatInfoData[IgpInfoIdx["SREW"]]    
    SFLT = SatInfoData[IgpInfoIdx["SFLT-W"]]    
    SRESTAT = SatInfoData[IgpInfoIdx["SRESTAT"]]    

    SI = np.array([])
    HOD_FILT = np.array([])
    PRN_FILT = np.array([])

    for i in range (len(SREW)):
        # Reject if satellite is not MONITORED:
        mon  = SRESTAT[i]
        if(mon != 1):
            continue
        HOD_FILT = np.append(HOD_FILT, HOD[i])
        PRN_FILT = np.append(PRN_FILT, PRN[i])        
        SI = np.append(SI, SREW[i] / (SFLT[i]*5.33))

    PRN_NUM = [int(s[1:]) for s in PRN_FILT]

    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        HOD_FILT, SI, PRN_NUM  ,                             # xData, yData, zData 
        "Hour of Day", "SI", "GPS-PRN",                 # xLabel, yLabel, zLabel 
        '.' , False)                                    # marker, applyLimits
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]      
    PlotConf["ColorBarTicks"] = range(max(PRN_NUM))
    
    plt.generatePlot(PlotConf)
