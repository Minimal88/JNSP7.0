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
import pandas as pd
import COMMON.Plots as plt
from COMMON import GnssConstants
from COMMON.Files import readDataFile
import IgpFunctions as sft
from IgpStatistics import IgpStatsIdx, IgpInfoIdx

# Define relative path
RelativePath = '/OUT/IGP/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def plotIgpStatsMaps(IgpStatsFile, yearDayText):    
    # Fecth all the columns
    IgpStatsData = readDataFile(IgpStatsFile, IgpStatsIdx.values(), 1)

    plotIgpMapMon(IgpStatsData, yearDayText)

    plotIgpMapMinNIPPs(IgpStatsData, yearDayText)

    plotIgpMapMaxNIPPs(IgpStatsData, yearDayText)

    plotIgpMapMaxVTEC(IgpStatsData, yearDayText)

    plotIgpMapMaxGIVD(IgpStatsData, yearDayText)

    plotIgpMapMaxRMSGIVDE(IgpStatsData, yearDayText)

    plotIgpMapMaxGIVE(IgpStatsData, yearDayText)

    plotIgpMapMaxGIVEi(IgpStatsData, yearDayText)

    plotIgpMapMaxSI(IgpStatsData, yearDayText)

    plotIgpMapNTRANS(IgpStatsData, yearDayText)

    plotIgpMapNMI(IgpStatsData, yearDayText)
    return

def plotIgpInfoTime(IgpInfoFile, yearDayText):

    positions = {
    "CNTR": {"LAT": 45, "LON": 5},
    "SW-1": {"LAT": 20, "LON": -20},
    "SW-2": {"LAT": 20, "LON": 35},
    "NW-1": {"LAT": 65, "LON": -20},
    "NW-2": {"LAT": 60, "LON": 35}
}
    
    # Fecth target columns
    IgpInfoData = readDataFile(IgpInfoFile, [
        IgpInfoIdx["SoD"], 
        IgpInfoIdx["STATUS"],
        IgpInfoIdx["LAT"],
        IgpInfoIdx["LON"],
        IgpInfoIdx["GIVEI"],
        IgpInfoIdx["GIVDE"],
        IgpInfoIdx["GIVE"],
        IgpInfoIdx["GIVEI"],
        IgpInfoIdx["VTEC"]
        ], 1)

    plotIgpTimeMon(IgpInfoData, yearDayText)

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for IGP CENTER
    plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, positions["CNTR"], "CENTER")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for IGP SOUTH 1
    plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, positions["SW-1"], "SW-1")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for IGP SOUTH 2
    plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, positions["SW-2"], "SW-2")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for IGP NORTH 1
    plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, positions["NW-1"], "NW-1")

    # Plot the GIVDE, GIVE, GIVEi and Monitoring for IGP SOUTH 2
    plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, positions["NW-2"], "NW-2")
    

    return

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

# Generate a plot with Map for the IGP Monitired Percentage
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
    
# Generate a plot with Map for the IGP Minimum NIPPs
def plotIgpMapMinNIPPs(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MIN_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Minimum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MINIPPs = IgpStatsData[IgpStatsIdx["MINIPPs"]]
    MINIPPsINT = [int(x) for x in MINIPPs]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum NIPPs
def plotIgpMapMaxNIPPs(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXIPPs = IgpStatsData[IgpStatsIdx["MAXIPPs"]]
    MAXIPPsINT = [int(x) for x in MAXIPPs]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum VTEC
# TODO: Check the values of this plot, something is off
def plotIgpMapMaxVTEC(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_VTEC_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum VTEC [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXVTEC = IgpStatsData[IgpStatsIdx["MAXVTEC"]]
    MAXVTECFLOAT = [round(float(x), 1) for x in MAXVTEC]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum GIVD
def plotIgpMapMaxGIVD(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_GIVD_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum GIVD [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVD = IgpStatsData[IgpStatsIdx["MAXGIVD"]]
    MAXGIVDFLOAT = [round(float(x), 1) for x in MAXGIVD]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP RMS GIVD Error
def plotIgpMapMaxRMSGIVDE(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_RMS_GIVDE_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: RMS GIVD Error [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    RMSGIVDE = IgpStatsData[IgpStatsIdx["RMSGIVDE"]]
    RMSGIVDEFLOAT = [round(float(x), 1) for x in RMSGIVDE]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum GIVE
def plotIgpMapMaxGIVE(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_GIVE_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum GIVE [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVE = IgpStatsData[IgpStatsIdx["MAXGIVE"]]
    MAXGIVEFLOAT = [round(float(x), 1) for x in MAXGIVE]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum GIVEi
def plotIgpMapMaxGIVEi(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_GIVEi_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum GIVEi [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVEi = IgpStatsData[IgpStatsIdx["MAXGIVEI"]]
    MAXGIVEiFLOAT = [round(float(x), 1) for x in MAXGIVEi]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP Maximum SI
def plotIgpMapMaxSI(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_MAX_SI_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Maximum SI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXSI = IgpStatsData[IgpStatsIdx["MAXSI"]]
    MAXSIFLOAT = [round(float(x), 1) for x in MAXSI]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP NTRANS Number of Transitions
def plotIgpMapNTRANS(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_NTRANS_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Number of Transitions MtoNM MtoDU {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NTRANS = IgpStatsData[IgpStatsIdx["NTRANS"]]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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

# Generate a plot with Map for the IGP NMI Number of MI
def plotIgpMapNMI(IgpStatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_NMI_MAP_{yearDayText}_G123_50s.png' 
    title = f"IGP Map: Number of MI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NMI = IgpStatsData[IgpStatsIdx["NMI"]]
    LON = IgpStatsData[IgpStatsIdx["LON"]]    
    LAT = IgpStatsData[IgpStatsIdx["LAT"]]    

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


# Generate a plot with the Number of Monitored/ Not Monitored / DU IGPs 
def plotIgpTimeMon(IgpInfoData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}IGP_TIME_MON_{yearDayText}_G123_50s.png' 
    title = f"Number of IGP Monitored EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns        
    HOD = IgpInfoData[IgpInfoIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours    
    MON = IgpInfoData[IgpInfoIdx["STATUS"]]
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
def plotIgpTimeGivdeGiveGiveiMon(IgpInfoData, yearDayText, pos, posLabel):
    filePath = sys.argv[1] + f'{RelativePath}IGP_TIME_GIVDE_GIVE_GIVEI_{posLabel}_{yearDayText}_G123_50s.png' 
    lon = pos["LON"]
    lat = pos["LAT"]
    title = f"IGP {posLabel} [Lon|Lat]:[{lon}:{lat}] {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns
    FilterCondLon = IgpInfoData[IgpInfoIdx["LON"]] == lon
    FilterCondLat = IgpInfoData[IgpInfoIdx["LAT"]] == lat
    HOD = IgpInfoData[IgpInfoIdx["SoD"]][FilterCondLat][FilterCondLon] / GnssConstants.S_IN_H  # Converting to hours    
    MON = IgpInfoData[IgpInfoIdx["STATUS"]][FilterCondLat][FilterCondLon]
    GIVDE = IgpInfoData[IgpInfoIdx["GIVDE"]][FilterCondLat][FilterCondLon]
    GIVE = IgpInfoData[IgpInfoIdx["GIVE"]][FilterCondLat][FilterCondLon]
    GIVEI = IgpInfoData[IgpInfoIdx["GIVEI"]][FilterCondLat][FilterCondLon]       
   
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