
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import conda
CondaFileDir = conda.__file__
CondaDir = CondaFileDir.split('lib')[0]
ProjLib = os.path.join(os.path.join(CondaDir, 'share'), 'proj')
os.environ["PROJ_LIB"] = ProjLib
from mpl_toolkits.basemap import Basemap

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

#import PlotsConstants as Const


# ------------------------------------------------------------------------------------
# INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------

def createFigure(PlotConf):
    try:
        fig, ax = plt.subplots(1, 1, figsize = PlotConf["FigSize"])
    
    except:
        fig, ax = plt.subplots(1, 1)

    return fig, ax

def saveFigure(fig, Path):
    Dir = os.path.dirname(Path)
    try:
        os.makedirs(Dir)
    except: pass
    fig.savefig(Path, dpi=150., bbox_inches='tight')

def prepareAxis(PlotConf, ax):
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    for key in PlotConf:
        if key == "Title":
            ax.set_title(PlotConf["Title"])

        for axis in ["x", "y"]:
            if axis == "x":
                if key == axis + "Label":
                    ax.set_xlabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_xticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_xticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_xlim(PlotConf[axis + "Lim"])

            if axis == "y":
                if key == axis + "Label":
                    ax.set_ylabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_yticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_yticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_ylim(PlotConf[axis + "Lim"])

        if key == "Grid" and PlotConf[key] == True:
            ax.grid(linestyle='--', linewidth=0.5, which='both')

def prepareColorBar(PlotConf, ax, Values):
    try:
        Min = PlotConf["ColorBarMin"]
    except:
        Mins = []
        for v in Values.values():
            Mins.append(min(v))
        Min = min(Mins)
    try:
        Max = PlotConf["ColorBarMax"]
    except:
        Maxs = []
        for v in Values.values():
            Maxs.append(max(v))
        Max = max(Maxs)
    normalize = mpl.cm.colors.Normalize(vmin=Min, vmax=Max)

    divider = make_axes_locatable(ax)
    # size size% of the plot and gap of pad% from the plot
    color_ax = divider.append_axes("right", size="3%", pad="2%")
    cmap = mpl.cm.get_cmap(PlotConf["ColorBar"])
    
    if "ColorBarTicks" in PlotConf:
        cbar = mpl.colorbar.ColorbarBase(color_ax, 
        cmap=cmap,
        norm=mpl.colors.Normalize(vmin=Min, vmax=Max),
        label=PlotConf["ColorBarLabel"],
        ticks=PlotConf["ColorBarTicks"])
    else: 
        cbar = mpl.colorbar.ColorbarBase(color_ax, 
        cmap=cmap,
        norm=mpl.colors.Normalize(vmin=Min, vmax=Max),
        label=PlotConf["ColorBarLabel"])

    return normalize, cmap

def drawMap(PlotConf, ax,):
    Map = Basemap(projection = 'cyl',
    llcrnrlat  = PlotConf["LatMin"]-0,
    urcrnrlat  = PlotConf["LatMax"]+0,
    llcrnrlon  = PlotConf["LonMin"]-0,
    urcrnrlon  = PlotConf["LonMax"]+0,
    lat_ts     = 10,
    resolution = 'l',
    ax         = ax)

    # Draw map meridians
    Map.drawmeridians(
    np.arange(PlotConf["LonMin"],PlotConf["LonMax"]+1,PlotConf["LonStep"]),
    labels = [0,0,0,1],
    fontsize = 6,
    linewidth=0.2)
        
    # Draw map parallels
    Map.drawparallels(
    np.arange(PlotConf["LatMin"],PlotConf["LatMax"]+1,PlotConf["LatStep"]),
    labels = [1,0,0,0],
    fontsize = 6,
    linewidth=0.2)

    # Draw coastlines
    Map.drawcoastlines(linewidth=0.5)

    # Draw countries
    Map.drawcountries(linewidth=0.25)

def generateLinesPlot(PlotConf):
    LineWidth = 1.5

    fig, ax = createFigure(PlotConf)

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]
        if key == "ColorBar":
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)

    for Label in PlotConf["yData"].keys():
        if "ColorBar" in PlotConf:
            ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label], 
            marker = PlotConf["Marker"][Label],
            linewidth = LineWidth,
            c = cmap(normalize(np.array(PlotConf["zData"][Label]))))

        else:
            ax.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
            marker = PlotConf["Marker"][Label],
            color = PlotConf["Color"][Label],
            linewidth = LineWidth,
            label = Label)

    if "ShowLegend" in PlotConf:
         # Create legends for each label
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = list(set(labels))
        legend_handles = [handles[labels.index(label)] for label in unique_labels]
        ax.legend(
            legend_handles, unique_labels, loc=PlotConf["ShowLegend"], fontsize='medium')
        
    saveFigure(fig, PlotConf["Path"])

def generateVerticalBarPlot(PlotConf):
    LineWidth = 1.5
    
    fig, ax = createFigure(PlotConf)

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]        
        if key == "ColorBar":
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)

    for Label in PlotConf["yData"].keys():
        if "ColorBar" in PlotConf:
            ax.bar(PlotConf["xData"][Label], PlotConf["yData"][Label],
                   color=cmap(normalize(np.array(PlotConf["zData"][Label]))))
        else:
            if "Color" not in PlotConf:
                Color = 'b'
            else:
                Color = PlotConf["Color"][Label]

            ax.bar(
                PlotConf["xData"][Label], 
                PlotConf["yData"][Label],                
                color = Color,
                linewidth = LineWidth,
                label = Label)
    
    if "ShowLegend" in PlotConf:
         # Create legends for each label
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = list(set(labels))
        legend_handles = [handles[labels.index(label)] for label in unique_labels]
        ax.legend(
            legend_handles, unique_labels, loc=PlotConf["ShowLegend"], fontsize='medium')

    saveFigure(fig, PlotConf["Path"])



# ------------------------------------------------------------------------------------
# EXTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------


def generatePlot(PlotConf):
    if(PlotConf["Type"] == "Lines"):
        generateLinesPlot(PlotConf)
    elif PlotConf["Type"] == "VerticalBar":
        generateVerticalBarPlot(PlotConf)

def createPlotConfig2DVerticalBars(filepath, title, xData, yDataList, xLabel, yLabels, colors, legPos, yOffset = [0,0]):
    """
    Creates a new Plot Configuration for plotting vertical 2D bars.
    Y-axis: Multiple sets of data received from lists of lists
    X-asis: A single set of data from a list

    Parameters:
        filepath (str): Path to save the plot figure.
        title (str): Title of the plot figure.
        xData (list): List of x-axis data.
        yDataList (list): List of lists containing y-axis data sets.
        xLabel (str): Label of x-axis data.
        yLabels (list): List of labels for each y-axis data set.
        colors (list): List of colors for each y-axis data set.
        legPos (str): Position of the legend (example: 'upper left').
        yOffset (list): List of y-axis offsets: [lowerOffset, upperOffset]
    
    Returns:
        PlotConf(list): Configuration Data Structure for plotting Vertical 2D Bars with generatePlot()
    """
    PlotConf = {}
    PlotConf["Type"] = "VerticalBar"
    PlotConf["FigSize"] = (12, 6)
    PlotConf["Title"] = title
    PlotConf["xLabel"] = xLabel
    PlotConf["xTicks"] = range(0, len(xData))
    PlotConf["xLim"] = [-1, len(xData)]
    minY = min([min(y) for y in yDataList])
    maxY = max([max(y) for y in yDataList])
    PlotConf["yLim"] = [minY + yOffset[0], maxY + yOffset[1]]
    PlotConf["Grid"] = True    
    PlotConf["LineWidth"] = 1
    if legPos: PlotConf["ShowLegend"] = legPos
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}    
    PlotConf["Color"] = {}    
    PlotConf["Path"] = filepath
    for yLabel, yData, color in zip(yLabels, yDataList, colors):        
        PlotConf["yData"][yLabel] = yData
        PlotConf["xData"][yLabel] = xData
        PlotConf["Color"][yLabel] = color        
    
    return PlotConf

def createPlotConfig2DLines(filepath, title, xData, yDataList, xLabel, yLabels, colors, markers, legPos, yOffset=[0, 0], applyLimits = True):
    """
    Creates a new Plot Configuration for plotting 2D lines with points.
    
    Parameters:
        filepath (str): Path to save the plot figure.
        title (str): Title of the plot figure.
        xData (list): List of x-axis data.
        yDataList (list): List of lists containing y-axis data sets.
        xLabel (str): Label of x-axis data.
        yLabels (list): List of labels for each y-axis data set.
        colors (list): List of colors for each y-axis data set.
        markers (list): List of markers for each y-axis data set.
        legPos (str): Position of the legend (example: 'upper left'). // If null or empty the Legend is disabled
        yOffset (list): List of y-axis offsets: [lowerOffset, upperOffset]. // By default = [0,0] 
        applyLimits (bool): True for applying the Limits of x-axis and y-axis. // By Default = True

    Returns:
        PlotConf (dict): Configuration Data Structure for plotting 2D lines with points using generateLinesPlot().
    """
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12, 6)
    PlotConf["Title"] = title
    PlotConf["xLabel"] = xLabel
    if legPos: PlotConf["ShowLegend"] = legPos
    if applyLimits:
        PlotConf["xTicks"] = range(0, len(xData))
        PlotConf["xLim"] = [0, len(xData)-1]
        minY = min([min(y) for y in yDataList])
        maxY = max([max(y) for y in yDataList])
        PlotConf["yLim"] = [minY + yOffset[0], maxY + yOffset[1]]    
    PlotConf["Grid"] = True
    PlotConf["LineWidth"] = 1    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}
    PlotConf["Marker"] = {}
    PlotConf["Path"] = filepath
    for yLabel, yData, color, marker in zip(yLabels, yDataList, colors, markers):
        PlotConf["yData"][yLabel] = yData
        PlotConf["xData"][yLabel] = xData
        PlotConf["Color"][yLabel] = color
        PlotConf["Marker"][yLabel] = marker

    return PlotConf

def createPlotConfig2DLinesColorBar(filepath, title, xData, yData, zData, xLabel, yLabel, zLabel,  marker, applyLimits = True):
    """
    Creates a new Plot Configuration for plotting 2D lines with a color bar.

    Parameters:
        filepath (str): Path to save the plot figure.
        title (str): Title of the plot figure.
        xData (list): List of x-axis data.
        yData (list): List of y-axis data.
        zData (list): List of z-axis data for color mapping.
        xLabel (str): Label of x-axis data.
        yLabel (str): Label of y-axis data.
        zLabel (str): Label of z-axis data.        
        marker (str): Marker for the plot.
        applyLimits (bool): True for applying the Limits of x-axis and y-axis. // By Default = True

    Returns:
        PlotConf (dict): Configuration Data Structure for plotting 2D lines with a color bar using generateLinesPlot().
    """
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = title
    PlotConf["yLabel"] = yLabel
    PlotConf["xLabel"] = xLabel
    if applyLimits:
        PlotConf["xTicks"] = range(0, len(xData))
        PlotConf["xLim"] = [0, len(xData)-1]
        minY = min([min(y) for y in yData])
        maxY = max([max(y) for y in yData])
        PlotConf["yLim"] = [minY, maxY]    
        
    PlotConf["LineWidth"] = 1.5
    PlotConf["Grid"] = True    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    PlotConf["Color"] = {}
    PlotConf["Marker"] = {}
    PlotConf["Marker"][yLabel] = marker    
    PlotConf["xData"][yLabel] = xData
    PlotConf["yData"][yLabel] = yData    
    PlotConf["zData"][yLabel] = zData  
    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = zLabel
    PlotConf["ColorBarMin"] = min(zData)
    PlotConf["ColorBarMax"] = max(zData)      
    PlotConf["Path"] = filepath

    return PlotConf
