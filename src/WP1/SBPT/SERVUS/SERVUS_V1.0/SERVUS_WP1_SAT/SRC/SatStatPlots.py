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
from COMMON.Plots import generatePlot
from COMMON import GnssConstants
from SatStatistics import SatStatsIdx, SatInfoIdx, SatStatsTimeIdx
import SatFunctions as sft
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
    
    # Plot MAX FC and LTCb
    plotMaxFcAndLTCb(satStatsData, yearDayText)

    # Plot MAX LTCxyz
    plotMaxLTCxyz(satStatsData, yearDayText)

    # Plot MAX NMI
    plotNMI(satStatsData, yearDayText)
    
def plotSatStatsTime(SatStatsTimeData, yearDayText):
    """
    Plot Satellite Statistics against time.

    Parameters:
        SatStatsTimeData (DataFrame): DataFrame containing satellite information data.
        yearDayText (str): Year day text for including in plot titles.

    Returns:
        None
    """

    # Plot the instantaneous number of satellites monitored as a function of the hour of the day 
    plotMON1(SatStatsTimeData, yearDayText)

    #Plot the ENT-GPS Offset along the day
    plotEntGpsOffset(SatStatsTimeData, yearDayText)

# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

def plotMonPercentage(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MON_PERCENTAGE_{yearDayText}_G123_50s.png' 
    title = f"Satellite Monitoring Percentage {yearDayText} G123 50s [%]"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    MON = StatsData[SatStatsIdx["MON"]]
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [MON], "GPS-PRN", ["MON [%]"], ['y'],'upper left' , [-2,6]))

def plotNTRANS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NTRANS_{yearDayText}_G123_50s.png' 
    title = f"Number of Transitions MtoNM or MtoDU {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    NTRANS = StatsData[SatStatsIdx["NTRANS"]]
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [NTRANS], "GPS-PRN", ["Number of Transitions"], ['y'],'upper right' , [-2,1]))
    
def plotNRIMS(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_NRIMS_{yearDayText}_G123_50s.png' 
    title = f"Minimun and Maximun Number of RIMS in view {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    RIMSMIN = StatsData[SatStatsIdx["RIMS-MIN"]]
    RIMSMAX = StatsData[SatStatsIdx["RIMS-MAX"]]    
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [RIMSMAX,RIMSMIN], "GPS-PRN", ["MAX-RIMS","MIN-RIMS"], ['y','g'],'upper left', [0,10] ))

def plotRmsSreAcr(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_ACR_{yearDayText}_G123_50s.png' 
    title = f"RMS of SREW Along/Cross/Radial along the day {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREaRMS = StatsData[SatStatsIdx["SREaRMS"]]
    SREcRMS = StatsData[SatStatsIdx["SREcRMS"]]
    SRErRMS = StatsData[SatStatsIdx["SRErRMS"]]    
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREaRMS,SREcRMS,SRErRMS], 
        "GPS-PRN", ["RMS SRE-A[m]","RMS SRE-C[m]","RMS SRE-R[m]"], 
        ['y','g','r'],'upper left',[0,1]))

def plotRmsSreb(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_RMS_SRE_B_{yearDayText}_G123_50s.png' 
    title = f"RMS of SRE-B Clock Error Component {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREbRMS = StatsData[SatStatsIdx["SREbRMS"]]       
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, 
        PRN, [SREbRMS], 
        "GPS-PRN", ["RMS SRE-B[m]"], 
        ['y'],'upper left',[0,0.1]))

def plotSREW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SREW_{yearDayText}_G123_50s.png' 
    title = f"RMS and Maximun Value of SRE at the WUL {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SREWRMS = StatsData[SatStatsIdx["SREWRMS"]]
    SREWMAX = StatsData[SatStatsIdx["SREWMAX"]]    
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SREWMAX,SREWRMS], "GPS-PRN", ["MAX SREW[m]","RMS SREW[m]"], ['y','b'],'upper left', [0,0.4] ))

def plotSFLT(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SFLT_{yearDayText}_G123_50s.png' 
    title = f"Maximun and Minimun SigmaFLT (=SigmaUDRE) {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]
    SFLTMIN = StatsData[SatStatsIdx["SFLTMIN"]]
    SFLTMAX = StatsData[SatStatsIdx["SFLTMAX"]]    
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SFLTMAX,SFLTMIN], "GPS-PRN", ["MAX SFLT[m]","MIN SFLT[m]"], ['y','b'],'upper left', [0,0.7] ))

def plotSIW(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_SIW_{yearDayText}_G123_50s.png' 
    title = f"Maximun Satellite Safety Index SI at WUL SREW/5.33UDRE {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]    
    SIMAX = StatsData[SatStatsIdx["SIMAX"]]    
    SILIM = [1 for l in SIMAX]
    
    generatePlot(sft.createPlotConfig2DVerticalBars(
        filePath, title, PRN, [SIMAX,SILIM], "GPS-PRN", ["MAX SI[m]","LIMIT"], ['y','b'],'upper left', [0,0.7] ))

def plotMaxFcAndLTCb(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_FC_LTCb_{yearDayText}_G123_50s.png' 
    title = f"Maximun Satellite Clock Fast and Long Term Corrections {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]    
    FCMAX = StatsData[SatStatsIdx["FCMAX"]]
    LTCbMAX = StatsData[SatStatsIdx["LTCbMAX"]]
    
    generatePlot(sft.createPlotConfig2DLines(
        filePath, title, 
        PRN, [FCMAX,LTCbMAX], 
        "GPS-PRN", ["MAX FC[m]","MAX LTCb[m]"], 
        ['y','b'], ['s','s'],
        'upper left', [-0.5,0.7] ))

def plotMaxLTCxyz(StatsData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_MAX_LTCxyz_{yearDayText}_G123_50s.png' 
    title = f"Maximun Satellite LTC-XYZ {yearDayText} G123 50s"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns
    PRN = StatsData[SatStatsIdx["PRN"]]    
    LTCxMAX = StatsData[SatStatsIdx["LTCxMAX"]]
    LTCyMAX = StatsData[SatStatsIdx["LTCyMAX"]]
    LTCzMAX = StatsData[SatStatsIdx["LTCzMAX"]]
    
    generatePlot(sft.createPlotConfig2DLines(
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
    PRN = StatsData[SatStatsIdx["PRN"]]    
    NMI = StatsData[SatStatsIdx["NMI"]]    
    
    generatePlot(sft.createPlotConfig2DLines(
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
    HOD = SatStatsTimeData[SatStatsTimeIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    MON = SatStatsTimeData[SatStatsTimeIdx["MON"]]    
    NMON = SatStatsTimeData[SatStatsTimeIdx["NMON"]]   
    DU = SatStatsTimeData[SatStatsTimeIdx["DU"]]   
    
    conf = sft.createPlotConfig2DLines(
        filePath, title, 
        HOD, [MON,NMON,DU], 
        "Hour of Day", ["MON","NOT-MON","DONT USE"], 
        ['y','g','b'], [',',',',','],
        'upper right', [-0.1,5] )
    
    conf["xTicks"] = range(0, 25)
    conf["xLim"] = [0, 24]
    generatePlot(conf)

def plotEntGpsOffset(SatStatsTimeData, yearDayText):
    filePath = sys.argv[1] + f'{RelativePath}SAT_ENT_GPS_OFFSET_{yearDayText}_G123_50s.png' 
    title = f"ENT-GPS EGNOS SIS {yearDayText}"    
    print( f'Ploting: {title}\n -> {filePath}')

    # Extracting Target columns    
    HOD = SatStatsTimeData[SatStatsTimeIdx["SoD"]] / GnssConstants.S_IN_H  # Converting to hours
    ENTGPS = SatStatsTimeData[SatStatsTimeIdx["ENT-GPS"]]        
    
    conf = sft.createPlotConfig2DLines(
        filePath, title, 
        HOD, [ENTGPS], 
        "Hour of Day", ["ENT-GPES [m]"], 
        ['y'], [','],
        'upper right', [-0.2,0.2] )
    
    conf["xTicks"] = range(0, 25)
    conf["xLim"] = [0, 24]
    generatePlot(conf)