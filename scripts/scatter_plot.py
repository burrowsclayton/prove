""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Scatter Plot:

Creates the scatter plot
"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Getting the data table object
table_name = "Monthly Production information link"
data_table = Document.Data.Tables[table_name]

# Creating the scatter plot
scatter_plot = Document.ActivePageReference.Visuals.AddNew[ScatterPlot]()
# Linking the data table with the newly created scatter plot
scatter_plot.Data.DataTableReference = data_table
# Auto configures the scattter plot settings, needed for markings
scatter_plot.Data.AutoConfigure()
# Setting the x and y axis of the scatter plot, and setting them to use a log scale
scatter_plot.YAxis.Expression = "[GAS_RATE_MSCF_PD]"
scatter_plot.XAxis.Expression = "[NUMBER_OF_DAYS_PRODUCED]"
scatter_plot.XAxis.UseLogTransform = True
scatter_plot.YAxis.UseLogTransform = True


# Display settings of the scatter plot
scatter_plot.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)
