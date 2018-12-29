from flask import Flask, url_for, render_template

app=Flask(__name__)


@app.route("/")
def mainPage():
    return render_template("index.html")


if 'user' in session:
    locations=db.execute("select * from locations").fetchall()
    return render_template("search.html",locations=locations,username=session["user"])
return redirect(url_for('mainPage'))
