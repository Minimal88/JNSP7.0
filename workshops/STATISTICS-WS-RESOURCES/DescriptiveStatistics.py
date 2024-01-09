#!/usr/bin/env python

# GNSS Academy Copyright 2023
# Name: DescriptiveStatistics.py

# Dependencies
# numpy
# scipy
# matplotlib
# pandas

# Some configuration
NSEED=0
DPI=150

# Analyses selection
ALL = 1
CENTR=0
PANDA=0
OTFLY=0

# Import external libraries
import numpy as np
from scipy.stats import norm
from scipy.special import erfinv
import matplotlib.pyplot as plt
from collections import OrderedDict
from pandas import read_csv





# Get Gaussian shooting
def getGaussianShooting(nseed, N):
    # Select seed
    np.random.seed(seed=nseed)

    # Generate random samples following a Gaussian distribution
    return np.random.randn(N)




# Mean vs Median
#---------------------------------------------
def plotCentralTendencyExample(x, y):

    # Get ones array
    ones = np.ones(len(x))

    # Open figure
    fig, ax = plt.subplots(figsize=(8,2), dpi=DPI)
    
    # Plot second set of samples
    ax.plot(y, 2*ones, linewidth=0, marker='.', label='y')
    ax.plot(y.mean(), 2*1, linewidth=0, marker='+', 
    markersize=10, label='y Mean',)
    ax.plot(np.median(y), 2*1, linewidth=0, marker='+', 
    markersize=10, label='y Median',)
    
    # Plot first set of samples
    ax.plot(x, ones, linewidth=0, marker='.', label='x')
    ax.plot(x.mean(), 1, linewidth=0, marker='+', 
    markersize=10, label='x Mean',)
    ax.plot(np.median(x), 1, linewidth=0, marker='+', 
    markersize=10, label='x Median', color='b')
    
    # Arrange plot
    ax.set_title('%d samples' % len(x))
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_xticks(range(-7,7))
    ax.set_ylim([0,3])
    ax.set_xlim([-1+min(x.min(), y.min()), 3+max(x.max(), y.max())])
    ax.grid()
    ax.legend(loc='best')
    plt.show()





# Compute Statistics with pandas
#---------------------------------------------
def computeStatsWithPandas(PosFile):
    PosInfo = read_csv(PosFile, 
                       delim_whitespace=True, 
                       skiprows=1, 
                       header=None,
                       usecols=[7,8,9])
    PosInfo = \
        PosInfo.rename(columns={7: 'EPE',
                                8: 'NPE',
                                9: 'UPE'})
    print(PosInfo.describe())



# Statistics on-the-fly
#---------------------------------------------

# Function to update a histogram with a new sample
def updateHist(Hist, Value, Resolution):
    # Get the bin representative
    Bin = float(int(Value/Resolution)) * Resolution
    
    # Add one more sample to the bin, if it exists
    if Bin in Hist:
        Hist[Bin] = Hist[Bin] + 1

    # Create the bin with one samples if it doesn't exist
    else:
        Hist[Bin] = 1

# Compute the CDF from a Histogram
def computeCdfFromHistogram(Histogram, NSamples):
    # Sort histogram
    SortedHist = OrderedDict({})
    for key in sorted(Histogram.keys()):
        SortedHist[key] = Histogram[key]

    # Initialize CDF and number of samples
    Cdf = OrderedDict({})
    CumulatedSamples = 0

    # Cumulate the frequencies
    for Bin, Samples in SortedHist.items():
        CumulatedSamples = CumulatedSamples + Samples
        Cdf[Bin] = float(CumulatedSamples) / NSamples

    return Cdf

# Compute the Percentile from the CDF
def computePercentile(Cdf, Percentile):
    for Bin, Freq in Cdf.items():
        # If the cumulated frequency exceeds the Percentile
        # we're trying to find, we found our Percentile
        if (Freq * 100) > Percentile:
            return Bin

    return Bin

# Compute the Sigma of the Overbounding Gaussian
def computeOverboundingSigma(Cdf, MinP):
    OverboundingSigma = 0

    for Bin, Freq in Cdf.items():
        # Only overbound percentiles higher than MinP
        if (Freq * 100) > MinP and Freq < 1:
            # Equivalent Sigma of the Overbounding Gaussian
            # of the bin
            EqSigma = Bin /\
                 (np.sqrt(2) * erfinv(Freq))
        
            # Keep the maximum sigma among all bins
            OverboundingSigma = max(EqSigma, OverboundingSigma)

    return OverboundingSigma

# Compute Statistics On-the-fly
def computeStatsOnTheFly(PosFile):

    # Initialize summary dictionaries
    HpeStats = 'HPE Stats'
    VpeStats = 'VPE Stats'
    Max  = 'Max'
    Avg  = 'Avg'
    Rms  = 'RMS'
    P95  = '95%'
    Num  = 'Num'
    Ext  = 'Ext'

    Stats0 = {
        Max: 0,
        Avg: 0,
        Rms: 0,
        P95: 0,
        Num: 0,

    }

    Stats = {
        HpeStats: Stats0,
        VpeStats: Stats0.copy(),

    }
    Stats[VpeStats][Ext] = 0

    # Initialize histograms of the parameters
    # we want to describe
    HpeHist = {}
    VpeHist = {}
    
    # Parse the POS file
    with open(PosFile, 'r') as f:
        for line in f:
            # Skip comments
            if '#' not in line:
                # Get East, North and Up Position Errors
                fields = line.split()
                epe = float(fields[7])
                npe = float(fields[8])
                upe = float(fields[9])
                
                # Compute the Horizontal and Vertical Position
                # Error
                hpe = np.sqrt(epe**2 + npe**2)
                vpe = abs(upe)

                # Increment number of samples
                Stats[HpeStats][Num] += 1
                Stats[VpeStats][Num] += 1

                # Keep maximum
                if hpe > Stats[HpeStats][Max]:
                    Stats[HpeStats][Max] = hpe

                if vpe > Stats[VpeStats][Max]:
                    Stats[VpeStats][Max] = vpe

                # Update the sum of all the samples
                Stats[HpeStats][Avg] += hpe
                Stats[VpeStats][Avg] += vpe

                # Update the sum of all the samples squares
                Stats[HpeStats][Rms] += hpe**2
                Stats[VpeStats][Rms] += vpe**2

                # Account for the sample in the histogram
                updateHist(HpeHist, hpe, 0.001)
                updateHist(VpeHist, vpe, 0.001)

    # End of with open(PosFile, 'r') as f:

    # Compute mean: sum(xi)/N
    Stats[HpeStats][Avg] /= Stats[HpeStats][Num]
    Stats[VpeStats][Avg] /= Stats[VpeStats][Num]
    
    # Compute RMS: sqrt(sum(xi^2)/N)
    Stats[HpeStats][Rms] = np.sqrt(\
                                   Stats[HpeStats][Rms] /\
                                   Stats[HpeStats][Num]
                                )
    Stats[VpeStats][Rms] = np.sqrt(\
                                   Stats[VpeStats][Rms] /\
                                   Stats[VpeStats][Num]
                                )

    # Compute HPE CDF from histogram
    Cdf = computeCdfFromHistogram(HpeHist, Stats[HpeStats][Num])

    # Compute 95% percentile
    Stats[HpeStats][P95] = computePercentile(Cdf, 95)

    # Compute VPE CDF from histogram
    Cdf = computeCdfFromHistogram(VpeHist, Stats[VpeStats][Num])

    # Compute 95% percentile
    Stats[VpeStats][P95] = computePercentile(Cdf, 95)

    # Compute Extrapolated VPE
    Stats[VpeStats][Ext] = 5.33 * computeOverboundingSigma(Cdf, 60,)

    # Display Statistics
    for param in Stats:
        print(param)
        print("#--------------")
        for stat in Stats[param]:
            print(stat,'=', "%.3f" % (Stats[param][stat]))

    return


#---------------------------------------------
# MAIN PROCESSING
#---------------------------------------------

# Mean vs Median
#---------------------------------------------
if ALL or CENTR:
    xSamples = getGaussianShooting(NSEED, 10)
    ySamples = np.copy(np.sort(xSamples))
    ySamples[-1] = 6
    ySamples[-2] = 5.5

    plotCentralTendencyExample(xSamples, ySamples)

# Statistics with pandas
#---------------------------------------------
if ALL or PANDA:
    PosFile = '/Users/tapiasa/PROJECTS/GNSS-ACADEMY/WORKSHOP/'\
    'STATISTICS/RESOURCES/TLSA00615_PosInfo_5s.dat'

    computeStatsWithPandas(PosFile)

# Statistics On-the-fly
#---------------------------------------------
if ALL or OTFLY:
    PosFile = '/Users/tapiasa/PROJECTS/GNSS-ACADEMY/WORKSHOP/'\
    'STATISTICS/RESOURCES/TLSA00615_PosInfo_5s.dat'

    computeStatsOnTheFly(PosFile)

print()