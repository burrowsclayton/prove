from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

# Getting the data table by searching all data tables and getting the name
# of the first data table in the list, the data table is the data imported from
# the spreadsheet or database
dataTable = Document.Data.Tables
# Tablename is the name of the first table found
tableName = [table.Name for table in dataTable][0]
# Selecting the data table, based on the table name found
dataTable = dataTable[ tableName ]

# Creating the scatter plot
scatterPlot = Document.ActivePageReference.Visuals.AddNew[ScatterPlot]()
# Linking the data table with the newly created scatter plot
scatterPlot.Data.DataTableReference = dataTable
# Setiing the y axis to plot the column GasRate from the excel spreadsheet
scatterPlot.YAxis.Expression = "[GasRate]"
# Setiing the x axis to plot the column Number of days produced from the excel spreadsheet
scatterPlot.XAxis.Expression = "[Number of days produced]"
# Setting the title of the scatter plot
scatterPlot.Title = tableName
# Use Log scale for box x and y axis
scatterPlot.XAxis.UseLogTransform = True
scatterPlot.YAxis.UseLogTransform = True

#Change shape to circles
scatterPlot.ShapeAxis.DefaultShape = MarkerShape(MarkerType.Circle)

print "Script Complete"
