#!/usr/bin/env python

# GNSS Academy Copyright 2023
# Name: EstimationProblems.py

# Dependencies
# numpy
# matplotlib

# Some configuration
NSEED=0
DPI=200

# Analyses selection
ALL       = 1
LINELSQ   = 0
LINEWLSQ  = 0
PARABOLA  = 0

# Import external libraries
import numpy as np
import matplotlib.pyplot as plt


# (W)LSQ
#---------------------------------------------
def estimateLineFittingLsq(xmeas, ymeas):
    onescol = np.ones(len(xmeas))
    
    # Build G matrix
    G = np.column_stack((onescol, xmeas))
    
    # LSQ solution
    a, b = np.linalg.inv(G.T @ G) @ G.T @ ymeas

    # Get dilution of precision due to geometry
    dop = np.sqrt(np.trace(np.linalg.inv(G.T @ G)))

    return a, b, dop

def estimateLineFittingWlsq(xmeas, ymeas, weights):
    onescol = np.ones(len(xmeas))
    
    # Build G matrix
    G = np.column_stack((onescol, xmeas))

    # Build W matrix
    W = np.diag(weights)
    
    # LSQ solution
    a, b = np.linalg.inv(G.T @ W @ G) @ G.T @ W @ ymeas

    # Get dilution of precision due to geometry
    dop = np.sqrt(np.trace(np.linalg.inv(G.T @ G)))

    return a, b, dop





# Line LSQ
#---------------------------------------------
def estimateLineLsq(xmeas, measerrors, name, weights=np.array([])):
    # Get xaxis samples
    xaxis = np.arange(21)
    
    # Define reference line
    aref = 5
    bref = 2
    yref = aref + bref * xaxis
    reflegend = f'Reference: y={aref:.0f}+{bref:.0f}x'

    # Generate measurements
    ymeas = yref[xmeas] + measerrors
    
    # Fit regression line
    if len(weights) == 0:
        afit, bfit, dop = estimateLineFittingLsq(xmeas, ymeas)

    else:
        afit, bfit, dop = estimateLineFittingWlsq(xmeas, ymeas, weights)
    
    fitlegend = f'Fitting: y={afit:.2f}+{bfit:.2f}x with DOP={dop:.2f}'

    # Get estimation errors
    aerror = abs(afit - aref)
    berror = abs(bfit - bref)
    yfit = afit + bfit*xaxis
    fiterrors = yfit - yref

    # Plot
    fig, ax = plt.subplots()
    
    # Plot reference
    ax.plot(xaxis, yref, label=reflegend)
    
    # Plot measurements
    ax.plot(xmeas, ymeas, linewidth=0, marker='s', label='Data points')
    
    # Plot measurement errors
    ax.plot(xmeas, measerrors, linewidth=0, marker='x',
            color='brown',
            label='Measurement Error RMS = %.2f' % 
            np.sqrt(np.mean(measerrors**2)))
    ax.set_xlabel('x')
    ax.set_ylim([-25, 70])
    ax.set_ylabel('y')
    ax.legend(facecolor='white')
    ax.set_title(name)
    ax.grid()

    # Plot fitting line and fitting errors
    ax.plot(xaxis, yfit, color='purple', label=fitlegend)
    ax.plot(xaxis, fiterrors, marker='.', color = 'r',
            label='|Fit - Reference| Errors: $\Delta$a = %.2f, $\Delta$b %.2f' % 
            (aerror,
             berror))
    ax.legend(facecolor='white')
    
    # Save figure
    fig.savefig(name + '.png', dpi=DPI)
    plt.close('all')

def runLineLsq(sigmaerr):
    # Get measurements' x coordinates
    x0 = np.arange(21)

    # Select seed
    np.random.seed(seed=NSEED)

    # Get gaussian measurement errors
    measerrors = sigmaerr * np.random.randn(len(x0))

    # Fit line with a LSQ
    name = 'LSQ - 2 measurements'
    xmeas = np.array([x0[1], x0[-2]])
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - 2 measurements with larger errors'
    xmeas = np.array([x0[2], x0[-3]])
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - 2 measurements with a bias'
    xmeas = np.array([x0[2], x0[-3]])
    bias = 2
    estimateLineLsq(xmeas, measerrors[xmeas] + bias, name)
    
    name = 'LSQ - 5 measurements'
    xmeas = x0[:-1:4]
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - Another 5 measurements'
    xmeas = x0[1::4]
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - 5 crowded measurements'
    xmeas = x0[-5:]
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - 5 measurements in 2 clusters'
    xmeas = np.concatenate((x0[:3], x0[-2:]))
    estimateLineLsq(xmeas, measerrors[xmeas], name)

    name = 'LSQ - 10 measurements'
    xmeas = x0[::2]
    estimateLineLsq(xmeas, measerrors[xmeas], name)
    
    name = 'LSQ - 20 measurements'
    xmeas = x0
    estimateLineLsq(x0, measerrors[xmeas], name)
    
    # Introduce outliers
    measerrorswoutlier = measerrors.copy()
    measerrorswoutlier[-5] = measerrorswoutlier[-5] - 20

    name = 'LSQ - 5 measurements with outlier'
    xmeas = x0[::4]
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name)
    
    name = 'LSQ - 10 measurements with outlier'
    xmeas = x0[::2]
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name)
    
    name = 'LSQ - 20 measurements with outlier'
    xmeas = x0
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name)





# Line WLSQ
#---------------------------------------------
def runLineWlsq(sigmaerr):
    # Get measurements' x coordinates
    x0 = np.arange(21)

    # Select seed
    np.random.seed(seed=NSEED)

    # Get gaussian measurement errors
    measerrors = sigmaerr * np.random.randn(len(x0))

    # Get weights
    w = np.ones(len(x0))

    name = 'WLSQ - 5 measurements with all weights = 1'
    xmeas = x0[:-1:4]
    estimateLineLsq(xmeas, measerrors[xmeas], name, weights=w[xmeas])
    
    # Multiply all weights by 100
    w = 100 * w

    name = 'WLSQ - 5 measurements with all weights = 100'
    xmeas = x0[:-1:4]
    estimateLineLsq(xmeas, measerrors[xmeas], name, weights=w[xmeas])
    
    # Introduce an outlier
    measerrorswoutlier = measerrors.copy()
    measerrorswoutlier[-5] = measerrorswoutlier[-5] - 20

    # Reduce the weight of the outlier
    w[-5] = 1

    name = 'WLSQ - 5 measurements with outlier weighting 1%'
    xmeas = x0[::4]
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name, weights=w[xmeas])
    
    name = 'WLSQ - 10 measurements with outlier weighting 1%'
    xmeas = x0[::2]
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name, weights=w[xmeas])
    
    name = 'WLSQ - 20 measurements with outlier weighting 1%'
    xmeas = x0
    estimateLineLsq(xmeas, measerrorswoutlier[xmeas], name, weights=w[xmeas])





# Parabola
#---------------------------------------------
def estimateParabolaFittingWlsq(xmeas, ymeas, weights):
    onescol = np.ones(len(xmeas))
    
    # Build G matrix
    G = np.column_stack((onescol, xmeas, xmeas**2))

    # Build W matrix
    W = np.diag(weights)
    
    # LSQ solution
    a, b, c = np.linalg.inv(G.T @ W @ G) @ G.T @ W @ ymeas

    # Get dilution of precision due to geometry
    dop = np.sqrt(np.trace(np.linalg.inv(G.T @ G)))

    return a, b, c, dop


def estimateParabolaLsq(xmeas, measerrors, name, weights=np.array([])):
    # Get xaxis samples
    xaxis = np.arange(21)
    
    # Define reference parabola
    aref = 5
    bref = 0.5
    cref = 0.25
    yref = aref + bref * xaxis + cref * xaxis**2
    reflegend = f'Reference: y={aref:.0f}+{bref:.2f}x+{cref:.2f}x$^2$'

    # Generate measurements
    ymeas = yref[xmeas] + measerrors
    
    # Fit parabola
    if len(weights) == 0:
        weights = np.ones(len(xmeas))

    afit, bfit, cfit, dop = estimateParabolaFittingWlsq(xmeas, ymeas, weights)
    
    fitlegend = f'Fitting: y={afit:.2f}+{bfit:.2f}x+{cfit:.2f}x$^2$'
    'with DOP={dop:.2f}'

    # Get estimation errors
    aerror = abs(afit - aref)
    berror = abs(bfit - bref)
    cerror = abs(cfit - cref)
    yfit = afit + bfit*xaxis + cfit*(xaxis**2)
    fiterrors = yfit - yref

    fig, ax = plt.subplots()
    
    # Plot reference
    ax.plot(xaxis, yref, label=reflegend)
    
    # Plot measurements
    ax.plot(xmeas, ymeas, linewidth=0, marker='s', label='Data points')
    
    # Plot measurement errors
    ax.plot(xmeas, measerrors, linewidth=0, marker='x',
            color='brown',
            label='Measurement Error RMS = %.2f' % 
            np.sqrt(np.mean(measerrors**2)))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend(facecolor='white')
    ax.set_title(name)
    ax.grid()

    # Plot fitting parabola and fitting errors
    ax.plot(xaxis, yfit, color='purple', label=fitlegend)
    ax.plot(xaxis, fiterrors, marker='.', color = 'r',
            label='|Fit - Reference| Errors: $\Delta$a = %.2f, $\Delta$b %.2f, $\Delta$c %.2f' % 
            (aerror,
             berror,
             cerror))
    ax.legend(facecolor='white')
    
    # Save figure
    fig.savefig(name + '.png', dpi=DPI)
    plt.close('all')

def runParabolaWlsq(sigmaerr):
    # Get measurements' x coordinates
    x0 = np.arange(21)

    # Select seed
    np.random.seed(seed=NSEED)

    # Get gaussian measurement errors
    measerrors = sigmaerr * np.random.randn(len(x0))

    # Get weights
    w = np.ones(len(x0))

    name = 'Parabola - 10 measurements with all weights = 1'
    xmeas = x0[::2]
    estimateParabolaLsq(xmeas, measerrors[xmeas], name, weights=w[xmeas])

    name = 'Parabola - 20 measurements with all weights = 1'
    xmeas = x0
    estimateParabolaLsq(xmeas, measerrors[xmeas], name, weights=w[xmeas])





#---------------------------------------------
# MAIN PROCESSING
#---------------------------------------------

# Line fit
#---------------------------------------------
# Select the sigma of the errors
sigmaerr = 5

if ALL or LINELSQ:
    runLineLsq(sigmaerr)

if ALL or LINEWLSQ:
    runLineWlsq(sigmaerr)

if ALL or PARABOLA:
    runParabolaWlsq(sigmaerr)
