## Copyright (C) GNSS ACADEMY 
##
## Name          : TropoFunctions.py
## Purpose       : Satellite Analyses functions
## Project       : WP0-JSNP
## Component     : 
## Author        : GNSS Academy - Esteban Martinez
## Creation date : 2023
## File Version  : 1.0
## Version date  : 11/30/2023
##

import sys, os
from pandas import unique
from interfaces import LOS_IDX
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
from COMMON.Plots import generatePlot
import numpy as np
# from pyproj import Transformer
from COMMON.Coordinates import xyz2llh

# T4.1 Troposphere STD[m] vs Time (Elev)
def plotSatTropoStecElev(LosData):
    TROPO = LosData[LOS_IDX["TROPO[m]"]]  # Extracting satellite TROPO information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Slant Tropospheric Delay (STD) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "STD [m]"
    PlotConf["xLabel"] = "Hour of Day 006"
    
    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = TROPO  # Using satellite TROPO in m
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'TROPO_STD_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T4.2 PRN vs TIME (STEC)
def plotSatIonoPrnStec(LosData):
    stec = LosData[LOS_IDX["STEC[m]"]]  # Extracting satellite STEC information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Satellite Visibility vs STEC from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "GPS-PRN"
    PlotConf["xLabel"] = "Hour of Day 006"
    
    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "STEC [m]"
    PlotConf["ColorBarMin"] = min(stec)
    PlotConf["ColorBarMax"] = max(stec)

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = LosData[LOS_IDX["PRN"]]  # Elevation data
    PlotConf["zData"][Label] = stec  # Using satellite STEC in m
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'IONO_STEC_vs_PRN_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T4.3 VTEC vs. Time
def plotSatIonoVtecTimeElev(LosData):
    vtec = LosData[LOS_IDX["VTEC[m]"]]  # Extracting satellite VTEC information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Ionospheric Klobuchar (VTEC) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "VTEC [m]"
    PlotConf["xLabel"] = "Hour of Day 006"
    
    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = vtec  # Using satellite VTEC in m
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'IONO_VTEC_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T4. PRN vs TIME (VTEC)
def plotSatIonoPrnVtec(LosData):
    vtec = LosData[LOS_IDX["VTEC[m]"]]  # Extracting satellite VTEC information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Satellite Visibility vs VTEC from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "GPS-PRN"
    PlotConf["xLabel"] = "Hour of Day 006"
    
    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "VTEC [m]"
    PlotConf["ColorBarMin"] = min(vtec)
    PlotConf["ColorBarMax"] = max(vtec)

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = LosData[LOS_IDX["PRN"]]  # Elevation data
    PlotConf["zData"][Label] = vtec  # Using satellite VTEC in m
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'IONO_VTEC_vs_PRN_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 
    