#import tools needed
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#creating engine, copied over from jupyter notebook
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
#creating session, copied over from jupyter notebook
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#Flask time
app = Flask(__name__)
#creating routes
@app.route("/")
def home():
    print("Looking for all API's")
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>") 

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).order_by(Measurement.date).all()

@app.route("/api/v1.0/tobs")
    tobs = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23').all())

@app.route("/api/v1.0/stations")
    stations_list = session.query(Stations.station).all()
    lists = list(np.ravel(stations_list))
    return jsonify(lists)



if __name__ == '__main__':
    app.run(debug=True)
