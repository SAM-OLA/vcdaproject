from flask import Flask, render_template, request, redirect, url_for
import functionbase
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#from sqlalchemy import Integer, String, Float
#import sqlite3


app = Flask(__name__)

  
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        conn1 = functionbase.connection()
        conn2 = functionbase.connection()
        conn3 = functionbase.connection()

        cur1 = conn1.cursor() 
        cur2 = conn2.cursor() 
        cur3 = conn3.cursor() 

        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        address=request.form["houseaddress"],
        apartmenttype=request.form["apartmenttype"],
        phonenumber=request.form["mobilenumber"]
    
        cur1.execute( 
        '''INSERT INTO register 
        (surname, firstname,othernames,address,apartmenttype,phonenumber) VALUES (%s,%s, %s,%s, %s,%s)''', 
        (surname, firstname,othernames,address,apartmenttype,phonenumber)) 
        
        # Define the password to be hashed
        password = 'guest'
        # Generate a salt using gen_salt
        cur3.execute("SELECT gen_salt('md5')")
        salt = cur3.fetchone()[0]

        # Hash the password using crypt
        cur3.execute("SELECT crypt(%s, %s)", (password, salt))
        hashed_password = cur3.fetchone()[0]

        cur2.execute( 
        '''INSERT INTO users 
        (username, password,status,dateregistered,defaultpwd) VALUES (%s, %s,%s, %s,%s)''',
        (phonenumber, hashed_password, '1','31/01/2025','1'))
        #insert into users values('tayo', crypt('guest', gen_salt('md5')), '1','31/01/2025','1')
  
        # commit the changes 
        conn1.commit()
        conn2.commit()
        conn3.commit()

        # close the cursor and connection 
        cur1.close() 
        cur2.close() 
        cur3.close() 
        conn1.close() 
        conn2.close() 
        conn3.close() 
        return f'Data Successfully added for {surname}'+'*'*5
    
@app.route("/login_confirm", methods=["GET", "POST"])
def login_confirm():
    if request.method == "POST":
        # CREATE RECORD
        conn1 = functionbase.connection()
        cur1 = conn1.cursor() 
        phonenumber=request.form["phonenumber"],
        password=request.form["password"]

        sql = 'SELECT * from users where username=%s and password=crypt(%s,password)'
        param = (phonenumber,password)
        cur1.execute(sql,param)
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        myresult = cur1.fetchone()  
        cur1.close() 
        conn1.close() 
        if(numrows > 0):
            return render_template("dashboard.html", phonenumber1=phonenumber)
        else:
            return f'<h3>Login NOT Successful for {phonenumber}</h3>'+'*'*5

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