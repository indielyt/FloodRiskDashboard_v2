# RESOURCES
# https://plot.ly/python/cmocean-colorscales/ (updated for python 3 and dash app)
# Better source for generating color dictionaries  --  https://matplotlib.org/cmocean/
# Script for developing the initial colormap from cmocean color scale

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import cmocean

import numpy as np
import os

def cmocean_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = map(np.uint8, np.array(cmap(k*h)[:3])*255)
        C = list(C)
        pl_colorscale.append('rgb'+str((C[0], C[1], C[2])))

    return pl_colorscale
    # return C

# # Develop initial color map from matter colormap
balance = cmocean_to_plotly(cmocean.cm.balance, 5)
print (balance)