#!/usr/bin/env python

########################################################################
# SatStatPlots.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatStatPlots.py
#  Date(YY/MM/DD): 24/02/08
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON.Plots import generatePlot, generateVerticalBarPlot
from SatStatistics import SatStatsIdx
from COMMON import GnssConstants
from pandas import read_csv
from math import sqrt
import numpy as np

# Define relative path
RelativePath = '/OUT/SAT/FIGURES/'
# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

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

    # Plot Number of Transitions
    plotNTRANS(satStatsData, yearDayText)

    # Plot Number of RIMS
    plotNRIMS(satStatsData, yearDayText)

    # Plot RMS SRE ACR
    plotRmsSreAcr(satStatsData, yearDayText)

    # Plot RMS SREB
    plotRmsSreb(satStatsData, yearDayText)

    # Plot SREW
    plotSREW(satStatsData, yearDayText)

    # Plot SFLT
    plotSFLT(satStatsData, yearDayText)

    # Plot SIW
    plotSIW(satStatsData, yearDayText)


def readStatsFile(statisticsFilePath, columnNameList):
    """
    Read specific columns from a statistics file and return a DataFrame.

    Parameters:
    - statisticsFilePath: Path to the statistics file.
    - columnNameList: List of column names to be read.

    Returns:
    - StatsData containing the specified columns.
    """
    # Read the specified columns from the file
    #StatsData = read_csv(statisticsFilePath, delim_whitespace=True, skiprows=1, header=None, usecols=fixedColumnList)
    StatsData = read_csv(statisticsFilePath, delim_whitespace=True, skiprows=1, header=None)

    # Set column names based on the provided columnList    
    #StatsData.columns = columnNameList

    return StatsData

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------
def createPlotConfig2DVerticalBars(filepath, title, xData, yDataList, xLabel, yLabels, colors, legPos, yOffset = [0,0]):
    """
    Creates a new Plot Configuration for plotting vertical 2D bars.
    Y-axis: Multiple sets of data received from lists of lists
    X-asis: A single set of data from a list

    Parameters:
        filepath (str): Path to save the plot figure.
        title (str): Title of the plot figure.
        xData (list): List of x-axis data.
        yDataList (list): List of lists containing y-axis data sets.
        xLabel (str): Label of x-axis data.
        yLabels (list): List of labels for each y-axis data set.
        colors (list): List of colors for each y-axis data set.
        legPos (str): Position of the legend (example: 'upper left').
        yOffset (list): List of y-axis offsets: [lowerOffset, upperOffset]
    
    Returns:
        PlotConf(list): Configuration Data Structure for plotting Vertical 2D Bars with generateVerticalBarPlot()
    """
    PlotConf = {}
    PlotConf["Type"] = "VerticalBar"
    PlotConf["FigSize"] = (12, 6)
    PlotConf["Title"] = title
    PlotConf["xLabel"] = xLabel
    PlotConf["xTicks"] = range(0, len(xData))
    PlotConf["xLim"] = [-1, len(xData)]
    minY = min([min(y) for y in yDataList])
    maxY = max([max(y) for y in yDataList])
    PlotConf["yLim"] = [minY + yOffset[0], maxY + yOffset[1]]
    PlotConf["Grid"] = True    
    PlotConf["LineWidth"] = 1
    if legPos: PlotConf["ShowLegend"] = legPos
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}    
    PlotConf["Color"] = {}    
    PlotConf["Path"] = filepath
    for yLabel, yData, color in zip(yLabels, yDataList, colors):        
        PlotConf["yData"][yLabel] = yData
        PlotConf["xData"][yLabel] = xData
        PlotConf["Color"][yLabel] = color        
    
    return PlotConf    

def plotMonPercentage(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON_PERCENTAGE_{yearDayText}_G123_50s.png' 
    title = f"Satellite Monitoring Percentage {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    MON = StatsData[SatStatsIdx["MON"]]
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [MON], "GPS-PRN", ["MON [%]"], ['y'],'upper left' , [-2,6]))

def plotNTRANS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NTRANS_{yearDayText}_G123_50s.png' 
    title = f"Number of Transitions MtoNM or MtoDU {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    NTRANS = StatsData[SatStatsIdx["NTRANS"]]
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [NTRANS], "GPS-PRN", ["Number of Transitions"], ['y'],'upper right' , [-2,1]))
    
def plotNRIMS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NRIMS_{yearDayText}_G123_50s.png' 
    title = f"Minimun and Maximun Number of RIMS in view {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    RIMSMIN = StatsData[SatStatsIdx["RIMS-MIN"]]
    RIMSMAX = StatsData[SatStatsIdx["RIMS-MAX"]]    
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [RIMSMAX,RIMSMIN], "GPS-PRN", ["MAX-RIMS","MIN-RIMS"], ['y','g'],'upper left', [0,10] ))

def plotRmsSreAcr(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_ACR_{yearDayText}_G123_50s.png' 
    title = f"RMS of SREW Along/Cross/Radial along the day {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREaRMS = StatsData[SatStatsIdx["SREaRMS"]]
    SREcRMS = StatsData[SatStatsIdx["SREcRMS"]]
    SRErRMS = StatsData[SatStatsIdx["SRErRMS"]]    
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREaRMS,SREcRMS,SRErRMS], 
        "GPS-PRN", ["RMS SRE-A[m]","RMS SRE-C[m]","RMS SRE-R[m]"], 
        ['y','g','r'],'upper left',[0,1]))

def plotRmsSreb(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_B_{yearDayText}_G123_50s.png' 
    title = f"RMS of SRE-B Clock Error Component {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREbRMS = StatsData[SatStatsIdx["SREbRMS"]]       
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREbRMS], 
        "GPS-PRN", ["RMS SRE-B[m]"], 
        ['y'],'upper left',[0,0.1]))

def plotSREW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SREW_{yearDayText}_G123_50s.png' 
    title = f"RMS and Maximun Value of SRE at the WUL {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREWRMS = StatsData[SatStatsIdx["SREWRMS"]]
    SREWMAX = StatsData[SatStatsIdx["SREWMAX"]]    
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SREWMAX,SREWRMS], "GPS-PRN", ["MAX SREW[m]","RMS SREW[m]"], ['y','b'],'upper left', [0,0.4] ))

def plotSFLT(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SFLT_{yearDayText}_G123_50s.png' 
    title = f"Maximun and Minimun SigmaFLT (=SigmaUDRE) {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SFLTMIN = StatsData[SatStatsIdx["SFLTMIN"]]
    SFLTMAX = StatsData[SatStatsIdx["SFLTMAX"]]    
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SFLTMAX,SFLTMIN], "GPS-PRN", ["MAX SFLT[m]","MIN SFLT[m]"], ['y','b'],'upper left', [0,0.7] ))

def plotSIW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SIW_{yearDayText}_G123_50s.png' 
    title = f"Maximun Satellite Safety Index SI at WUL SREW/5.33UDRE {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]    
    SIMAX = StatsData[SatStatsIdx["SIMAX"]]    
    SILIM = [1 for l in SIMAX]
    
    generateVerticalBarPlot(createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SIMAX,SILIM], "GPS-PRN", ["MAX SI[m]","LIMIT"], ['y','b'],'upper left', [0,0.7] ))

