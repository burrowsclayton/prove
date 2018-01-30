""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76
""""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Get a handle on the data table (object that contains all data)
data_table_handle = Document.Data.Tables
data_table_name = [table.Name for table in data_table_handle][0]
data_table_handle = data_table_handle[ data_table_name ]

# Creating the scatter plot
scatter_plot_handle = Document.ActivePageReference.Visuals.AddNew[ScatterPlot]()
# Linking the data table with the newly created scatter plot
scatter_plot_handle.Data.DataTableReference = data_table_handle

# Setting the x and y axis of the scatter plot, and setting them to use a log scale
scatter_plot_handle.YAxis.Expression = "[GAS_RATE_MSCF_PD]"
scatter_plot_handle.XAxis.Expression = "[NUMBER_OF_DAYS_PRODUCED]"
scatter_plot_handle.XAxis.UseLogTransform = True
scatter_plot_handle.YAxis.UseLogTransform = True

# Display settings of the scatter plot
scatter_plot_handle.Title = data_table_name
scatter_plot_handle.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)

print "Script Complete"
