# ProVe Automated Analysis
Automated graphing of well data for ProVe analysis. It contains a default Spotfire application that connects to the database to extract montly well data. It also contains all necessary filtering columns for proper analysis, as well as a calculated column for the number of producing days. The default Spotfire application also contains a Text Area where the filtering options are displayed and action items that run the necessary scripts to plot the data in the required manner for ProVe analysis.

## Prequisites
- Spotfire v7.6
- Access to data source: <br>
&nbsp;&nbsp;&nbsp;&nbsp;
`Library/Subsurface-Analytics/Development/Coopprod/Information links/Monthly Production information link`

## Scripts
The scripts are written in [IronPython](http://ironpython.net/). Refer to the [Spotfire v7.6 API](https://docs.tibco.com/pub/doc_remote/spotfire/7.6.0/doc/api/) for details about function calls within the scripts. 

## Authors
- Joseph Tripodi

## Acknowledgements
- Spotfire IronPython Community