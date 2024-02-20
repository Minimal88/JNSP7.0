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
from COMMON.Coordinates import xyz2llh
from COMMON.Files import readDataFile
import IgpFunctions as sft
from IgpStatistics import IgpStatsIdx, IgpInfoIdx

# Define relative path
RelativePath = '/OUT/IGP/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def plotIgpStatsMaps(IgpStatsFile, yearDayText):
    
    #Fecth all the columns
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