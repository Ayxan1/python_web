import os
from flask import Flask, url_for, render_template, request, session, jsonify, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import time
from decimal import Decimal
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)
app.secret_key=os.urandom(24)




@app.route("/ajax")
def ajax():
    return render_template("ajax.html")

@app.route("/ajaxResult", methods=["post"])
def ajaxResult():
    lat0=request.form.get("lat")
    log0=request.form.get("long")
    lat=float(0 if lat0 is None else lat0)
    log=float(0 if log0 is None else log0 )
    res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
    return jsonify({"success": True, "weather": res["currently"]})



@app.route("/")
def mainPage():
    message=None
    return render_template("index.html")

@app.route("/login", methods=["post"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    databaseUser=db.execute("select * from users where email=:email",{"email":email}).fetchone()
    if databaseUser!=None:
        if check_password_hash(databaseUser.password,password):
            session["user"]=databaseUser.first_name
            return redirect(url_for('search'))

    return redirect(url_for('mainPage'))


@app.route("/signUp", methods=["post"])
def signUp():
    hashed_password=generate_password_hash(request.form.get("password"), method='sha256')
    firstName=request.form.get("firstName")
    email=request.form.get("email")
    lastName=request.form.get("lastName")
    db.execute("insert into users (first_name, last_name, email, password) values(:first_name,:last_name,:email,:password)",{"first_name":firstName,"last_name":lastName,"email":email,"password":hashed_password})
    db.commit()
    session["user"]=firstName
    return redirect(url_for('search'))


@app.route("/search")
def search():
    if 'user' in session:
        locations=db.execute("select * from locations").fetchall()
        return render_template("search.html",locations=locations)
    return redirect(url_for('mainPage'))

@app.route("/location",methods=["post"])
def location():
    showSignUp=1
    showLogOut=1
    if 'user' in session:
        showSignUp=0
        isUser=1
        permitionOfComment=0
        locationsInfo=request.form.get("locationsInfo")
        location=db.execute("select * from locations where zipcode=:zipcode or city=:city",{"zipcode":locationsInfo,"city":locationsInfo}).fetchone()
        lat=location.lat
        log=location.long
        currentUser=db.execute("select * from users where first_name=:first_name",{"first_name":session["user"]}).fetchone()
        commentOfThisCity=db.execute("select * from comments where user_id=:user_id and location_id=:location_id",{"user_id":currentUser.id,"location_id":location.id}).fetchone()
        if commentOfThisCity==None:
            permitionOfComment=1
        location_id=location.id
        comment=db.execute("select comment,first_name from comments join locations on comments.location_id=locations.id join users on comments.user_id=users.id where locations.id=:location_id",{"location_id":location_id}).fetchall()
        res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
        weatherDump=json.dumps(res["currently"])
        weather = json.loads(weatherDump)
        return render_template("locations.html",location=location,weather=weather,comment=comment,permitionOfComment=permitionOfComment,user_id=currentUser.id,isUser=isUser,showSignUp=showSignUp,showLogOut=showLogOut)

    return redirect(url_for('mainPage'))


@app.route("/locationGet/<location_id>/<user_id>")
def locationGet(location_id,user_id):
    isUser=1
    showSignUp=1
    showLogOut=1
    if 'user' in session:
        showSignUp=0
        permitionOfComment=0
        location=db.execute("select * from locations where id=:location_id",{"location_id":location_id}).fetchone()
        lat=location.lat
        log=location.long
        currentUser=db.execute("select * from users where id=:user_id",{"user_id":user_id}).fetchone()
        commentOfThisCity=db.execute("select * from comments where user_id=:user_id and location_id=:location_id",{"user_id":user_id,"location_id":location_id}).fetchone()
        if commentOfThisCity==None:
            permitionOfComment=1
        comment=db.execute("select comment,first_name from comments join locations on comments.location_id=locations.id join users on comments.user_id=users.id where locations.id=:location_id",{"location_id":location_id}).fetchall()
        res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
        weatherDump=json.dumps(res["currently"])
        weather = json.loads(weatherDump)
        return render_template("locations.html",location=location,weather=weather,comment=comment,permitionOfComment=permitionOfComment,user_id=user_id,isUser=isUser,showSignUp=showSignUp,showLogOut=showLogOut)
    else:
        showLogOut=0
        isUser=0
        location=db.execute("select * from locations where id=:location_id",{"location_id":location_id}).fetchone()
        lat=location.lat
        log=location.long
        res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
        weatherDump=json.dumps(res["currently"])
        weather = json.loads(weatherDump)
        return render_template("locations.html",location=location,weather=weather,isUser=isUser,showSignUp=showSignUp,showLogOut=showLogOut)


@app.route("/locationGetId/<location_id>/")
def locationGetId(location_id):
    showSignUp=1
    showLogOut=0
    isUser=0
    location=db.execute("select * from locations where id=:location_id",{"location_id":location_id}).fetchone()
    lat=location.lat
    log=location.long
    res = requests.get(f"https://api.darksky.net/forecast/3b941c6184523c05db2a68af08a67c51/{lat},{log}").json()
    weatherDump=json.dumps(res["currently"])
    weather = json.loads(weatherDump)
    return render_template("locations.html",location=location,weather=weather,isUser=isUser,showSignUp=showSignUp,showLogOut=showLogOut)



@app.route("/comment/<location_id>/<user_id>",methods=["post","get"])
def comment(location_id,user_id):
    if 'user' in session:
        comment=request.form.get("comment")
        db.execute("insert into comments (location_id,user_id,comment) values(:location_id,:user_id,:comment)",{"location_id":location_id,"user_id":user_id,"comment":comment})
        db.commit()
        return redirect(url_for("locationGet",location_id=location_id,user_id=user_id))
    return redirect(url_for('mainPage'))




"""builtins.AttributeError
AttributeError: Could not locate column in row for column 'zip'
"""
@app.route("/api/<int:zip>", methods=["get"])
def sendJson(zip):
    locations=db.execute("select * from locations where zipcode=':zip'",{"zip":zip}).fetchone()
    if locations is None:
        return jsonify({"error": "invalid location zip code"}),422

    return jsonify({
        "place_name": locations.city,
        "state": locations.state,
        "latitude": locations.lat,
        "longitude": locations.long,
        "zip": locations.zip,
        "population": locations.population
    })

@app.route("/sessionDestroy", methods=["post"])
def sessionDestroy():
    session.pop('user', None)
    return redirect(url_for("mainPage"))








@app.route("/protectedPage")
def protectedPage():
    if 'user' in session:
        return render_template("protectedPage.html",user=session["user"])
    message='please log in page'
    return render_template("login.html",message=message)



@app.route("/getsession")
def getsession():
    if 'user' in session:
        return session['user']

    return 'you aren t logged in page'

@app.route("/logout")
def dropsession():
    session.pop('user', None)
    return 'you logged out !'
