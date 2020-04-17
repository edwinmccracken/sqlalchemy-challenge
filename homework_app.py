from flask import Flask, jsonify
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def index():
    return (
        f"<h2>Available Routes:<h2><br/>"
        f"<h3>/api/v1.0/precipitation<h3><br/>"
        f"<h3>/api/v1.0/stations<h3><br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of percipitation data"""
    # Query all precipitation data
    result = session.query(measurement.date, measurement.prcp).filter(measurement.date > ('2016-08-23')).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in result:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results1 = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results1))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature of most popular station for a year ago
    histo = list(np.ravel(results))

    session.close()

    # Convert list of tuples into normal list
    all_temperatures = list(np.ravel(histo))

    return jsonify(all_temperatures)

if __name__ == "__main__":
    app.run(debug=True)