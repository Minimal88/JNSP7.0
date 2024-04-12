#!/usr/bin/env python

########################################################################
# WP3Plots.py:
# This script defines all internal functions of UsrPerformance Module
#
#  Project:        SBPT
#  File:           WP3Plots.py
#  Date(YY/MM/DD): 24/03/25
#
#   Author: Esteban Martinez Valvere
#   Copyright 2024 GNSS Academy
# 
# Internal dependencies:
#   COMMON
#   UsrStatistics
#   UsrFunctions
########################################################################
import sys, os
projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, projectDir)

# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys
import numpy as np
import pandas as pd
import COMMON.Plots as plt
from COMMON import GnssConstants
from COMMON.Files import readDataFile
import UsrFunctions as sft
from UsrHelper import UsrPosIdx, UsrLosIdx

# Define relative path
RelativePath = '/OUT/USR/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def plotUsrStatsMaps(UsrStatsFile, yearDayText):    
    # Fecth all the columns
    UsrStatsData = readDataFile(UsrStatsFile, UsrPosIdx.values(), 1)

    plotUsrMapMon(UsrStatsData, yearDayText)

    plotUsrMapMinNIPPs(UsrStatsData, yearDayText)

    plotUsrMapMaxNIPPs(UsrStatsData, yearDayText)

    plotUsrMapMaxVTEC(UsrStatsData, yearDayText)

    plotUsrMapMaxGIVD(UsrStatsData, yearDayText)

    plotUsrMapMaxRMSGIVDE(UsrStatsData, yearDayText)

    plotUsrMapMaxGIVE(UsrStatsData, yearDayText)

    plotUsrMapMaxGIVEi(UsrStatsData, yearDayText)

    plotUsrMapMaxSI(UsrStatsData, yearDayText)

    plotUsrMapNTRANS(UsrStatsData, yearDayText)

    plotUsrMapNMI(UsrStatsData, yearDayText)
    return

def plotUsrInfoTime(UsrInfoFile, yearDayText):

    positions = {
    "CNTR": {"LAT": 45, "LON": 5},
    "SW-1": {"LAT": 20, "LON": -20},
    "SW-2": {"LAT": 20, "LON": 35},
    "NW-1": {"LAT": 65, "LON": -20},
    "NW-2": {"LAT": 60, "LON": 35}
}
    
    # Fecth target columns
    UsrInfoData = readDataFile(UsrInfoFile, [
        UsrLosIdx["SoD"], 
        UsrLosIdx["STATUS"],
        UsrLosIdx["LAT"],
        UsrLosIdx["LON"],
        UsrLosIdx["GIVEI"],
        UsrLosIdx["GIVDE"],
        UsrLosIdx["GIVE"],
        UsrLosIdx["GIVD"],
        UsrLosIdx["GIVEI"],
        UsrLosIdx["VTEC"]
        ], 1)

    plotUsrTimeMon(UsrInfoData, yearDayText)

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for USR CENTER
    plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, positions["CNTR"], "CENTER")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for USR SOUTH 1
    plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, positions["SW-1"], "SW-1")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for USR SOUTH 2
    plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, positions["SW-2"], "SW-2")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for USR NORTH 1
    plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, positions["NW-1"], "NW-1")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for USR SOUTH 2
    plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, positions["NW-2"], "NW-2")
    

    # Plot GIVD and VTEC Evolution along the day for USR CENTER
    plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, positions["CNTR"], "CENTER")

    # Plot GIVD and VTEC Evolution along the day for SOUTH 1
    plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, positions["SW-1"], "SW-1", [0 , 5])

    # Plot GIVD and VTEC Evolution along the day for SOUTH 2
    plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, positions["SW-2"], "SW-2", [0 , 4])

    # Plot GIVD and VTEC Evolution along the day for NORTH 1
    plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, positions["NW-1"], "NW-1")

    # Plot GIVD and VTEC Evolution along the day for NORTH 2
    plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, positions["NW-2"], "NW-2")


    # Plot VTEC Evolution along the day for all the positions
    plotUsrTimeVtecAllPositions(UsrInfoData, yearDayText, positions)

    # Plot SI (Safey Index) Evolution along the day for all the positions
    plotUsrTimeSiAllPositions(UsrInfoData, yearDayText, positions)
    

    return

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

# Generate a plot with Map for the USR Monitired Percentage
def plotUsrMapMon(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MON_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: USR Monitoring Percentage [%] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MON = UsrStatsData[UsrPosIdx["MON"]]
    MONINT = [int(x) for x in MON]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

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
    
# Generate a plot with Map for the USR Minimum NIPPs
def plotUsrMapMinNIPPs(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MIN_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Minimum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MINIPPs = UsrStatsData[UsrPosIdx["MINIPPs"]]
    MINIPPsINT = [int(x) for x in MINIPPs]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MINIPPs,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MIN NIPPs",      # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MINIPPsINT)       # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum NIPPs
def plotUsrMapMaxNIPPs(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXIPPs = UsrStatsData[UsrPosIdx["MAXIPPs"]]
    MAXIPPsINT = [int(x) for x in MAXIPPs]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXIPPs,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX NIPPs",      # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXIPPsINT)       # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum VTEC
# TODO: Check the values of this plot, something is off
def plotUsrMapMaxVTEC(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_VTEC_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum VTEC [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXVTEC = UsrStatsData[UsrPosIdx["MAXVTEC"]]
    MAXVTECFLOAT = [round(float(x), 1) for x in MAXVTEC]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXVTEC,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX VTEC [m]",   # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXVTECFLOAT)     # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum GIVD
def plotUsrMapMaxGIVD(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVD_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVD [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVD = UsrStatsData[UsrPosIdx["MAXGIVD"]]
    MAXGIVDFLOAT = [round(float(x), 1) for x in MAXGIVD]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXGIVD,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX GIVD [m]",   # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXGIVDFLOAT)     # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR RMS GIVD Error
def plotUsrMapMaxRMSGIVDE(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_RMS_GIVDE_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: RMS GIVD Error [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    RMSGIVDE = UsrStatsData[UsrPosIdx["RMSGIVDE"]]
    RMSGIVDEFLOAT = [round(float(x), 1) for x in RMSGIVDE]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , RMSGIVDE,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"RMS GIVDE [m]",   # xLabel, yLabel, zLabel
        's', False)                                  # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, RMSGIVDEFLOAT)    # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum GIVE
def plotUsrMapMaxGIVE(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVE_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVE [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVE = UsrStatsData[UsrPosIdx["MAXGIVE"]]
    MAXGIVEFLOAT = [round(float(x), 1) for x in MAXGIVE]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXGIVE,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX GIVE [m]",   # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXGIVEFLOAT)     # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum GIVEi
def plotUsrMapMaxGIVEi(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVEi_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVEi [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVEi = UsrStatsData[UsrPosIdx["MAXGIVEI"]]
    MAXGIVEiFLOAT = [round(float(x), 1) for x in MAXGIVEi]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXGIVEi,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX GIVEi [m]",   # xLabel, yLabel, zLabel
        's', False)                                 # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXGIVEiFLOAT)     # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR Maximum SI
def plotUsrMapMaxSI(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_SI_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum SI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXSI = UsrStatsData[UsrPosIdx["MAXSI"]]
    MAXSIFLOAT = [round(float(x), 1) for x in MAXSI]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , MAXSI,                        # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX SI",       # xLabel, yLabel, zLabel
        's', False)                               # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, MAXSIFLOAT)    # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

# Generate a plot with Map for the USR NTRANS Number of Transitions
def plotUsrMapNTRANS(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_NTRANS_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Number of Transitions MtoNM MtoDU {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NTRANS = UsrStatsData[UsrPosIdx["NTRANS"]]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , NTRANS,                        # xData, yData, zData
        "Longitude [deg]", yLabel," NTRANS",       # xLabel, yLabel, zLabel
        's', False)                                # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, NTRANS)           # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)    

# Generate a plot with Map for the USR NMI Number of MI
def plotUsrMapNMI(UsrStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_NMI_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Number of MI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NMI = UsrStatsData[UsrPosIdx["NMI"]]
    LON = UsrStatsData[UsrPosIdx["LON"]]    
    LAT = UsrStatsData[UsrPosIdx["LAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , NMI,                        # xData, yData, zData
        "Longitude [deg]", yLabel," NMI",       # xLabel, yLabel, zLabel
        's', False)                             # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -65, 85, 10,              # LonMin, LonMax, LonStep
        0, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, NMI)              # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)    


# Generate a plot with the Number of Monitored/ Not Monitored / DU USRs 
def plotUsrTimeMon(UsrInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_TIME_MON_{yearDayText}_G123_50s.png' 
    title = f"Number of USR Monitored EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns        
    HOD = UsrInfoData[UsrLosIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours    
    MON = UsrInfoData[UsrLosIdx["STATUS"]]
    HOD_FILT = np.unique(HOD)
    arraySize = len(HOD_FILT)    
    MON_FILT = np.zeros(arraySize)
    NMON_FILT = np.zeros(arraySize)
    DU_FILT = np.zeros(arraySize)    

    # Loop through unique HOD values (Each EPOCH)
    for i, hod in enumerate(HOD_FILT):

        # Boolean mask for current HOD
        mask = (HOD == hod)  

        # Count number of Mon/NMon/DU for the current EPOCH
        MON_FILT[i] = (MON[mask] == 1).sum()          
        NMON_FILT[i] = (MON[mask] == 0).sum() 
        DU_FILT[i] = (MON[mask] == -1).sum()

    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD_FILT, [MON_FILT,NMON_FILT,DU_FILT],         
        "Hour of Day", ["MON","NOT-MON","DONT USE"], 
        ['g','r','b'], ['s','s','s'],
        'upper right', [-0.2,30] )
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["LineStyle"] = 'None'
    PlotConf["LineWidth"] = 1
    plt.generatePlot(PlotConf)


# Generate a Plot with the GIVDE, GIVE, GIVEi and Monitoring flag along the hour of the day for a specific Lon|Lat.
def plotUsrTimeGivdeGiveGiveiMon(UsrInfoData, yearDayText, pos, posLabel):
    filePath = sys.argv[1] + f'{RelativePath}USR_TIME_GIVDE_GIVE_GIVEI_{posLabel}_{yearDayText}_G123_50s.png' 
    lon = pos["LON"]
    lat = pos["LAT"]
    title = f"USR {posLabel} [Lon|Lat]:[{lon}:{lat}] {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns
    FilterCondLon = UsrInfoData[UsrLosIdx["LON"]] == lon
    FilterCondLat = UsrInfoData[UsrLosIdx["LAT"]] == lat
    HOD = UsrInfoData[UsrLosIdx["SoD"]][FilterCondLat][FilterCondLon] / GnssConstants.S_IN_H  # Converting to hours    
    MON = UsrInfoData[UsrLosIdx["STATUS"]][FilterCondLat][FilterCondLon]
    GIVDE = UsrInfoData[UsrLosIdx["GIVDE"]][FilterCondLat][FilterCondLon]
    GIVE = UsrInfoData[UsrLosIdx["GIVE"]][FilterCondLat][FilterCondLon]
    GIVEI = UsrInfoData[UsrLosIdx["GIVEI"]][FilterCondLat][FilterCondLon]       
   
    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD, [GIVDE,GIVE,GIVEI,MON],                                       # xData, yDatas
        "Hour of Day", ["GIVDE [m]","GIVE [m]","GIVEI [m]", "Monitored"],  # xLabel, yLabels
        ['r','g','b','y'], ['s','s','s','.'],                              # Colors, Markers
        'upper right', [0,2] )                                             # legendPos, yOffsets
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["LineStyle"] = 'None'
    PlotConf["LineWidth"] = 0.9
    PlotConf["FigSize"] = (12, 10)
    PlotConf["Twin"] = {                
        "yLim" : [0 , 2] ,
        "Label" : "Monitored"    # Must match with one yLabel        
        }
    plt.generatePlot(PlotConf)


# Generate a Plot GIVD and VTEC Evolution along the day for a specific Lon|Lat.
def plotUsrTimeGivdVtecMon(UsrInfoData, yearDayText, pos, posLabel, yLimits = None):
    filePath = sys.argv[1] + f'{RelativePath}USR_TIME_GIVD_VTEC_{posLabel}_{yearDayText}_G123_50s.png' 
    lon = pos["LON"]
    lat = pos["LAT"]
    title = f"USR {posLabel} [Lon|Lat]:[{lon}:{lat}] {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns
    FilterCondLon = UsrInfoData[UsrLosIdx["LON"]] == lon
    FilterCondLat = UsrInfoData[UsrLosIdx["LAT"]] == lat
    HOD = UsrInfoData[UsrLosIdx["SoD"]][FilterCondLat][FilterCondLon] / GnssConstants.S_IN_H  # Converting to hours    
    MON = UsrInfoData[UsrLosIdx["STATUS"]][FilterCondLat][FilterCondLon]
    GIVD = UsrInfoData[UsrLosIdx["GIVD"]][FilterCondLat][FilterCondLon]
    VTEC = UsrInfoData[UsrLosIdx["VTEC"]][FilterCondLat][FilterCondLon]    
   
    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD, [GIVD,VTEC,MON],                                       # xData, yDatas
        "Hour of Day", ["GIVD [m]","VTEC [m]", "Monitored"],        # xLabel, yLabels
        ['g','b','y'], ['s','s','.'],                                # Colors, Markers
        'upper right', [0,0.2] )                                       # legendPos, yOffsets
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["LineStyle"] = 'None'
    PlotConf["LineWidth"] = 0.9
    PlotConf["FigSize"] = (12, 10)
    PlotConf["Twin"] = {                
        "yLim" : [0 , 2] ,
        "Label" : "Monitored"    # Must match with one yLabel        
        }
    
    if yLimits:
        PlotConf["yLim"] = yLimits

    plt.generatePlot(PlotConf)


# Generate a Plot VTEC Evolution along the day for all the positions
def plotUsrTimeVtecAllPositions(UsrInfoData, yearDayText, positions):
    filePath = sys.argv[1] + f'{RelativePath}USR_TIME_VTEC_All_Positions_{yearDayText}_G123_50s.png' 
    title = f"USRs VTEC Evolution {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns    
    VTECs = []
    VTECsLabels = []
    for pos in positions:
        lon = positions[pos]["LON"]
        lat = positions[pos]["LAT"]
        FilterCondLon = UsrInfoData[UsrLosIdx["LON"]] == lon
        FilterCondLat = UsrInfoData[UsrLosIdx["LAT"]] == lat
        VTECs.append(UsrInfoData[UsrLosIdx["VTEC"]][FilterCondLat][FilterCondLon])
        VTECsLabels.append(f'VTEC {pos} [{lon} {lat}]')
        HOD = UsrInfoData[UsrLosIdx["SoD"]][FilterCondLat][FilterCondLon] / GnssConstants.S_IN_H   
   
    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD, VTECs,                                         # xData, yDatas
        "Hour of Day", VTECsLabels,                         # xLabel, yLabels
        ['g','b','y','r','m'], ['s','s','s','s','s'],       # Colors, Markers
        'upper right', [-0.2,0.2] )                            # legendPos, yOffsets
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]    
    PlotConf["LineWidth"] = 0.9
    PlotConf["FigSize"] = (12, 10)
    PlotConf["LineStyle"] = 'None'
    plt.generatePlot(PlotConf)


# Generate a Plot SI (Safey Index) Evolution along the day for all the positions
def plotUsrTimeSiAllPositions(UsrInfoData, yearDayText, positions):
    filePath = sys.argv[1] + f'{RelativePath}USR_TIME_SI_All_Positions_{yearDayText}_G123_50s.png' 
    title = f"USRs GIVDE/5.33*GIVE {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns    
    SI = []
    SILabels = []
    for pos in positions:
        lon = positions[pos]["LON"]
        lat = positions[pos]["LAT"]
        FilterCondLon = UsrInfoData[UsrLosIdx["LON"]] == lon
        FilterCondLat = UsrInfoData[UsrLosIdx["LAT"]] == lat
        GIVDE = UsrInfoData[UsrLosIdx["GIVDE"]][FilterCondLat][FilterCondLon]
        GIVE = UsrInfoData[UsrLosIdx["GIVE"]][FilterCondLat][FilterCondLon]
        SI.append(GIVDE / (GIVE * 5.33))
        SILabels.append(f'SI {pos} [{lon} {lat}]')
        HOD = UsrInfoData[UsrLosIdx["SoD"]][FilterCondLat][FilterCondLon] / GnssConstants.S_IN_H   
   
    PlotConf = plt.createPlotConfig2DLines(
        filePath, title, 
        HOD, SI,                                         # xData, yDatas
        "Hour of Day", SILabels,                         # xLabel, yLabels
        ['g','b','y','r','m'], ['s','s','s','s','s'],    # Colors, Markers
        'upper right', [-0.05,0.1] )                      # legendPos, yOffsets
    
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]        
    PlotConf["LineWidth"] = 0.9
    PlotConf["FigSize"] = (12, 10)
    PlotConf["LineStyle"] = 'None'
    plt.generatePlot(PlotConf)