
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

def createFigure(PlotConf):
    try:
        if "Polar" in PlotConf and PlotConf["Polar"] == True:
            fig, ax = plt.subplots(figsize=PlotConf["FigSize"],subplot_kw=dict(polar=True))    
            ax.set_aspect('equal')
        else:
            fig, ax = plt.subplots(1, 1, figsize=PlotConf["FigSize"])
    
    except:
        fig, ax = plt.subplots(1, 1)

    return fig, ax

def saveFigure(fig, Path):
    Dir = os.path.dirname(Path)
    try:
        os.makedirs(Dir)
    except: pass
    fig.savefig(Path, dpi=150., bbox_inches='tight')
    plt.close('all')

def prepareAxis(PlotConf, ax):
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    
    for key in PlotConf:
        if key == "Title":
            ax.set_title(PlotConf["Title"], fontsize=12)     

        if key == "Polar" and PlotConf[key] == True:
            # Define the radial ticks and limits
            ax.set_rticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
            ax.set_rlim(0, 90)            

            ax.set_yticklabels([90, 80, 70, 60, 50, 40, 30, 20, 10, 0], fontsize=10, fontweight='bold')
            
            # Define the ticks at 0, 90, 180, 270 degrees
            xticks = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
            ax.set_xticks(xticks) 
            ax.set_xticklabels(['N', 'E', 'S', 'W'], fontsize=10, fontweight='bold')
            
            ax.set_theta_zero_location('N')
            ax.set_theta_direction('clockwise')
        
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

def prepareColorPolarBar(PlotConf, ax, Values):
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

    # Create a separate axis for the color bar outside the polar plot area
    color_ax = plt.gcf().add_axes([0.95, 0.1, 0.05, 0.8])  # Adjust the position and size as needed
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
        if key == "ColorBar" and "Polar" not in PlotConf:
            normalize, cmap = prepareColorBar(PlotConf, ax, PlotConf["zData"])
        if key == "ColorBar" and "Polar"  in PlotConf:
            normalize, cmap = prepareColorPolarBar(PlotConf, ax, PlotConf["zData"])
        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)
            

    for Label in PlotConf["yData"].keys():
        if "ColorBar" in PlotConf:
            ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label], 
            marker = PlotConf["Marker"],
            linewidth = LineWidth,
            c = cmap(normalize(np.array(PlotConf["zData"][Label]))))

        else:
            ax.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
            PlotConf["Marker"],
            linewidth = LineWidth,
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

                    ax2.set_yticks(PlotConf["Twin_yTicks"])
                    ax2.set_ylim(PlotConf["Twin_yLim"])
        
        # Comprobar PlotConf["label"]

    if "ShowLegend" in PlotConf:
         # Create legends for each label
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = list(set(labels))
        legend_handles = [handles[labels.index(label)] for label in unique_labels]

        ax.legend(legend_handles, unique_labels, loc='upper right', fontsize='medium')
    
    saveFigure(fig, PlotConf["Path"])

def generatePlot(PlotConf):
    if(PlotConf["Type"] == "Lines"):
        generateLinesPlot(PlotConf)