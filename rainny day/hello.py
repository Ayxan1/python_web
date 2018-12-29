import os
from flask import Flask, url_for, render_template, request, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

notes=[]


@app.route('/app/flights/<id>')
def main4(id):
    flights=db.execute("select * from flights where id=:id",{"id":id}).fetchone()
    if flights is None:
        return jsonify({"error": "invalid flight id"}),422
    passengers=db.execute("select  * from passengers join flights on passengers.flight_id=flights.id where passengers.flight_id=:flight_id",{"flight_id":id}).fetchall()
    names=[]
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
        "origin":flights.origin,
        "destination":flights.destination,
        "duration":flights.duration,
        "passengers":names
    })



@app.route('/3')
def main3():
    hashed_password=2141241
    firstName='aasfasf'
    email='aasfasf'
    lastName='aasfasf'
    db.execute("insert into users (first_name, last_name, email, password) values(:first_name,:last_name,:email,:password)",{"first_name":firstName,"last_name":lastName,"email":email,"password":hashed_password})
    """flights=db.execute("select * from flights").fetchall()"""
    db.commit()
    return 'added' """render_template("flightBrochure.html",flights=flights)"""


@app.route("/brochure/<id>")
def brochure(id):
    no=1
    flights=db.execute("select * from flights where id=:id",{"id":id}).fetchall()
    passengers=db.execute("select  * from passengers join flights on passengers.flight_id=flights.id where passengers.flight_id=:flight_id",{"flight_id":id}).fetchall()
    if len(passengers)>0:
        no=0
    return render_template("brochureContent.html",flights=flights,passengers=passengers,no=no)





@app.route('/')
def main1():
    flights=db.execute("select * from flights").fetchall()
    return render_template("bookFlight.html", flights=flights)

@app.route('/2')
def main2():
    flights=db.execute("select * from flights").fetchall()
    return render_template("formPassenger.html",flights=flights)


@app.route('/flight_list',methods=["POST"])
def flight_list():
    flight_id=request.form.get("flight_id")
    name=request.form.get("passenger_name")
    db.execute("insert into passengers (name,flight_id) values(:name,:flight_id)",{"name":name,"flight_id":flight_id})
    db.commit()
    return "successfully booked"

@app.route('/passenger_list',methods=["POST"])
def passenger_list():
    flight_id=request.form.get("flight_id")
    passengers=db.execute("select  * from passengers join flights on passengers.flight_id=flights.id where passengers.flight_id=:flight_id",{"flight_id":flight_id}).fetchall()
    len1=len(passengers)
    return render_template("test.html",passengers=passengers,len1=len1)







@app.route('/submit',methods=["post"])
def submit():
    origin=request.form.get("origin_name")
    destination=request.form.get("destination_name")
    duration=request.form.get("duration_name")
    db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
                    {"origin": origin, "destination": destination, "duration": duration})
    db.commit()
    return note()

@app.route('/other')
def note():
    flights=db.execute("select origin, destination, duration from flights").fetchall()
    return  render_template("other.html",flights=flights)


""""



@app.route('/other',methods=["POST", "GET"])
def note():
    if session.get("notes") is None:
        session["notes"]=[]
    if request.method=="POST":
        note=request.form.get("note")
        session["notes"].append(note)
        return render_template("other.html",notes=session["notes"])

    return render_template("other.html",notes=session["notes"])

"""

"""
@app.route('/')
def mainPag():
    return render_template('mainPag.html')
"""

"""
@app.route('/user',methods=["POST", "GET"])
def user():
    if request.method=="GET":
        return "fill the form"
    name=request.form.get("name")
    return render_template("user.html",name=name)
"""



"""
@app.route('/main',methods=["POST", "GET"])
def main1():
    return render_template("other.html")
________________________________________________
"""


"""
session['username']='ayxan'

@app.route('/')
def login1():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    if request.form['username'] in session:
            return render_template('userPage.html',user=request.form['username'])
    return redirect(url_for('login1'))


"""
"""
@app.route('/')
def hello_user():
    names=["ayxan", "toyxan", "eflatun"]
    return render_template("hello.html",names=names)

@app.route('/main')
def mainPag():
    return render_template("main.html")

@app.route('/projects')
def project(username):
    return 'the projects'

@app.route('/hello/<name>')
def welcome_user(name):
    return render_template('hello.html',name=name)

@app.route('/login',methods=['POST','GET'])
def login():
    error=None
    if request.method=='POST':
"""
