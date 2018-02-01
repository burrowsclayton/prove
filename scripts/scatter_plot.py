""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Scatter Plot:

Creates the scatter plot
"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Get a handle on the data table (object that contains all data)
data_table = Document.Data.Tables
data_table_name = [table.Name for table in data_table][0]
data_table = data_table[ data_table_name ]

# Creating the scatter plot
scatter_plot = Document.ActivePageReference.Visuals.AddNew[ScatterPlot]()
# Linking the data table with the newly created scatter plot
scatter_plot.Data.DataTableReference = data_table

# Setting the x and y axis of the scatter plot, and setting them to use a log scale
scatter_plot.YAxis.Expression = "[GAS_RATE_MSCF_PD]"
scatter_plot.XAxis.Expression = "[NUMBER_OF_DAYS_PRODUCED]"
scatter_plot.XAxis.UseLogTransform = True
scatter_plot.YAxis.UseLogTransform = True

# Display settings of the scatter plot
scatter_plot.Title = data_table_name
scatter_plot.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)

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


print "Script Complete"
