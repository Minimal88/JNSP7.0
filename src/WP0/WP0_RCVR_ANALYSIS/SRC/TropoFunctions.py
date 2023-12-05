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
def plotSatTropoStdElev(LosData):
    print( 'Ploting the Slant Tropospheric Delay (STD) image ...')
    
    std = LosData[LOS_IDX["TROPO[m]"]]  # Extracting satellite TROPO information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Slant Tropospheric Delay (STD) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "STD [m]"
    PlotConf["xLabel"] = "Hour of Day 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    
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
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/TRO/' + 'TROPO_STD_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T4.2 ZTD vs TIME (Elev)
def plotSatTropoZtdElev(LosData):
    std = LosData[LOS_IDX["TROPO[m]"]]  # Extracting satellite TROPO information
    elev = LosData[LOS_IDX["ELEV"]] # Elevation data
    
    mpp = 1.001 / ((0.002001) +  np.sin(elev * np.pi / 180)**2)**0.5 # Elevation in rad

    ztd = std / mpp
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Zenith Tropo Delay (ZTD) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "ZTD [m]"
    
    PlotConf["xLabel"] = "Hour of Day 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]    
    
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
    PlotConf["yData"][Label] = ztd  # Using satellite TROPO in m
    PlotConf["zData"][Label] = elev
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/TRO/' + 'TROPO_ZTD_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 
