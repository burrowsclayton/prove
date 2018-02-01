""""
Author: Joseph Tripodi
Contact: au.joseph.tripodi@gmail.com
For more information see: https://github.com/joseph-tripodi/prove/wiki/04.-Spotfire-API#spotfire-api-v76

Driver:

This script runs the entire project. 

"""

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Scripting import ScriptDefinition
import clr

scatter_plot = clr.Reference[ScriptDefinition]()
simplified_fetkovich = clr.Reference[ScriptDefinition]()
Document.ScriptManager.TryGetScript("scatter_plot", scatter_plot)
Document.ScriptManager.TryGetScript("simplified_fetkovich", simplified_fetkovich)

Document.ScriptManager.ExecuteScript(scatter_plot.ScriptCode, {})


