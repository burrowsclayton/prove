from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Getting the data table by searching all data tables and getting the name
# of the first data table in the list, the data table is the data imported from
# the spreadsheet or database
data_table_handle = Document.Data.Tables
# Tablename is the name of the first table found
tableName = [table.Name for table in data_table_handle][0]
# Selecting the data table, based on the table name found
data_table_handle = data_table_handle[ tableName ]

# Creating the scatter plot
scatter_plot_handle = Document.ActivePageReference.Visuals.AddNew[ScatterPlot]()
# Linking the data table with the newly created scatter plot
scatter_plot_handle.Data.DataTableReference = data_table_handle
# Setiing the y axis to plot the column GasRate from the excel spreadsheet
scatter_plot_handle.YAxis.Expression = "[GasRate]"
# Setiing the x axis to plot the column Number of days produced from the excel spreadsheet
scatter_plot_handle.XAxis.Expression = "[Number of days produced]"
# Setting the title of the scatter plot
scatter_plot_handle.Title = tableName
# Use Log scale for box x and y axis
scatter_plot_handle.XAxis.UseLogTransform = True
scatter_plot_handle.YAxis.UseLogTransform = True

#Change shape to circles
scatter_plot_handle.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)

print "Script Complete"
