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
    print( 'Ploting image: Satellites Used in PVT ...')

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
    print( 'Ploting image: the PDOP, GDOP, TDOP in order ...')

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
    print( 'Ploting image: HDOP and VDOP together with the number of satellites ...')

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
    print( 'Ploting image: East/North/Up Position Error (EPE, NPE, UPE) ...')    

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

# T6.5 Plot the Horizontal and Vertical Position Error (HPE) and VPE
def plotPosHpeVpe(PosData):
    print( 'Ploting image: Horizontal and Vertical Position Error (HPE) and VPE ...')    

    # Extract information
    EPE = PosData[POS_IDX["EPE[m]"]]
    NPE = PosData[POS_IDX["NPE[m]"]]
    UPE = PosData[POS_IDX["UPE[m]"]]
    HoursDoY = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours

    # Calculate HPE and VPE
    HPE = np.sqrt(EPE**2 + NPE**2)
    VPE = np.abs(UPE)
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "ENU Position Error from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "H/V-PE [m]"
    PlotConf["yTicks"] = range(0,8)
    PlotConf["yLim"] = [0,8]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '-'
    PlotConf["LineWidth"] = 2
    PlotConf["ShowLegend"] = True

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    Label = "HPE [m]"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = HPE

    Label = "VPE [m]"
    PlotConf["xData"][Label] = HoursDoY
    PlotConf["yData"][Label] = VPE

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_HVPE_vs_TIME_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 


# T6.6 Plot Horizontal Scatter plot with NPE vs. EPE (North Position Error
# Y-axis and East Position Error X-axis)
def plotPosEpeNpe(PosData):
    print( 'Ploting image: Plot Horizontal Scatter plot with NPE vs. EPE ...')    

    # Extract information
    EPE = PosData[POS_IDX["EPE[m]"]]
    NPE = PosData[POS_IDX["NPE[m]"]]    
    HDOP = PosData[POS_IDX["HDOP"]]        
    HoursDoY = PosData[POS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours

    # Calculate NPE and VPE
    
    # Plot settings
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "EPE vs NPE from TLSA on Year 2015 DoY 006 "

    PlotConf["yLabel"] = "NPE [m]"
    PlotConf["yTicks"] = range(-3,5)
    PlotConf["yLim"] = [-3,5]

    PlotConf["xLabel"] = "EPE [m]"
    PlotConf["xTicks"] = range(-3, 3)
    PlotConf["xLim"] = [-3, 3]

    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5    

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "HDOP"
    PlotConf["ColorBarMin"] = np.min(HDOP)
    PlotConf["ColorBarMax"] = np.max(HDOP)


    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    Label = 0
    PlotConf["xData"][Label] = EPE
    PlotConf["yData"][Label] = NPE
    PlotConf["zData"][Label] = HDOP    

    PlotConf["Path"] = sys.argv[1] + '/OUT/POS/POS/' + 'POS_NPE_vs_EPE_TLSA_D006Y15.png'  

    # Generate plot
    generatePlot(PlotConf) 