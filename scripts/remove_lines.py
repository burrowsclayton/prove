"""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Remove lines:

Removs the lines present on the scatter plot

"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
from System import Random, Double
from System.Drawing import Color
import math
import sys
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox

# Getting a reference to the scatter plot
scatter_plot = None
for visual in Document.ActivePageReference.Visuals:
  if "ScatterPlot" in str(visual.TypeId):
    temp = visual.As[ScatterPlot]()
    # Select the scatter plot that has gas rate vs number of days produced
    # Just incase the user has created more than one scatter plot
    if (temp.XAxis.Expression == "[NUMBER_OF_DAYS_PRODUCED]" and
          temp.YAxis.Expression == "[GAS_RATE_MSCF_PD]"):
       scatter_plot = temp

if scatter_plot == None:
  # If no scatter plot has been created then we will not attempt k-means
  MessageBox.Show("No scatter plot has been detected.\nPlease press ProVe Analysis after selecting a well.\nCheers.", "No Scatter Plot")
else:
  # Removing all lines on scatter plot
  scatter_plot.FittingModels.Clear()
