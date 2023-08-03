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
Base.prepare(autoload_with=engine)

# Save reference to the table
Hawaii_measurements = Base.classes.measurement
Hawaii_stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperatures<br/>"
        f"/api/v1.0/temperatures/start<br/>"
        f"/api/v1.0/temperatures/start/end<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperatures names"""
    # Query all temperatures
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)  
    sel = [Hawaii_measurements.date, 
        Hawaii_measurements.prcp]
    prcp_scores = session.query(*sel).\
        filter(Hawaii_measurements.date >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    print(prcp_scores)
    data = []
    for i in prcp_scores: 
        data.append({
            i[0]:i[1]
        })
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query all stations
    all_stations = session\
    .query(Hawaii_measurements.station).distinct(Hawaii_measurements.station).all()

    session.close()

    # Convert list of tuples into normal list   
    data = list(np.ravel(all_stations))
    return jsonify(data)



@app.route("/api/v1.0/temperatures")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all temperatures
    query_temp = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    ma_station = "USC00519281" 
    temp_histo = session.query(Hawaii_measurements.tobs).\
    filter(Hawaii_measurements.station == ma_station).\
    filter(Hawaii_measurements.date >= query_temp).all()

    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(temp_histo))

    return jsonify(data)



@app.route("/api/v1.0/temperatures/<startdate>")
def tempstart(startdate):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(startdate,"%m-%d-%Y")
    """Return a list of all temperatures names"""
    # Query all temperatures
    ma_station = "USC00519281" 
    sel2 = [Hawaii_measurements.station, 
       func.min(Hawaii_measurements.tobs), 
       func.avg(Hawaii_measurements.tobs), 
       func.max(Hawaii_measurements.tobs)]

    mas_temp = session.query(*sel2).\
    filter(Hawaii_measurements.station == ma_station).\
    filter(Hawaii_measurements.date >= start).all()
   

    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(mas_temp))
    return jsonify(data)





@app.route("/api/v1.0/temperatures1/<startdate>/<enddate>")
def tempsend(startdate, enddate):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(startdate,"%m-%d-%Y")
    end = dt.datetime.strptime(enddate,"%m-%d-%Y")
    """Return a list of all temperatures names"""
    # Query all temperatures
    ma_station = "USC00519281" 
    sel2 = [Hawaii_measurements.station, 
       func.min(Hawaii_measurements.tobs), 
       func.avg(Hawaii_measurements.tobs), 
       func.max(Hawaii_measurements.tobs)]

    mas_temp = session.query(*sel2).\
    filter(Hawaii_measurements.station == ma_station).\
    filter(Hawaii_measurements.date >= start).\
    filter(Hawaii_measurements.date <= end).all()
   

    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(mas_temp))
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True)
#"72.196