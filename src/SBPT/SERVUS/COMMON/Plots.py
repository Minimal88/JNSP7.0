
import sys, os
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
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
    plt.close(fig)  # Close the figure to release memory

def prepareAxis(PlotConf, ax):
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    for key in PlotConf:
        if key == "Title":
            ax.set_title(PlotConf["Title"])

        for axis in ["x", "y"]:
            if axis == "x":
                if key == axis + "Label":
                    ax.set_xlabel(PlotConf[axis + "Label"], labelpad=20)

                if key == axis + "Ticks":
                    ax.set_xticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_xticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_xlim(PlotConf[axis + "Lim"])

            if axis == "y":
                if key == axis + "Label":                    
                    if isinstance(PlotConf[axis + "Label"], dict):
                        ax.set_ylabel("", labelpad=5)
                    else:
                        ax.set_ylabel(PlotConf[axis + "Label"], labelpad=35)

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

    if PlotConf["ColorBar"] == "Availability_0_100":
        cmapTmp = mpl.cm.get_cmap("jet", 100)        
        newcolors = cmapTmp(np.linspace(0, 1, 100))
        gray = np.array([0.5, 0.5, 0.5, 1])
        start_index = int(0.99 * len(newcolors))  # Index corresponding to 99% of segments
        newcolors[start_index:, :] = gray
        cmap = ListedColormap(newcolors)
        
    elif PlotConf["ColorBar"] == "Availability_70_99":
        cmapTmp = mpl.cm.get_cmap("jet", 100)        
        newcolors = cmapTmp(np.linspace(0, 1, 100))       
        white = np.array([1, 1, 1, 1])
        end_index_white = int(0.7 * len(newcolors)) # Assign white color to the first 70% of segments
        newcolors[:end_index_white, :] = white

        gray = np.array([0.5, 0.5, 0.5, 1])
        start_index_gray = int(0.99 * len(newcolors)) # Assign gray color to the last 99% of segments
        newcolors[start_index_gray:, :] = gray

        # Create new colormap        
        cmap = ListedColormap(newcolors)

    else:
        cmap = mpl.cm.get_cmap(PlotConf["ColorBar"], 100)
    
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
    LineStyle = '-'

    fig, ax = createFigure(PlotConf)

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]
        if key == "LineStyle":
            LineStyle = PlotConf["LineStyle"]
        if key == "ColorBar":
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)
            
    ax2_handles = {}
    for Label in PlotConf["yData"].keys():
        if "Twin" in PlotConf:
            if (PlotConf["Twin"]["Label"] == Label):
                ax2 = ax.twinx()
                ax2.set_label(Label)
                ax2.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],                
                marker=PlotConf["Marker"][Label],
                linewidth = LineWidth,
                label = Label, 
                color=PlotConf["Color"][Label])
                #ax2.set_yticks(PlotConf["Twin_yTicks"])
                ax2.set_ylim(PlotConf["Twin"]["yLim"])

                # Get handles and labels
                handles, labels = ax.get_legend_handles_labels()

                # Get ax2 handles and labels
                ax2_handles, ax2_labels = ax2.get_legend_handles_labels()

                # Manually add twin handle
                handles.extend(ax2_handles)
                continue

        if "ColorBar" in PlotConf:
            ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label], 
            marker = PlotConf["Marker"][Label],
            linewidth = LineWidth,
            c = cmap(normalize(np.array(PlotConf["zData"][Label]))))

        if "Text" in PlotConf:
            # Add text to each point
            for i, txt in enumerate(PlotConf["Text"][Label]):
                x_coord = PlotConf["xData"][Label][i]
                y_coord = PlotConf["yData"][Label][i]
                # Check if coordinates are within the specified limits
                if PlotConf["xLim"][0] <= x_coord <= PlotConf["xLim"][1] and PlotConf["yLim"][0] <= y_coord <= PlotConf["yLim"][1]:
                    y = PlotConf["yData"][Label][i]
                    color = cmap(normalize(np.array(PlotConf["zData"][Label][i]))) if "ColorBar" in PlotConf else PlotConf["Color"][Label]
                    ax.text(PlotConf["xData"][Label][i], y + 0.5 , f'{txt}',
                            ha='center', va='bottom', fontsize=8, color=color)
        
        else:
            ax.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
            marker = PlotConf["Marker"][Label],
            color = PlotConf["Color"][Label],
            linewidth = LineWidth,
            LineStyle = LineStyle,
            label = Label)

            # When Using the 'Twin' configuration, make sure to use the last label
            if "Twin" in PlotConf:
                if (PlotConf["Twin"] == Label):
                    ax2 = ax.twinx()
                    ax2.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
                    PlotConf["Marker"],
                    linewidth = LineWidth,
                    label = Label, 
                    color='green')

                    #ax2.set_yticks(PlotConf["Twin_yTicks"])
                    ax2.set_ylim(PlotConf["Twin_yLim"])

        

    if "ShowLegend" in PlotConf:
         # Create legends for each label
        handles, labels = ax.get_legend_handles_labels()

        if "Twin" in PlotConf:
            handles.extend(ax2_handles)
            for h in ax2_handles: labels.append(h.get_label())                

        unique_labels = list(set(labels))
        legend_handles = [handles[labels.index(label)] for label in unique_labels]
        ax.legend(
            legend_handles, unique_labels, loc=PlotConf["ShowLegend"], fontsize='medium')
        
    saveFigure(fig, PlotConf["Path"])

def generateVerticalBarPlot(PlotConf):
    LineWidth = 1.5
    
    fig, ax = createFigure(PlotConf)

    Labels = PlotConf["yData"].keys()

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]        
        if key == "ColorBar":
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)

    legend_handles = []  # Collect handles for the legend
    
    for Label in Labels:
        if "Twin" in PlotConf:
            if (PlotConf["Twin"]["Label"] == Label):
                ax2 = ax.twinx()
                line = ax2.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
                "-", # Marker,
                linewidth = LineWidth,
                label = Label, 
                color=PlotConf["Color"][Label])
                #ax2.set_yticks(PlotConf["Twin_yTicks"])
                ax2.set_ylim(PlotConf["Twin"]["yLim"])[0]  
                # Extract the line object from the returned list
                legend_handles.append(Line2D([0], [0], color=PlotConf["Color"][Label], label=Label))
                continue

        if "ColorBar" in PlotConf:
            bar = ax.bar(
                PlotConf["xData"][Label], 
                PlotConf["yData"][Label],
                color=cmap(normalize(np.array(PlotConf["zData"][Label])))
            )
            legend_handles.append(Patch(color=bar[0].get_facecolor(), label=Label))
        else:
            if "Color" not in PlotConf:
                Color = 'b'
            else:
                Color = PlotConf["Color"][Label]

            bar = ax.bar(
                PlotConf["xData"][Label], 
                PlotConf["yData"][Label],                
                color=Color,
                linewidth=LineWidth,
                label=Label
            )
            legend_handles.append(Patch(color=bar[0].get_facecolor(), label=Label))

    
    if "ShowLegend" in PlotConf:
        # Create legends for each label         
        unique_labels = list(Labels)
        ax.legend(legend_handles, unique_labels, loc=PlotConf["ShowLegend"], fontsize='medium')


        # handles, labels = ax.get_legend_handles_labels()        
        # unique_labels = list(Labels)

        # legend_handles = [handles[labels.index(label)] for label in unique_labels]
        # ax.legend(
        #     legend_handles, unique_labels, loc=PlotConf["ShowLegend"], fontsize='medium')

    saveFigure(fig, PlotConf["Path"])

def generateInterpolatedMapPlot(PlotConf):
    # Create figure and axis
    fig, ax = createFigure(PlotConf)

    # Draw map if specified
    if "Map" in PlotConf and PlotConf["Map"]:
        drawMap(PlotConf, ax)
    if "ColorBar" in PlotConf:
        normalize, Cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])

    # Generate meshgrid for interpolation
    lon_grid, lat_grid = np.meshgrid(
        np.linspace(PlotConf["LonMin"], PlotConf["LonMax"], 100),
        np.linspace(PlotConf["LatMin"], PlotConf["LatMax"], 100)
    )

    # Interpolate zData (availability) on the meshgrid
    zData_interpolated = griddata(
        (PlotConf["xData"], PlotConf["yData"]), PlotConf["zData"], (lon_grid, lat_grid), method='cubic'
    )

    # Plot interpolated data
    contour = ax.contourf(lon_grid, lat_grid, zData_interpolated, cmap=Cmap)    

    # Set labels and title
    ax.set_xlabel(PlotConf["xLabel"], labelpad=50) 
    ax.set_ylabel(PlotConf["yLabel"], labelpad=50) 
    ax.set_title(PlotConf["Title"])  

    # Save and show the plot
    saveFigure(fig, PlotConf["Path"])
    plt.show()


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
    if (len(yLabels) == 1): PlotConf["yLabel"] = yLabels[0]
    else: PlotConf["yLabel"] = {}
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}
    PlotConf["Marker"] = {}
    PlotConf["Path"] = filepath
    for yLabel, yData, color, marker in zip(yLabels, yDataList, colors, markers):
        if (len(yLabels) > 1): PlotConf["yLabel"][yLabel] = yLabel        
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
    PlotConf["ColorBar"] = "jet"
    PlotConf["ColorBarLabel"] = zLabel
    PlotConf["ColorBarMin"] = min(zData)
    PlotConf["ColorBarMax"] = max(zData)      
    PlotConf["Path"] = filepath

    return PlotConf

def createPlotConfig3DMapColorBarInterpolated(filepath, title, xData, yData, zData, xLabel, yLabel, zLabel, LonMin, LonMax, LonStep, LatMin, LatMax, LatStep, ColorBar):
    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8, 15.2)
    PlotConf["Title"] = title
    PlotConf["yLabel"] = yLabel
    PlotConf["xLabel"] = xLabel        
    PlotConf["LineWidth"] = 1.5
    PlotConf["Grid"] = True            
    PlotConf["xData"] = xData
    PlotConf["yData"] = yData    
    PlotConf["zData"] = zData  
    PlotConf["ColorBar"] = ColorBar
    PlotConf["ColorBarLabel"] = zLabel
    PlotConf["ColorBarMin"] = min(zData)
    PlotConf["ColorBarMax"] = max(zData)
    PlotConf["Map"] = True    
    PlotConf["LonMin"] = LonMin
    PlotConf["LonMax"] = LonMax
    PlotConf["LonStep"] = LonStep
    PlotConf["LatMin"] = LatMin
    PlotConf["LatMax"] = LatMax
    PlotConf["LatStep"] = LatStep
    PlotConf["Path"] = filepath

    return PlotConf

def addMapToPlotConf(PlotConf, LonMin, LonMax, LonStep, LatMin, LatMax, LatStep, yLabel='', TextData=[]):
    """
    Adds to an existing configuration, the parameters for a plotting a Map.

    Parameters:
        

    Returns:
        PlotConf (dict): Configuration Data Structure for plotting 2D lines with a color bar using generateLinesPlot().
    """
    
    PlotConf["Map"] = True    
    PlotConf["LonMin"] = LonMin
    PlotConf["LonMax"] = LonMax
    PlotConf["LonStep"] = LonStep
    PlotConf["LatMin"] = LatMin
    PlotConf["LatMax"] = LatMax
    PlotConf["LatStep"] = LatStep
    PlotConf["xTicks"] = range(PlotConf["LonMin"],PlotConf["LonMax"]+1,LonStep)
    PlotConf["xLim"] = [PlotConf["LonMin"], PlotConf["LonMax"]]
    PlotConf["yTicks"] = range(PlotConf["LatMin"],PlotConf["LatMax"]+1,LatStep)
    PlotConf["yLim"] = [PlotConf["LatMin"], PlotConf["LatMax"]]
    if (len(TextData) > 0):
        PlotConf["Text"] = {}
        PlotConf["Text"][yLabel] = TextData

    return PlotConf
