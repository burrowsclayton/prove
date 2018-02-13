"""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Quarter Slope:

Plots a line with a quarter slope, based on the user selected points on the scatter plot
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

# There are multiple scatter plots so we must first extract the data to determine which 
# scatter plot we want. This is because the marked data should only contain the name
# of a well for that specific scatter plot
markings = Document.ActiveMarkingSelectionReference.GetSelection(data_table)
columns = data_table.Columns
name_cursor = DataValueCursor.Create(columns["WELL_NAME"])
well_name = ""
# Extracting the data into separate lists
for row in data_table.GetRows(markings.AsIndexSet(), name_cursor):
  well_name = name_cursor.CurrentValue
  break

# Getting a reference to the scatter plot
scatter_plot = None
for visual in Document.ActivePageReference.Visuals:
  if "ScatterPlot" in str(visual.TypeId):
    temp = visual.As[ScatterPlot]()
    # Select the scatter plot that has gas rate vs number of days produced
    # Just incase the user has created more than one scatter plot
    
    #Extract the name from the where clause expression  
    name_begins = temp.Data.WhereClauseExpression.find('^') + 1
    name_ends = temp.Data.WhereClauseExpression.find('$')  
    temp_well_name = temp.Data.WhereClauseExpression[name_begins:name_ends]  
    if well_name == temp_well_name:  
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
    intercept = math.exp(math.log(median[gas_rate])+0.25*math.log(median[days]))
    quarter_slope_expression = "[x]*-.25+log10(" + str(intercept) + ")"
    quarter_slope_curve = scatter_plot.FittingModels.AddCurve(quarter_slope_expression)

    # Disabling any previous quarter slope lines
    for fm in scatter_plot.FittingModels:
      if str(fm.TypeId) == "TypeIdentifier:Spotfire.ReferenceCurveFittingModel":
        if fm.Curve.CustomDisplayName == "QUARTER SLOPE":
          fm.Enabled = False

    # Line style
    quarter_slope_curve.Curve.CustomDisplayName = "QUARTER SLOPE"
    quarter_slope_curve.Curve.LineStyle = LineStyle().Dot
    red = Color.FromArgb(255, 255, 0, 0)
    quarter_slope_curve.Curve.Color = red
    quarter_slope_curve.Curve.Width = 3  
