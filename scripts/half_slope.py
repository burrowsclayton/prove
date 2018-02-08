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
    scatter_plot = visual.As[ScatterPlot]()

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
  gas_rate, days = [], []

  # Extracting the data into separate lists
  for row in data_table.GetRows(markings.AsIndexSet(), gas_rate_cursor, days_cursor):
    gas_rate.append(gas_rate_cursor.CurrentValue)
    days.append(days_cursor.CurrentValue)

  # Getting the median value from number of days produced
  # Using that index to get the gas rate value
  days_median = sorted(days)[len(days)/2]
  index_of_median = days.index(days_median)
  gas_rate_median = gas_rate[index_of_median]

  # Wokring out the equation of the line, only unknown is the y intercept (a)
  # log(y) = log(x)*b + log(a)
  intercept = math.exp(math.log(gas_rate_median)+0.5*math.log(days_median))
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
  orange = Color.FromArgb(255, 255, 174, 25)
  half_slope_curve.Curve.Color = orange
  


