from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#from sqlalchemy import Integer, String, Float
#import sqlite3
import psycopg2

app = Flask(__name__)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        conn = psycopg2.connect(database="victoryestate", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", port="5432") 
        cur = conn.cursor() 
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        address=request.form["houseaddress"],
        phonenumber=request.form["mobilenumber"]
        id = 2
        cur.execute( 
        '''INSERT INTO register 
        (id,surname, firstname,othernames,address,phonenumber) VALUES (%s,%s, %s,%s, %s,%s)''', 
        (id,surname, firstname,othernames,address,phonenumber)) 
  
        # commit the changes 
        conn.commit() 
  
        # close the cursor and connection 
        cur.close() 
        conn.close() 
        return f'Data Successfully added for {surname}'+'*'*5

@app.route('/')
def home():
    return render_template('index.html',)

@app.route('/aboutus')
def about_us():
    return render_template("aboutus.html")

@app.route('/contactus')
def contact_us():
    return render_template("contactus.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/feeslist')
def feeslist():
    return render_template("feeslist.html")

@app.route('/<name>')
def greet(name):
    return f'Hello there {name}!'


if __name__ == '__main__':
    app.run(debug=True)