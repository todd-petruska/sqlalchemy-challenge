# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect = True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
	"""List all of the availabe api routes."""
	return (
		f"Hawaii Vacation Data Routes:<br/>"
		f"--Precipitation 2016-08-23 to 2017=08-23 Daily Totals: /api/v1.0/precipitation<br/>"
		f"--Most Active Weathaer Stations: /api/v1.0/stations<br/>"
		f"--Station USC00519281 Daily Temperature Observations: /api/v1.0/tobs<br/>"
		f"--Input Dates for Minimum, Average, and Maximum Temp for Date Range: /api/v1.0/temp/yyyy-mm-dd/yyyy-mm-dd<br/>"
		f"----Please input date in this format, ex. 2016-10-26/2016-11-09"
	)
	
@app.route("/api/v1.0/precipitation")
def precipitation():
	# Create our session link from Python to the DB
	session = Session(engine)

	"""Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value"""
	back_date = "2016-08-23"

	""#select = [measurement.date, measurement.prcp]"""
	select = [measurement.prcp, measurement.date]
	#precip_year = session.query(*select).\
	precip_year = session.query(measurement.prcp, measurement.date).\
    	filter(measurement.date >= back_date).\
    	order_by(measurement.date).all()

	session.close()		

	# Create a dictionary from the row data and append to a list using date as ky and prcp as value
	precipitation_query = []
	for prcp, date in precip_year:
		precip_dict = {}
		precip_dict["Precipitation"] = prcp
		precip_dict["Date"] = date
		precipitation_query.append(precip_dict)

	# Return the JSON representation of your dictionary
	return jsonify(precipitation_query)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
	# Create our session (link) from Python to the DB
	session = Session(engine)

	# Query a list of weather stations from the dataset.
	station_totals = session.query(measurement.station).\
		group_by(measurement.station).all()
	session.close()

	# Convert list of tuples into normal list
	station_list = list(np.ravel(station_totals))
	# Return the JSON representation of your dictionary
	return jsonify(station_list)

# Return a JSON list of temperatures dataset.
@app.route("/api/v1.0/tobs")
def tobs():
	# Create our session link from Python to the DB
	session = Session(engine)

	# Query the dates and temp. observations of the most-active stations for prev. year of data.
	back_date = "2016-08-23"
	
	station_temps_stats = session.query(measurement.date, measurement.tobs).\
    	filter(measurement.date >= back_date, measurement.station == 'USC00519281').\
    	group_by(measurement.date).\
    	order_by(measurement.date)

	# Close the session
	session.close()

    # Create a dictionary from the row data and append to a list for date and tobs
	list_temp_dates= []
	for date, tobs in station_temps_stats:
		year_station_dict = {}
		#year_station_dict["Station"] = station
		year_station_dict["Date"] = date
		year_station_dict["Temperature"] = tobs
		list_temp_dates.append(year_station_dict)
		
	return jsonify(list_temp_dates)
# Create a date start/end to query min, max, and average temperatures.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    # Select statement
    sel = [
        func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs),
    ]
    if not end:
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        results = session.query(*sel).filter(measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # Calculate TMIN, TAVG, TMAX with start and stop and strip date time
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    results = (
        session.query(*sel)
        .filter(measurement.date >= start)
        .filter(measurement.date <= end)
        .all()
    )
    # Close the session
    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)
