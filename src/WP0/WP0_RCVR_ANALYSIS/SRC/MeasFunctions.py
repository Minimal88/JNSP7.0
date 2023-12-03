## Copyright (C) GNSS ACADEMY 
##
## Name          : MeasFunctions.py
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

# T5.1 Slant Tropospheric Delay (STD)
def plotSatMeasPsrElev(LosData):    
    psr = LosData[LOS_IDX["MEAS[m]"]]  # Extracting satellite MEAS information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Psudo-range C1C vs Time TLSA"

    PlotConf["yLabel"] = "Pseudo-range [Km]"
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
    PlotConf["yData"][Label] = psr / 1000  # Using satellite MEAS in Km
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'MEAS_CODES_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T5.2 def plotSatMEASStdElev(LosData) (Elev)
def plotSatMeasTauElev(LosData):
    std = LosData[LOS_IDX["TROPO[m]"]]  # Extracting satellite TROPO information
    
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
    PlotConf["yData"][Label] = std  # Using satellite TROPO in m
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'TROPO_STD_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 
