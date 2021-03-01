import os

from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import json
from urllib.request import urlopen
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():     
    if request.method == "POST":
        
        start = request.form.get("start")
        end = request.form.get("end")
        
        if not start or not end:
            return render_template("index.html")    
        
        elif start==end:
            url = 'https://data.calgary.ca/resource/c2es-76ed.geojson?issueddate=' + start + 'T00:00:00.000'
            return render_template("index.html", url = url, start=start, end=end)
        
        else:
            url = "https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate%20%3E%20%27" + start + "%27%20and%20issueddate%20%3C%20%27" + end + "%27"
            return render_template("index.html", url = url, start=start, end=end)      
    
    else:  
        
        url = 'https://data.calgary.ca/resource/c2es-76ed.geojson'
        return render_template("index.html")

