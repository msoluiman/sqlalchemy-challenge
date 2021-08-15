import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
        """List all available api routes."""
        return (
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
        )


@app.route("/api/v1.0/precipitation")

def precipitation_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation date from a year ago<"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    precipitation_data = list(np.ravel(results))

    return jsonify(precipitation_data)


# Design a query to calculate the total number stations in the dataset
# Design a query to find the most active stations (i.e. what stations have the most rows?)

@app.route("/api/v1.0/station")
def station_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names <"""
    # Query all passengers
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(results))

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs_data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature from one year ago<"""
    # Query all station
    results = session.query(measurement.station,func.count(measurement.tobs)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first() 

    session.close()

    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def temperatures_data(start):
    """ When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""

    results = session.query(measurement.station,func.count(measurement.tobs)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first() 
    
    session.close()

    # Convert list of tuples into normal list
    temperatures_data = list(np.ravel(results))

    return jsonify(temperatures_data)


@app.route("/api/v1.0/<start>/<end>")
def temperatures_data_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive"""
    results = results = session.query(measurement.station,func.count(measurement.tobs)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first() 
                
    session.close()

    # Convert list of tuples into normal list
    temperatures_data_end = list(np.ravel(results))

    return jsonify(temperatures_data_end)


if __name__ == '__main__':
    app.run(debug=True)