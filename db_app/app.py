from flask import Flask, url_for, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
#import psycopg2
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///class_db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Class(db.Model):
    __tablename__ = "Class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    hobby = db.Column(db.String(225))
    age = db.Column(db.Integer)

@app.route("/")
def index():
    results = db.session.query(Class.name, Class.hobby, Class.age)
    return render_template("index.html", results = results)

@app.route("/update", methods = ["POST"])
def update_db():
    name = request.form["name"]
    hobby = request.form["hobby"]
    age = request.form["age"]

    person = Class(name = name, hobby = hobby, age = age)
    db.session.add(person)
    db.session.commit()

    return redirect("/", code = 302)

@app.route("/plot")
def show_plot():
    return render_template("plot.html")

@app.route("/data")
def data():
    results = []
    for result in db.session.query(Class.name,Class.hobby, Class.age).all():
        results.append({
            "name" : result[0],
            "hobby" : result[1],
            "age" : result[2]
        })
    return(jsonify(results))



if __name__ == "__main__":
    app.run(debug = True)
