# Import the dependencies.
from flask import Flask,jsonify

import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Test
print("Test, file running")
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)



#################################################
# Database Setup
#################################################


engine = engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

@app.route("/")
def welcome():
    return (
        f"Welcome to the climate and precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start/end<br/>"
        f"/api/v1.0/start"
    )

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
session = Session(engine)

prcpdata = pd.read_sql("SELECT date, sum(prcp) AS prcp FROM measurement WHERE date >= '2016-08-23' AND prcp IS NOT NULL GROUP BY date", conn)
prcpdata=prcpdata.sort_values(by=["date"])

hawaii_prcp_dict=prcpdata.to_dict()

hawaii_station_list = pd.read_sql("SELECT station FROM station", conn)
station_dict=hawaii_station_list.to_dict()

#print(hawaii_prcp_dict)

hawaii_prcp_dict_cleaned = {hawaii_prcp_dict['date'][i]: hawaii_prcp_dict['prcp'][i] for i in range(len(hawaii_prcp_dict['date']))}


Active_Station= pd.read_sql("SELECT date, tobs AS temperature FROM measurement WHERE date >= '2016-08-23' AND station ='USC00519281' ", conn)
Active_Station_dict=Active_Station.to_dict()
Active_Station_dict_cleaned={Active_Station_dict['date'][i]: Active_Station_dict['temperature'][i] for i in range(len(Active_Station_dict['date']))}


#################################################
# Flask Setup
#################################################

@app.route("/api/v1.0/stations")
def stations():
    """Return the station data as json"""

    return jsonify(station_dict)
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    return jsonify(hawaii_prcp_dict_cleaned)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data as json"""

    return jsonify(Active_Station_dict_cleaned)

@app.route("/api/v1.0/<start>")
def summary(start):
    """Return the summary data as json"""
    Summary_Station =pd.read_sql("SELECT MAX(tobs) AS max_temp,MIN(tobs) AS min_temp,AVG(tobs) AS average_temp FROM measurement WHERE date >='" + start + "' GROUP BY date ORDER BY date", conn)

    Summary_Station_dict =Summary_Station.to_dict()
    return jsonify(Summary_Station_dict)



@app.route("/api/v1.0/<start>/<end>")
def summary_two(start,end):
    """Return the summary data as json"""
    Summary_Station =pd.read_sql("SELECT MAX(tobs) AS max_temp,MIN(tobs) AS min_temp,AVG(tobs) AS average_temp FROM measurement WHERE date >='" + start + "' AND '" + end + "'GROUP BY date ORDER BY date", conn)
    Summary_Station_dict =Summary_Station.to_dict()

    return jsonify(Summary_Station_dict)


if __name__ == "__main__":
    app.run(debug=True)




#################################################
# Flask Routes
#################################################
