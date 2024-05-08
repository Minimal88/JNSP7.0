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

    plotUsrMapAvailability_0_100(UsrPerfData, yearDayText)

    plotUsrMapAvailability_70_99(UsrPerfData, yearDayText)

    plotUsrMapAvailability_0_99_NoInterpolation(UsrPerfData, yearDayText)

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
    
    # Get LAT and LON arrays
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig3DMapColorBarInterpolated(
        filePath, title, 
        LON, LAT  , APV1,                               # xData, yData, zData
        "Longitude [deg]", yLabel,"Availability [%]",   # xLabel, yLabel, zLabel
        -35, 50, 5,                                     # LonMin, LonMax, LonStep
        15, 80, 5,                                      # LatMin, LatMax, LatStep, 
        0, 100, "Availability_0_100")                   # ColorBarMin, ColorBarMax, ColorBar

    plt.generateInterpolatedMapPlot(PlotConf)

def plotUsrMapAvailability_70_99(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_AVAILABILITY_70_99_{yearDayText}_G123_50s.png' 
    title = f"APV-I Availability 70-99% {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    APV1 = UsrPerfData[UsrPerfIdx["AVAILABILITY"]]    

    # Get LAT and LON arrays
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig3DMapColorBarInterpolated(
        filePath, title, 
        LON, LAT  , APV1,                               # xData, yData, zData
        "Longitude [deg]", yLabel,"Availability [%]",   # xLabel, yLabel, zLabel
        -35, 50, 5,                                     # LonMin, LonMax, LonStep
        15, 80, 5,                                      # LatMin, LatMax, LatStep, 
        70, 99, "Availability_70_99")                   # ColorBarMin, ColorBarMax, ColorBar
    
    plt.generateInterpolatedMapPlot(PlotConf)

def plotUsrMapAvailability_0_99_NoInterpolation(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_AVAILABILITY_0_100_NoInterpolation_{yearDayText}_G123_50s.png' 
    title = f"APV-I Availability 0-100% No Interpolation {yearDayText} G123 50s "    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    APV1 = UsrPerfData[UsrPerfIdx["AVAILABILITY"]]
    APV1_FLOAT = [round(float(x), 2) for x in APV1]

    # Get LAT and LON arrays
    LAT = UsrPerfData[UsrPerfIdx["ULAT"]]
    LON = UsrPerfData[UsrPerfIdx["ULON"]]

    yLabel = "Latitude [deg]"
    PlotConf = plt.createPlotConfig2DLinesColorBar(
        filePath, title, 
        LON, LAT  , APV1_FLOAT,                       # xData, yData, zData
        "Longitude [deg]", yLabel,"Availability [%]", # xLabel, yLabel, zLabel
        's', False)                                   # Markers, applyLimits

    plt.addMapToPlotConf(PlotConf,
        -40, 70, 10,                         # LonMin, LonMax, LonStep
        10, 90, 10,                          # LatMin, LatMax, LatStep
        yLabel, APV1_FLOAT)                  # yLabel, TextData (Optional)

    plt.generatePlot(PlotConf)

def plotUsrMapHPE_95(UsrPerfData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}USR_PERF_MAP_APV-I_HPE_95_{yearDayText}_G123_50s.png' 
    title = f"HPE 95% {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HPE95 = UsrPerfData[UsrPerfIdx["HPE-95"]]
    # Convert to float and round to 2 decimal places
    HPE95_FLOAT = [round(float(x), 2) for x in HPE95]
    
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
    VPE95_FLOAT = [round(float(x), 2) for x in VPE95]
    
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
    HPE95_FLOAT = [round(float(x), 2) for x in HPE95]
    
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
    VPE95_FLOAT = [round(float(x), 2) for x in VPE95]
    
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