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
    session = Session(engine)
    last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).order_by(Measurement.date).all()
    session.close()
    rain_data = []
    for i in precipitation:
        data_dict = {}
        data_dict['date'] = precipitation[0]
        data_dict['prcp'] = precipitation[1]
        rain_data.appened(data_dict)
    return jsonify(rain_data) 

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23').all())
    session.close()
    info = []
    for i in tobs:
        tobs_dict = {}
        tobs_dict['station'] = tobs[0]
        tobs_dict['tobs'] = tobs[1]
        info.append(tobs_dict)
    return jsonify(info)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_list = session.query(Stations.station).all()
    session.close()
    lists = list(np.ravel(stations_list))
    return jsonify(lists)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    start_date = ('2016,08,23')
    start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs).\
        filter(Measurement.date >= start_date))
    session.close()
    start_tobs = []
    for i in start:
        start_dict = {}
        start_dict['Min'] = tobs[0]
        start_dict['Max'] = tobs[1]
        start_dict['Avg'] = tobs[2]
        start_tobs.append(start_dict)
    return jsonify(start_tobs)
@app.route("/api/v1.0/<start>/<end>")
def temp_end(end):
    session = Session(engine)
    end_date = ('2017,08,23')
    end = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs).\
        filter(Measurement.date <= end_date))
    session.close()
    end_tobs = []
    for i in start:
        end_dict = {}
        end_dict['Min'] = tobs[0]
        end_dict['Max'] = tobs[1]
        end_dict['Avg'] = tobs[2]
        end_tobs.append(start_dict)
    return jsonify(end_tobs)
if __name__ == "__main__":
    app.run(debug=True)