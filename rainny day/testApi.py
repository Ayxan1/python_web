import os
from flask import Flask, url_for, render_template, request, session
import requests
import json

app = Flask(__name__)
@app.route('/')
def main1():
    lat=42.37
    log=71.11
    res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
    weather=json.dumps(res["currently"])
    return render_template("testApiContent.html",weather=weather)



___________________________________________________



___________________________________________________
