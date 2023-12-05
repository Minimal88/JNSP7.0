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
    print( 'Ploting the Psudo-range C1C image ...')

    psr = LosData[LOS_IDX["MEAS[m]"]]  # Extracting satellite MEAS information
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Psudo-range C1C vs Time TLSA"

    PlotConf["yLabel"] = "Pseudo-range [Km]"
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
    PlotConf["yData"][Label] = psr / 1000  # Using satellite MEAS in Km
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'MEAS_CODES_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf) 

# T5.2  Plot Tau = C1C/c for all satellites as a function of the hour of the
# day. Color bar: satellite elevation.
def plotSatMeasTauElev(LosData):    
    print( 'Ploting Tau = C1C/c image ...')
    psr = LosData[LOS_IDX["MEAS[m]"]]  # Extracting satellite MEAS information
    tau = psr / GnssConstants.c_m_s
    
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Tau = Rho/c from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "Tau [ms]"
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
    PlotConf["yData"][Label] = tau * 1000  # Using satellite TAU in ms
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'TAU_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)


# T5.3  Plot Time of Flight (ToF) for all satellites as a function of the hour
# of the day. Color bar: satellite elevation.
def plotSatMeasTofElev(LosData):    
    print( 'Ploting Time of Flight (ToF) image ...')

    tof = LosData[LOS_IDX["TOF[ms]"]]  # Extracting satellite TOF information
        
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Time of Flight (ToF) from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "ToF [ms]"
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
    PlotConf["yData"][Label] = tof  # Using satellite TOF in ms
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'TOF_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)

# T5.4  Plot Doppler Frequency, fD, in kHz for all satellites as a function of the hour
# of the day. Color bar: satellite elevation.
def plotSatMeasDopplerElev(LosData, X_RCVR, Y_RCVR, Z_RCVR):
    print( 'Ploting Doppler Frequency (kHz) image ...')

    # Calculate satellite velocity projected in the direction of the Line Of Sight (LOS)
    rSAT_X = LosData[LOS_IDX["SAT-X[m]"]]  # Satellite X-Position
    rSAT_Y = LosData[LOS_IDX["SAT-Y[m]"]]  # Satellite Y-Position
    rSAT_Z = LosData[LOS_IDX["SAT-Z[m]"]]  # Satellite Z-Position

    # rLOS = rSAT − rRCVR
    rLOS_X = rSAT_X - X_RCVR
    rLOS_Y = rSAT_Y - Y_RCVR
    rLOS_Z = rSAT_Z - Z_RCVR

    # |rLOS|
    rLOS = np.column_stack((rLOS_X, rLOS_Y, rLOS_Z))
    norm_rLOS = np.linalg.norm(rLOS, axis=1)

    # uLOS = rLOS / |rLOS|
    uLOS = rLOS / norm_rLOS[:, np.newaxis]

    # vLOS = uLOS ∙ vLOS
    vLOS_X = LosData[LOS_IDX["VEL-X[m/s]"]]  # Satellite X-Velocity
    vLOS_Y = LosData[LOS_IDX["VEL-Y[m/s]"]]  # Satellite Y-Velocity
    vLOS_Z = LosData[LOS_IDX["VEL-Z[m/s]"]]  # Satellite Z-Velocity

    vLOS = np.sum(uLOS * np.column_stack((vLOS_X, vLOS_Y, vLOS_Z)), axis=1)

    # Calculate Doppler Frequency (fD) for all satellites
    fD_KHz = - (vLOS / GnssConstants.c_m_s) * GnssConstants.fL1_Hz / 1000  # Convert to kHz
        
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Doppler Frequency from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "Doppler Frequency [KHz]"
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
    PlotConf["yData"][Label] = fD_KHz  # Using Doppler Effect in KHz
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]  # Elevation data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'DOPPLER_FREQ_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)


# T5.5 Plot the PVT filter residuals, correcting the code
# measurements from all the known information from Navigation
# message and models
def plotSatMeasResidualsElev(LosData):    
    print( 'Ploting the PVT filter Residuals image ...')

    # Extract necessary data
    prn = LosData[LOS_IDX["PRN"]]  # Satellite PRN information
    PSRC1 = LosData[LOS_IDX["MEAS[m]"]]  # Code Measurements C1
    RGE = LosData[LOS_IDX["RANGE[m]"]]  # Satellite Geometrical Range
    CLKP1P2 = LosData[LOS_IDX["SV-CLK[m]"]]  # Satellite Clock (CLKP1P2)
    IONO = LosData[LOS_IDX["VTEC[m]"]]  # Vertical Total-Electron-Content
    TROPO = LosData[LOS_IDX["TROPO[m]"]]  # Slant Tropospheric Delay
    DTR = LosData[LOS_IDX["DTR[m]"]]  # Satellite Relativistic Effect
    TGD = LosData[LOS_IDX["TGD[m]"]]  # Total Group Delay Delay
    
    # Mono-Freq. clock
    CLKP1 = CLKP1P2 - TGD + DTR

    # Calculate Residuals for Code Measurements C1    
    RESC1 = PSRC1 - (RGE - CLKP1 + IONO + TROPO)
        
    # Plot settings    
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = "Residuals C1C vs Time from TLSA on Year 2015 DoY 006"

    PlotConf["yLabel"] = "Residuals [Km]"
    PlotConf["xLabel"] = "Hour of Day 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    
    PlotConf["Grid"] = True
    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "GPS-PRN"
    PlotConf["ColorBarMin"] =  min(prn)
    PlotConf["ColorBarMax"] = max(prn)
    PlotConf["ColorBarTicks"] = range(max(prn))

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H  # Converting to hours
    PlotConf["yData"][Label] = RESC1 / 1000 # Residuals in [Km] for Code Measurements C1 data
    PlotConf["zData"][Label] = prn  # PRN data
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/MSR/' + 'MEAS_RESIDUALS_vs_TIME_TLSA_D006Y15.png'  # Adjust path as needed
    
    # Generate plot
    generatePlot(PlotConf)