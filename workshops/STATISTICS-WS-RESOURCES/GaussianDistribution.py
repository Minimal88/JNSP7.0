#!/usr/bin/env python

# GNSS Academy Copyright 2023
# Name: GaussianDistribution.py

# Dependencies
# numpy
# scipy
# matplotlib

# Some configuration
NSAMP = 10000
NSEED = 0
DPI   = 150

# Analyses selection
ALL = 1
NORM1=0
NORM2=0
NORM3=0

# Import external libraries
import numpy as np
from scipy.stats import norm
from scipy.special import erfinv
import matplotlib.pyplot as plt





# Get Gaussian shooting
def getGaussianShooting(nseed, N):
    # Select seed
    np.random.seed(seed=nseed)

    # Generate random samples following a Gaussian distribution
    return np.random.randn(N)





# Get Gaussian Sigma vs Samples Percentile
def plotGaussianSigmaVsPercentile(x, y):

    # Get ones array
    ones = np.ones(len(x))

    # Open figure
    fig, ax = plt.subplots(figsize=(8,2), dpi=DPI)
    
    # Plot second set of samples
    ax.plot(y, 2*ones, linewidth=0, marker='.', color='r')
    ax.plot(np.std(x), 2, linewidth=0, marker='+', 
    markersize=10, label='1sigma', color='lightblue')
    ax.plot(2*np.std(x), 2, linewidth=0, marker='+', 
    markersize=10, label='2sigma', color='b')
    ax.plot(3*np.std(x), 2, linewidth=0, marker='+', 
    markersize=10, label='3sigma', color='k')

    # Plot first set of samples
    ax.plot(x, ones, linewidth=0, marker='.', color='r')
    ax.plot(np.percentile(abs(x),68.3), 1, linewidth=0, marker='*', 
    markersize=10, label='68.3% Percentile', color='lightblue')
    ax.plot(np.percentile(abs(x),95.4), 1, linewidth=0, marker='*', 
    markersize=10, label='95.4% Percentile', color='b')
    ax.plot(np.percentile(abs(x),99.7), 1, linewidth=0, marker='*', 
    markersize=10, label='99.7% Percentile', color='k')
    
    # Arrange plot
    ax.set_title('%d samples' % len(x))
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_xticks(range(-7,7))
    ax.set_ylim([0,3])
    ax.set_xlim([-1+min(x.min(), y.min()), 4+max(x.max(), y.max())])
    ax.grid()
    ax.legend(loc='best')
    plt.show()




# PDF vs Histogram
def plotGaussianPdfVsHistogram(x):

    # Open figure
    fig, ax = plt.subplots(figsize=(8,3), dpi=DPI)
    
    # Plot histogram
    ax.hist(x, bins=20, density=True, label='Density of x',
    color='lightblue',
    edgecolor='w')

    # Plot Gaussian PDF
    t=np.arange(-5,5,.01)
    ax.plot(t, norm.pdf(t, 0, 1),
    c='blue',
    label='Gaussian PDF')

    
    # Arrange plot
    ax.set_title('%d samples' % len(x))
    ax.grid()
    plt.show()





# CDF vs Cumulated Frequency
def plotGaussianCdfVsCumulatedFrequency(x):

    # Open figure
    fig, ax = plt.subplots(figsize=(8,3), dpi=DPI)
    
    # Plot Cumulated Density
    ax.hist(x, bins=20, 
    cumulative=True, density=True, 
    label='Cumulated Density of x',
    color='lightblue',
    edgecolor='w')

    # Plot Gaussian CDF
    t=np.arange(min(x),max(x),.01)
    ax.plot(t, norm.cdf(t, 0, 1),
    c='blue',
    label='Gaussian CDF')

    
    # Arrange plot
    ax.set_title('%d samples' % len(x))
    ax.grid()
    plt.show()

    if True:
        # Open figure
        fig, ax = plt.subplots(figsize=(8,3), dpi=DPI)
        
        # Plot 1 - Cumulated Density
        hist, bin_edges = np.histogram(x, bins=20,
        density=True)
        cumdensity = np.cumsum(hist)/np.sum(hist)
        ax.bar(bin_edges[1:], 1-cumdensity,
        label='1 - Cumulated Density of x',
        color='lightblue',
        edgecolor='w',
        width=(bin_edges[1]-bin_edges[0]))

        # Plot Gaussian PDF
        t=np.arange(min(x), max(x),.001)
        ax.plot(t, 1-norm.cdf(t, 0, 1),
        c='blue',
        label='1 - CDF')

        # Arrange plot
        plt.yscale('log')
        ax.set_title('%d samples' % len(x))
        ax.grid()
        plt.show()



#---------------------------------------------
# MAIN PROCESSING
#---------------------------------------------

# Gaussian distribution
#---------------------------------------------
# Gaussian vs Percentile
if ALL or NORM1:
    xSamples = getGaussianShooting(NSEED, NSAMP)
    ySamples = np.copy(xSamples)

    plotGaussianSigmaVsPercentile(xSamples, ySamples)

# Gaussian 
if ALL or NORM2:
    xSamples = getGaussianShooting(NSEED, NSAMP)

    plotGaussianPdfVsHistogram(xSamples)

if ALL or NORM3:
    xSamples = getGaussianShooting(NSEED, NSAMP)

    plotGaussianCdfVsCumulatedFrequency(xSamples)

print()