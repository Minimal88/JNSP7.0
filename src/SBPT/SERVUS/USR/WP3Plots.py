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
from UsrHelper import UsrPerfIdx, UsrLosIdx

# Define relative path
RelativePath = '/OUT/USR/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def plotUsrPerfMaps(UsrPerfFile, yearDayText):    
    # Fecth all the columns
    UsrPerfData = readDataFile(UsrPerfFile, UsrPerfIdx.values(), 1)

    # plotUsrMapAvailability_0_100(UsrPerfData, yearDayText)

    # plotUsrMapAvailability_70_99(UsrPerfData, yearDayText)

    plotUsrMapHPE_95(UsrPerfData, yearDayText)

    plotUsrMapVPE_95(UsrPerfData, yearDayText)

    plotUsrMapRMS_HPE(UsrPerfData, yearDayText)

    plotUsrMapRMS_VPE(UsrPerfData, yearDayText)

    plotUsrMapMAX_HSI(UsrPerfData, yearDayText)

    plotUsrMapMAX_VSI(UsrPerfData, yearDayText)

    plotUsrMapNSV_MAX(UsrPerfData, yearDayText)

    plotUsrMapNSV_MIN(UsrPerfData, yearDayText)
    
    plotUsrMapMAX_HPL(UsrPerfData, yearDayText)

    plotUsrMapMIN_HPL(UsrPerfData, yearDayText)
    
    plotUsrMapMAX_VPL(UsrPerfData, yearDayText)

    plotUsrMapMIN_VPL(UsrPerfData, yearDayText)

    plotUsrMapMAX_HDOP(UsrPerfData, yearDayText)

    plotUsrMapMAX_VDOP(UsrPerfData, yearDayText)

    plotUsrMapMAX_PDOP(UsrPerfData, yearDayText)
    
    ## OLD Plots
    # plotUsrMapMinNIPPs(UsrPerfData, yearDayText)

    # plotUsrMapMaxNIPPs(UsrPerfData, yearDayText)

    # plotUsrMapMaxVTEC(UsrPerfData, yearDayText)

    # plotUsrMapMaxGIVD(UsrPerfData, yearDayText)

    # plotUsrMapMaxRMSGIVDE(UsrPerfData, yearDayText)

    # plotUsrMapMaxGIVE(UsrPerfData, yearDayText)

    # plotUsrMapMaxGIVEi(UsrPerfData, yearDayText)

    # plotUsrMapMaxSI(UsrPerfData, yearDayText)

    # plotUsrMapNTRANS(UsrPerfData, yearDayText)

    # plotUsrMapNMI(UsrPerfData, yearDayText)
    return

def plotUsrInfoTime(UsrInfoFile, yearDayText):

    positions = {
    "CNTR": {"ULAT": 45, "ULON": 5},
    "SW-1": {"ULAT": 20, "ULON": -20},
    "SW-2": {"ULAT": 20, "ULON": 35},
    "NW-1": {"ULAT": 65, "ULON": -20},
    "NW-2": {"ULAT": 60, "ULON": 35}
}
    
    # Fecth target columns
    UsrInfoData = readDataFile(UsrInfoFile, [
        UsrLosIdx["SoD"], 
        UsrLosIdx["STATUS"],
        UsrLosIdx["ULAT"],
        UsrLosIdx["ULON"],
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
def plotUsrMapAvailability_0_100(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_AVAILABILITY_0_100_{yearDayText}_G123_50s.png' 
    title = f"APV-I Availability 0-100% {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    APV1 = UsrPerfData[UsrPerfIdx["AVAILABILITY"]]
    APV1_INT = [int(x) for x in APV1]
    
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , APV1,                              # xData, yData, zData
        "Longitude [deg]", yLabel,"Availability [%]", # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,              # LonMin, LonMax, LonStep
        10, 90, 10,                # LatMin, LatMax, LatStep
        yLabel, APV1_INT)           # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapAvailability_70_99(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_AVAILABILITY_70_99_{yearDayText}_G123_50s.png' 
    title = f"APV-I Availability 0-100% {yearDayText} G123 50s (Availability: 70-99%)"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    APV1 = UsrPerfData[UsrPerfIdx["AVAILABILITY"]]    

    # Filter data for availability between 70-99%
    APV1_filtered = [x for x in APV1 if 70 <= x <= 99]
    APV1_INT_filtered = [int(x) for x in APV1_filtered]
    
    # Filter LAT and LON arrays
    LAT = [lat for i, lat in enumerate(UsrPerfData[UsrPerfIdx["ULAT"]]) if 70 <= APV1[i] <= 99]
    LON = [lon for i, lon in enumerate(UsrPerfData[UsrPerfIdx["ULON"]]) if 70 <= APV1[i] <= 99]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , APV1_filtered,                              # xData, yData, zData
        "Longitude [deg]", yLabel,"Availability [%]", # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                         # LonMin, LonMax, LonStep
        10, 90, 10,                          # LatMin, LatMax, LatStep
        yLabel, APV1_INT_filtered)           # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapHPE_95(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_HPE_95_{yearDayText}_G123_50s.png' 
    title = f"HPE 95% {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HPE95 = UsrPerfData[UsrPerfIdx["HPE-95"]]
    # Convert to float and round to 2 decimal places
    HPE95_FLOAT = [round(float(x), 3) for x in HPE95]
    
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , HPE95,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"HPE95% [m]",       # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, HPE95_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapVPE_95(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_VPE_95_{yearDayText}_G123_50s.png' 
    title = f"VPE 95% {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    VPE95 = UsrPerfData[UsrPerfIdx["VPE-95"]]
    # Convert to float and round to 2 decimal places
    VPE95_FLOAT = [round(float(x), 3) for x in VPE95]
    
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , VPE95,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"VPE95% [m]",       # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, VPE95_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapRMS_HPE(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_RMS_HPE_{yearDayText}_G123_50s.png' 
    title = f"RMS HPE {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HPE95 = UsrPerfData[UsrPerfIdx["HPE-RMS"]]
    # Convert to float and round to 2 decimal places
    HPE95_FLOAT = [round(float(x), 3) for x in HPE95]
    
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , HPE95,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"RMS HPE [m]",       # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, HPE95_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapRMS_VPE(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_RMS_VPE_{yearDayText}_G123_50s.png' 
    title = f"RMS VPE {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    VPE95 = UsrPerfData[UsrPerfIdx["VPE-RMS"]]
    # Convert to float and round to 2 decimal places
    VPE95_FLOAT = [round(float(x), 3) for x in VPE95]
    
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , VPE95,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"RMS VPE [m]",       # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, VPE95_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)
    
def plotUsrMapMAX_HSI(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_HSI_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX HSI {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_HSI = UsrPerfData[UsrPerfIdx["HSI-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXHSI_FLOAT = [round(float(x), 2) for x in MAX_HSI]    

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_HSI,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX HSI",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXHSI_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMAX_VSI(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_VSI_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX VSI {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_VSI = UsrPerfData[UsrPerfIdx["VSI-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXVSI_FLOAT = [round(float(x), 2) for x in MAX_VSI]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_VSI,                            # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX VSI",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXVSI_FLOAT)               # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapNSV_MAX(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_NSV_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX Number of Satellites on {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    NSV_MAX = UsrPerfData[UsrPerfIdx["NVS-MAX"]]
    NSV_MAX_INT = [int(x) for x in NSV_MAX]    

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , NSV_MAX,                                 # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX Num of Satellites",   # xLabel, yLabel, zLabel
        's', False)                                          # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, NSV_MAX_INT)                # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapNSV_MIN(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_NSV_MIN_{yearDayText}_G123_50s.png'
    title = f"MIN Number of Satellites on {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    NSV_MIN = UsrPerfData[UsrPerfIdx["NVS-MIN"]]
    # Convert to float and round to 2 decimal places
    NSV_MIN_INT = [int(x) for x in NSV_MIN]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , NSV_MIN,                                 # xData, yData, zData
        "Longitude [deg]", yLabel,"MIN Num of Satellites",   # xLabel, yLabel, zLabel
        's', False)                                          # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, NSV_MIN_INT)              # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMAX_HPL(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_HPL_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX HPL {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_HPL = UsrPerfData[UsrPerfIdx["HPL-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXHPL_FLOAT = [round(float(x), 2) for x in MAX_HPL]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_HPL,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX HPL",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXHPL_FLOAT)               # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMIN_HPL(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_HPL_MIN_{yearDayText}_G123_50s.png'
    title = f"MIN HPL {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MIN_HPL = UsrPerfData[UsrPerfIdx["HPL-MIN"]]
    # Convert to float and round to 2 decimal places
    MINHPL_FLOAT = [round(float(x), 2) for x in MIN_HPL]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MIN_HPL,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MIN HPL",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMin, LonStep
        10, 90, 10,                         # LatMin, LatMin, LatStep
        yLabel, MINHPL_FLOAT)               # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMAX_VPL(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_VPL_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX VPL {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_VPL = UsrPerfData[UsrPerfIdx["VPL-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXVPL_FLOAT = [round(float(x), 2) for x in MAX_VPL]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_VPL,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX VPL",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXVPL_FLOAT)               # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMIN_VPL(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_VPL_MIN_{yearDayText}_G123_50s.png'
    title = f"MIN VPL {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MIN_VPL = UsrPerfData[UsrPerfIdx["VPL-MIN"]]
    # Convert to float and round to 2 decimal places
    MINVPL_FLOAT = [round(float(x), 2) for x in MIN_VPL]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MIN_VPL,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MIN VPL",          # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMin, LonStep
        10, 90, 10,                         # LatMin, LatMin, LatStep
        yLabel, MINVPL_FLOAT)               # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapMAX_HDOP(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_HDOP_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX HDOP {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_HDOP = UsrPerfData[UsrPerfIdx["HDOP-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXHDOP_FLOAT = [round(float(x), 2) for x in MAX_HDOP]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_HDOP,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX HDOP",          # xLabel, yLabel, zLabel
        's', False)                                    # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXHDOP_FLOAT)              # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)


def plotUsrMapMAX_VDOP(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_VDOP_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX VDOP {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_VDOP = UsrPerfData[UsrPerfIdx["VDOP-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXVDOP_FLOAT = [round(float(x), 2) for x in MAX_VDOP]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_VDOP,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX VDOP",          # xLabel, yLabel, zLabel
        's', False)                                    # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXVDOP_FLOAT)              # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)


def plotUsrMapMAX_PDOP(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_PDOP_MAX_{yearDayText}_G123_50s.png'
    title = f"MAX PDOP {yearDayText} G123 50s"
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    MAX_PDOP = UsrPerfData[UsrPerfIdx["PDOP-MAX"]]
    # Convert to float and round to 2 decimal places
    MAXPDOP_FLOAT = [round(float(x), 2) for x in MAX_PDOP]

    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title,
        LON, LAT  , MAX_PDOP,                          # xData, yData, zData
        "Longitude [deg]", yLabel,"MAX PDOP",          # xLabel, yLabel, zLabel
        's', False)                                    # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                        # LonMin, LonMax, LonStep
        10, 90, 10,                         # LatMin, LatMax, LatStep
        yLabel, MAXPDOP_FLOAT)              # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)




# Generate a plot with Map for the USR Minimum NIPPs
def plotUsrMapMinNIPPs(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MIN_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Minimum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MINIPPs = UsrPerfData[UsrPerfIdx["MINIPPs"]]
    MINIPPsINT = [int(x) for x in MINIPPs]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]

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
def plotUsrMapMaxNIPPs(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_NIPPs_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum Number of IPPs {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXIPPs = UsrPerfData[UsrPerfIdx["MAXIPPs"]]
    MAXIPPsINT = [int(x) for x in MAXIPPs]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxVTEC(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_VTEC_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum VTEC [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXVTEC = UsrPerfData[UsrPerfIdx["MAXVTEC"]]
    MAXVTECFLOAT = [round(float(x), 1) for x in MAXVTEC]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxGIVD(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVD_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVD [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVD = UsrPerfData[UsrPerfIdx["MAXGIVD"]]
    MAXGIVDFLOAT = [round(float(x), 1) for x in MAXGIVD]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxRMSGIVDE(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_RMS_GIVDE_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: RMS GIVD Error [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    RMSGIVDE = UsrPerfData[UsrPerfIdx["RMSGIVDE"]]
    RMSGIVDEFLOAT = [round(float(x), 1) for x in RMSGIVDE]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxGIVE(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVE_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVE [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVE = UsrPerfData[UsrPerfIdx["MAXGIVE"]]
    MAXGIVEFLOAT = [round(float(x), 1) for x in MAXGIVE]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxGIVEi(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_GIVEi_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum GIVEi [m] {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXGIVEi = UsrPerfData[UsrPerfIdx["MAXGIVEI"]]
    MAXGIVEiFLOAT = [round(float(x), 1) for x in MAXGIVEi]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapMaxSI(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_MAX_SI_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Maximum SI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    MAXSI = UsrPerfData[UsrPerfIdx["MAXSI"]]
    MAXSIFLOAT = [round(float(x), 1) for x in MAXSI]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapNTRANS(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_NTRANS_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Number of Transitions MtoNM MtoDU {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NTRANS = UsrPerfData[UsrPerfIdx["NTRANS"]]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
def plotUsrMapNMI(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_NMI_MAP_{yearDayText}_G123_50s.png' 
    title = f"USR Map: Number of MI {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    NMI = UsrPerfData[UsrPerfIdx["NMI"]]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]    
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]    

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
    lon = pos["ULON"]
    lat = pos["ULAT"]
    title = f"USR {posLabel} [Lon|Lat]:[{lon}:{lat}] {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns
    FilterCondLon = UsrInfoData[UsrLosIdx["ULON"]] == lon
    FilterCondLat = UsrInfoData[UsrLosIdx["ULAT"]] == lat
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
    lon = pos["ULON"]
    lat = pos["ULAT"]
    title = f"USR {posLabel} [Lon|Lat]:[{lon}:{lat}] {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting and Filtering  Target columns
    FilterCondLon = UsrInfoData[UsrLosIdx["ULON"]] == lon
    FilterCondLat = UsrInfoData[UsrLosIdx["ULAT"]] == lat
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
        lon = positions[pos]["ULON"]
        lat = positions[pos]["ULAT"]
        FilterCondLon = UsrInfoData[UsrLosIdx["ULON"]] == lon
        FilterCondLat = UsrInfoData[UsrLosIdx["ULAT"]] == lat
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
        lon = positions[pos]["ULON"]
        lat = positions[pos]["ULAT"]
        FilterCondLon = UsrInfoData[UsrLosIdx["ULON"]] == lon
        FilterCondLat = UsrInfoData[UsrLosIdx["ULAT"]] == lat
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