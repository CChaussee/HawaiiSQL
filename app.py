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
def intro():
    print("Looking for all API's")
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>") 

