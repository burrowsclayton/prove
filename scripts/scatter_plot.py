""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Scatter Plot:

Creates the scatter plot
"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Get the data table (object that contains all data)
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
scatter_plot.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)

print "Script Complete"
