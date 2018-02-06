""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Simplified Fetkovich:

Plots the simplified fetkovich curve

"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
import math
import clr

# Get the data table (object that contains all data)
data_table = Document.Data.Tables
data_table_name = [table.Name for table in data_table][0]
data_table = data_table[ data_table_name ]

# Getting a reference to the scatter plot
scatter_plot = None
for visual in Document.ActivePageReference.Visuals:
  if "ScatterPlot" in str(visual.TypeId):
    scatter_plot = visual.As[ScatterPlot]()

# Selecting the filtered rows for line calculations
# Creating the cursors to use in our column selections
columns = data_table.Columns
date_cursor = DataValueCursor.Create(columns["END_OF_MONTH_DATE"])
slope_cursor = DataValueCursor.Create(columns["SLOPE"])
gas_rate_cursor = DataValueCursor.Create(columns["GAS_RATE_MSCF_PD"])
days_cursor = DataValueCursor.Create(columns["NUMBER_OF_DAYS_PRODUCED"])

# Creating a row selection that allows us to only get the rows that match
# the current filtering options
filtering = Document.ActiveFilteringSelectionReference
# The selection needs to be converted to an Enumerable type to be used in GetRows
row_selection = filtering.GetSelection(data_table).AsIndexSet()

slope_hash, gas_rate_hash, day_hash = {}, {}, {}

for each in data_table.GetRows(row_selection, date_cursor, slope_cursor, gas_rate_cursor, days_cursor):
  slope_hash[date_cursor.CurrentValue] = slope_cursor.CurrentValue
  gas_rate_hash[date_cursor.CurrentValue] = gas_rate_cursor.CurrentValue
  day_hash[date_cursor.CurrentValue] = days_cursor.CurrentValue

quarter_slope, half_slope, one_slope = None, None, None
state = "start"
previous_slope = 0
for key in sorted(list(slope_hash.iterkeys())[7:] ):
  if state is "start":
    state = "quarter"
  elif state is "quarter":
    if abs(slope_hash[key]-previous_slope) >= 0.25:
      quarter_slope = key
      state = "half"
  elif state is "half":
    if abs(slope_hash[key]-previous_slope) >= 0.5:
      half_slope = key
      state = "one"
  elif state is "one":
    if abs(slope_hash[key]-previous_slope) >= 1:
      one_slope = key
      state = "fin"

  previous_slope = slope_hash[key]

# Line equation: log(y) = k*log(x) + log(a)
# Working out the y intercept
quarter_slope_a = math.exp(math.log(gas_rate_hash[quarter_slope])+0.25*math.log(day_hash[quarter_slope]))
half_slope_a = math.exp(math.log(gas_rate_hash[half_slope])+0.5*math.log(day_hash[half_slope]))
one_slope_a = math.exp(math.log(gas_rate_hash[one_slope])+1*math.log(day_hash[one_slope]))

# Creating the line expressions
quater_slope_expression = "[x]*-.25+log10(" + str(quarter_slope_a) + ")"
half_slope_expression = "[x]*-.5+log10(" + str(half_slope_a) + ")"
one_slope_expression = "[x]*-1+log10(" + str(one_slope_a) + ")"

# Plotting the lines onto the ScatterPlot
quarter_slope_curve = scatter_plot.FittingModels.AddCurve(quater_slope_expression)
half_slope_curve = scatter_plot.FittingModels.AddCurve(half_slope_expression)
one_slope_curve = scatter_plot.FittingModels.AddCurve(one_slope_expression)

quarter_slope_curve.Curve.CustomDisplayName = "QUARTER SLOPE"
half_slope_curve.Curve.CustomDisplayName = "HALF SLOPE"
one_slope_curve.Curve.CustomDisplayName = "ONE SLOPE"
