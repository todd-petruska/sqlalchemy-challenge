# SQLAlchemy-Challenge 

## ​**Background**:  *This code assists in producing climate analysis for a fictitious holiday vacation in Honolulu, Hawaii through Python, SQLAlchemy, Pandas, Matplotlib, and SQLAlchemy ORM queries​*. 

### ​**Folder** labeled SurfsUp contains the following files: 

* climate.ipynb 

* hawaii.sqlite

* precip_yearly.png 

* USC00519281_yearly_temps.png 
   
* Resources folder: 

** Hawaii_measurements.csv and hawaii_stations.csv  

** app.py 

## ​**Precipitation Analysis**: 

This code uses Jupyter Notebook, SQLAlchemy function to connect to the SQLite database for station and measurement classes, as well as precipitation values for a 12-month period (8/23/2016 -8/23/2017) and generates a histogram into the resources folder. The code also identifies the most recent date in the dataset.  Data revealed the highest amount of precipitation occurred in September 2016 followed by April 2017. 

## ​**Station Analysis**:

This code queries the number of weather stations in the dataset, then identifies the most active weather station by id from 8/23/2016 to 8/23/2017, and revealed that of the nine weather stations, USC00519281 is the most active weather station in Hawaii.  This code provides the lowest, highest, and average temperatures for USC00519281, and generates a histogram into the resources folder.   The most frequent temperature is 75 degrees for the quired timeframe.  



## ​**Climate App**: 

Lastly, a climate apps using a Flask API with respective routes to showcase the aforementioned queries to lowest, highest, and average temperatures for a one-year period.  This is an example of an acceptable time range 2016-10-24/2016-11-09 for /api/v1.0/temp/<start>/<end>. The app.py files is accessed using terminal or windows command line, which will generate a URL to paste into your browser of choice. 



## ​**Resources**: 

Resources and coded used for this project include, Instructor provided starter code, Office hours, Study Group, course materials, pandas.pydata.org, geeksforgeeks, SQLAlchemy documentation, and Stack Overflow.
