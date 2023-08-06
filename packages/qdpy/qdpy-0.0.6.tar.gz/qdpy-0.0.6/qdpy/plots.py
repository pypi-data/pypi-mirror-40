#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""A collection of functions to plot containers using Matplotlib."""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from functools import reduce
from operator import mul

from qdpy.utils import is_iterable


########### Plots ########### {{{1




# TODO refactor name, etc
def plotGridSubplots(data, outputFilename, cmap, featuresBounds=((0., 1.), (0., 1.), (0., 1.), (0., 1.)), fitnessBounds=(0., 1.), drawCbar = True, xlabel = "", ylabel = "", cBarLabel = "", nbBins = None, nbTicks = None, binSizeInInches = 0.30):
    """TODO"""
    # Verify data dimension is supported by this funtion
    if len(data.shape) > 4:
        raise ValueError("plotGridSubplots only supports up to 4 dimensions.")
    elif len(data.shape) <= 2:
        plotGrid(data, outputFilename, cmap, featuresBounds=featuresBounds, fitnessBounds=fitnessBounds, drawCbar=drawCbar, xlabel=xlabel, ylabel=ylabel, cBarLabel=cBarLabel, nbBins=nbBins, nbTicks=nbTicks)
        return

    # Verify dimension is even
    if len(data.shape) % 2 == 1:
        data = data.reshape((data.shape[0], 1) + data.shape[1:])
        featuresBounds = (featuresBounds[0], (0., 0.)) + tuple(featuresBounds[1:]) 
        if nbBins != None:
            nbBins = (nbBins[0], 1) + nbBins[1:]
    if not nbBins:
        nbBins = data.shape

    #data[0,:,:,:] = np.linspace(0., 1., nbBins[1] * nbBins[2] * nbBins[3]).reshape((nbBins[1], nbBins[2], nbBins[3]))

    # Compute figure infos from nbBins
    horizNbBins = nbBins[::2]
    horizNbBinsProd = reduce(mul, horizNbBins, 1)
    vertNbBins = nbBins[1::2]
    vertNbBinsProd = reduce(mul, vertNbBins, 1)
    totProp = horizNbBinsProd + vertNbBinsProd
    upperlevelTot = nbBins[0] + nbBins[1]

    # Determine figure size from nbBins infos
    #figsize = [2.1 + 10. * horizNbBinsProd / upperlevelTot, 1. + 10. * vertNbBinsProd / upperlevelTot]
    #if figsize[1] < 2:
    #    figsize[1] = 2.
    figsize = [2.1 + horizNbBinsProd * binSizeInInches, 1. + vertNbBinsProd * binSizeInInches]

    # Create figure
    fig, axes = plt.subplots(nrows=nbBins[1], ncols=nbBins[0], figsize=figsize)

    # Create subplots
    for x in range(nbBins[0]):
        for y in range(nbBins[1]):
            ax = plt.subplot(nbBins[1], nbBins[0], (nbBins[1] - y - 1) * nbBins[0] + x + 1)
            #ax = axes[x,y]
            cax = drawGridInAx(data[x, y, 0:nbBins[2], 0:nbBins[3]], ax, cmap=cmap, featuresBounds=featuresBounds[-2:], fitnessBounds=fitnessBounds[-2:], aspect="equal", xlabel=xlabel, ylabel=ylabel, nbBins=(nbBins[2], nbBins[3]), nbTicks=nbTicks)

    plt.tight_layout()
    if drawCbar:
        fig.subplots_adjust(right=0.85, wspace=0.40)
        #cbarAx = fig.add_axes([0.90, 0.15, 0.01, 0.7])
        if figsize[0] < 4.:
            cbarAx = fig.add_axes([0.75, 0.15, 0.02, 0.7])
        elif figsize[0] < 6.:
            cbarAx = fig.add_axes([0.80, 0.15, 0.02, 0.7])
        elif figsize[0] < 10.:
            cbarAx = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        else:
            cbarAx = fig.add_axes([0.90, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(cax, cax=cbarAx, format="%.2f")
        cbar.ax.tick_params(labelsize=20)
        cbar.ax.set_ylabel(cBarLabel, fontsize=22)

    fig.savefig(outputFilename)





# TODO refactor name, etc
def drawGridInAx(data, ax, cmap, featuresBounds, fitnessBounds, aspect="equal", xlabel = "", ylabel = "", nbBins=None, nbTicks = 5):
    # Draw grid
    cax = ax.imshow(data.T, interpolation="none", cmap=cmap, vmin=fitnessBounds[0], vmax=fitnessBounds[1], aspect=aspect)
    ax.invert_yaxis()

    # Define the number of ticks on x,y axis
    if is_iterable(nbTicks):
        if len(nbTicks) != 2:
            raise ValueError("nbTicks can be None, an Integer or a Sequence of size 2.")
        nbTicksX, nbTicksY = nbTicks
    elif nbTicks == None:
        nbTicksX = round(pow(nbBins[0], 1./2.))
        nbTicksX = nbTicksX if nbTicksX % 2 == 0 else nbTicksX + 1
        nbTicksY = round(pow(nbBins[1], 1./2.))
        nbTicksY = nbTicksY if nbTicksY % 2 == 0 else nbTicksY + 1
    else:
        if nbBins[0] > nbBins[1]:
            nbTicksX = nbTicks
            nbTicksY = int(nbTicksX * nbBins[1] / nbBins[0])
        elif nbBins[1] > nbBins[0]:
            nbTicksY = nbTicks
            nbTicksX = int(nbTicksY * nbBins[0] / nbBins[1])
        else:
            nbTicksX = nbTicksY = nbTicks
        # Verify than the number of ticks is valid
        if nbTicksX > nbBins[0] or nbTicksX < 1:
            nbTicksX = min(nbBins[0], nbTicks)
        if nbTicksY > nbBins[1] or nbTicksY < 1:
            nbTicksY = min(nbBins[1], nbTicks)

    # Set ticks
    ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
    ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
    if len(featuresBounds) > 1:
        xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / nbTicksX))
        yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
        deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
        ax.set_xticklabels([round(float(x / float(data.shape[0]) * deltaFeature0 + featuresBounds[0][0]), 2) for x in xticks], fontsize=18)
        deltaFeature1 = featuresBounds[1][1] - featuresBounds[1][0]
        ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature1 + featuresBounds[1][0]), 2) for y in yticks], fontsize=18)
        plt.xticks(xticks, rotation='vertical')
    else:
        yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
        deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
        ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature0 + featuresBounds[0][0]), 2) for y in yticks], fontsize=18)
        plt.xticks([])
        ax.set_xticklabels([])
    if nbBins[1] == 1:
        yticks = []
    plt.yticks(yticks)

    # Draw grid
    ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    ax.set_xticks(np.arange(-.5, data.shape[0], 1), minor=True)
    ax.set_yticks(np.arange(-.5, data.shape[1], 1), minor=True)
    ax.grid(which='minor', color=(0.8,0.8,0.8,0.5), linestyle='-', linewidth=0.1)

    ax.set_xlabel(xlabel, fontsize=25)
    ax.set_ylabel(ylabel, fontsize=25)
    ax.autoscale_view()
    return cax



# TODO refactor name, etc
def plotGrid(data, outputFilename, cmap, featuresBounds=[(0., 1.), (0., 1.)], fitnessBounds=(0., 1.), drawCbar = True, xlabel = "", ylabel = "", cBarLabel = "", nbBins = None, nbTicks = None):
    if len(data.shape) == 1:
        data = data.reshape((data.shape[0], 1))
        featuresBounds = tuple(featuresBounds) + ((0., 0.),)
        if nbBins != None:
            nbBins = nbBins + (1,)
    elif len(data.shape) > 2:
        raise ValueError("plotGrid only supports 1 ou 2-dimensional data.")
    if not nbBins:
        nbBins = data.shape

    figsize = [2.1 + 10. * nbBins[0] / (nbBins[0] + nbBins[1]), 1. + 10. * nbBins[1] / (nbBins[0] + nbBins[1])]
    aspect = "equal"
    if figsize[1] < 2:
        figsize[1] = 2.
        aspect = "auto"

    fig, ax = plt.subplots(figsize=figsize)
    cax = drawGridInAx(data, ax, cmap=cmap, featuresBounds=featuresBounds, fitnessBounds=fitnessBounds, aspect=aspect, xlabel=xlabel, ylabel=ylabel, nbBins=nbBins, nbTicks=nbTicks)

    if drawCbar:
        divider = make_axes_locatable(ax)
        #cax2 = divider.append_axes("right", size="5%", pad=0.15)
        cax2 = divider.append_axes("right", size=0.5, pad=0.15)
        cbar = fig.colorbar(cax, cax=cax2, format="%.2f")
        cbar.ax.tick_params(labelsize=20)
        cbar.ax.set_ylabel(cBarLabel, fontsize=22)

    plt.tight_layout()
    fig.savefig(outputFilename)


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
