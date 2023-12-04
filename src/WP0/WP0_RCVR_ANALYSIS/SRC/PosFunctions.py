## Copyright (C) GNSS ACADEMY 
##
## Name          : Posunctions.py
## Purpose       : Satellite Analyses functions
## Project       : WP0-JSNP
## Component     : 
## Author        : GNSS Academy
## Creation date : 2021
## File Version  : 1.0
## Version date  : 
##

import sys, os
from pandas import unique
from interfaces import LOS_IDX, POS_IDX
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
from COMMON.Plots import generatePlot
import numpy as np
# from pyproj import Transformer
from COMMON.Coordinates import xyz2llh

# T6.1 Satellites Used in PVT
def plotPosNumberOfSats(PosData):
    print( 'Ploting the Satellites Used in PVT image ...')

    # Extract number of satellites information
    num_sats = PosData[POS_IDX["NSATS"]]     
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Number of Satellites in PVT vs Time from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "Number of Satellites"
    PlotConf["yTicks"] = range(0,14)
    PlotConf["yLim"] = [0,14]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '-'
    PlotConf["LineWidth"] = 2

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    Label = 0
    PlotConf["xData"][Label] = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = num_sats

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_SATS_vs_TIME_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 

# T6.2 (X)DOPS Plot the PDOP, GDOP, TDOP in order
def plotPosDops(PosData):
    print( 'Ploting the PDOP, GDOP, TDOP in order image ...')

    # Extract information
    PDOP = PosData[POS_IDX["PDOP"]]
    GDOP = PosData[POS_IDX["GDOP"]]
    TDOP = PosData[POS_IDX["TDOP"]]
    HoursDoY = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Dilution of Precision (DOP) from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "DOP"
    PlotConf["yTicks"] = range(0,5)
    PlotConf["yLim"] = [0,5]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '-'
    PlotConf["LineWidth"] = 2
    PlotConf["ShowLegend"] = True

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    Label = "PDOP"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = PDOP

    Label = "GDOP"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = GDOP

    Label = "TDOP"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = TDOP

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_DOP_vs_TIME_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 

# T6.3 H/V-DOPs Plot the HDOP and VDOP together with the number of satellites
def plotPosHVDOPsNumSats(PosData):
    print( 'Ploting image: the HDOP and VDOP together with the number of satellites ...')

    # Extract information
    HDOP = PosData[POS_IDX["HDOP"]]
    VDOP = PosData[POS_IDX["VDOP"]]
    NSATS = PosData[POS_IDX["NSATS"]]
    
    HoursDoY = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Dilution of Precision (DOP) from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "DOP"
    PlotConf["yTicks"] = range(0,5)
    PlotConf["yLim"] = [0,5]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '-'
    PlotConf["LineWidth"] = 2
    PlotConf["ShowLegend"] = True

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    Label = "HDOP"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = HDOP

    Label = "VDOP"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = VDOP

    Label = "NSATS"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = NSATS

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_HVDOP_vs_TIME_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 

# T6.4 Plot the East/North/Up Position Error (EPE, NPE, UPE)
def plotPosEnu(PosData):
    print( 'Ploting image: Plot the East/North/Up Position Error (EPE, NPE, UPE) ...')    

    # Extract information
    EPE = PosData[POS_IDX["EPE[m]"]]
    NPE = PosData[POS_IDX["NPE[m]"]]
    UPE = PosData[POS_IDX["UPE[m]"]]
    
    HoursDoY = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "ENU Position Error from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "ENU-PE [m]"
    PlotConf["yTicks"] = range(-8,4)
    PlotConf["yLim"] = [-8,4]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '-'
    PlotConf["LineWidth"] = 2
    PlotConf["ShowLegend"] = True

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    Label = "EPE [m]"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = EPE

    Label = "NPE [m]"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = NPE

    Label = "UPE [m]"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = UPE

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_ENU_PE_vs_TIME_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 