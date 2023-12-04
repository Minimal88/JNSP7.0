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

# T5.1 Plot Pseudo-ranges (Code Measurements C1) for all satellites as a
# function of the hour of the day. Color bar: satellite elevation.
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

# T5.2  Plot Tau = C1C/c for all satellites as a function of the hour of the
# day. Color bar: satellite elevation.
def plotSatMeasTauElev(LosData):    
    psr = LosData[LOS_IDX["MEAS[m]"]]  # Extracting satellite MEAS information
    tau = psr / GnssConstants.c
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Tau = Rho/c from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "Tau [ms]"
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
    PlotConf["yData"][Label] = tau * 1000  # Using satellite TAU in ms
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'TAU_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)


# T5.3  Plot Time of Flight (ToF) for all satellites as a function of the hour
# of the day. Color bar: satellite elevation.
def plotSatMeasTofElev(LosData):    
    tof = LosData[LOS_IDX["TOF[ms]"]]  # Extracting satellite TOF information
        
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Time of Flight (ToF) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "Tau [ms]"
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
    PlotConf["yData"][Label] = tof  # Using satellite TOF in ms
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'TOF_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)