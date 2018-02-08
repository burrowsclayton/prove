"""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Half Slope:

Plots a line with a half slope, based on the user selected points on the scatter plot
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

# Getting the data table object
table_name = "Monthly Production information link"
data_table = Document.Data.Tables[table_name]

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
  # Creating the cursors to use in our column selections
  # Refer to the DataValueCursor in the Spotfire API
  columns = data_table.Columns
  gas_rate_cursor = DataValueCursor.Create(columns["GAS_RATE_MSCF_PD"])
  days_cursor = DataValueCursor.Create(columns["NUMBER_OF_DAYS_PRODUCED"])
  
  # Getting on the user marked data
  markings = Document.ActiveMarkingSelectionReference.GetSelection(data_table)
  points = []
  gas_rate, days = 0, 1
  # Extracting the data into separate lists
  for row in data_table.GetRows(markings.AsIndexSet(), gas_rate_cursor, days_cursor):
    points.append((gas_rate_cursor.CurrentValue, days_cursor.CurrentValue))

  if points == []:
    MessageBox.Show("No markings have been selected.", "No markings.")
  else:
    # Getting the median point based on the days value which is the 
    # second value in the tuple then we get the len/2 point which is
    # the median. 
    median = sorted(points, key = lambda points: points[days])[len(points)/2]

    # Wokring out the equation of the line, only unknown is the y intercept (a)
    # log(y) = log(x)*b + log(a)
    intercept = math.exp(math.log(median[gas_rate])+0.5*math.log(median[days]))
    half_slope_expression = "[x]*-.5+log10(" + str(intercept) + ")"
    half_slope_curve = scatter_plot.FittingModels.AddCurve(half_slope_expression)

    # Disabling any previous half slope lines
    for fm in scatter_plot.FittingModels:
      if str(fm.TypeId) == "TypeIdentifier:Spotfire.ReferenceCurveFittingModel":
        if fm.Curve.CustomDisplayName == "HALF SLOPE":
          fm.Enabled = False

    # Line style
    half_slope_curve.Curve.CustomDisplayName = "HALF SLOPE"
    half_slope_curve.Curve.LineStyle = LineStyle().Dash
    red = Color.FromArgb(255, 255, 0, 0)
    one_slope_curve.Curve.Color = red
    one_slope_curve.Curve.Width = 3  
  


