from flask import Flask, render_template, request, redirect, url_for
import functionbase
import datetime
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#from sqlalchemy import Integer, String, Float
import sqlite3
import ast

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
        groupid='0',
        phonenumber=request.form["mobilenumber"]
    
        cur1.execute( 
        '''INSERT INTO register 
        (surname, firstname,othernames,address,apartmenttype,groupid,phonenumber) VALUES (%s,%s, %s,%s, %s,%s,%s)''', 
        (surname, firstname,othernames,address,apartmenttype,groupid,phonenumber)) 
        
        # Define the password to be hashed
        password = 'guest'
        # Generate a salt using gen_salt
        cur3.execute("SELECT gen_salt('md5')")
        salt = cur3.fetchone()[0]

        # Hash the password using crypt
        cur3.execute("SELECT crypt(%s, %s)", (password, salt))
        hashed_password = cur3.fetchone()[0]
        try:
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
            return render_template("success.html", messageText = "Data Successfully Saved")
        except:
            return render_template("Failure.html", messageText = "Data Error - Phone Number Already Exists")
    
@app.route("/login_confirm", methods=["GET", "POST"])
def login_confirm():
    if request.method == "POST":
        # CREATE RECORD
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        con3 = functionbase.connection()
        con4 = functionbase.connection()

        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        cur3 = con3.cursor() 
        cur4 = con4.cursor() 

        phonenumber=request.form["phonenumber"],
        password=request.form["password"]
        dictdata = {}
         
        sql1 = 'SELECT * from users where username=%s and password=crypt(%s,password)'
        sql2 = 'SELECT * from register where phonenumber=%s'
        sql3 = 'SELECT * from paymenttransactions where phonenumber=%s'
        
        param = (phonenumber,password)
        param2 = (phonenumber)
        param3 = (phonenumber)
        cur1.execute(sql1,param)
        cur2.execute(sql2,param2)
        cur3.execute(sql3,param3)
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
           
            myresult1 = cur1.fetchone()
            myresult2 = cur2.fetchone()
            sql4 = "SELECT * from apartment_type where code='{}'".format(str(myresult2[6]))
            cur4.execute(sql4)
            myresult4 = cur4.fetchone()
            #myresult3 = cur3.fetchall()
            myresult3 = [item for item in cur3.fetchall()]
            cur1.close() 
            con1.close() 
            cur2.close() 
            con2.close() 
            cur3.close() 
            con3.close() 
            totalpaid=0
            print(myresult3)
            for payamt in myresult3:
                totalpaid = totalpaid + float(payamt[3].replace(',',''))
                #payamt[3] = f'{float(payamt[3]):,}'

            dictdata['title'] = myresult2[1]
            dictdata['surname'] = myresult2[2]
            dictdata['firstname'] = myresult2[3]
            dictdata['othernames'] = myresult2[4]
            dictdata['address'] = myresult2[5]
            dictdata['apartmenttype'] = myresult4[2]
            dictdata['apartmenttypeamount'] = f'{myresult4[3]:,}'
            dictdata['totalpaid'] = f'{totalpaid:,}'
            dictdata['balancetopay'] = f'{float(myresult4[3]) - totalpaid:,}'
            dictdata['outstandingpay'] = True if float(myresult4[3]) - totalpaid > 0 else False
            dictdata['payments'] = myresult3
            
            print(dictdata)
            #if(numrows > 0):

            return render_template("dashboard.html", customerdata = dictdata)
        else:
            return render_template("Failure.html", messageText = f"Login NOT Successful for {phonenumber}")
        

@app.route("/add_payment", methods=["GET", "POST"])
def add_payment():
    if request.method == "POST":
        # CREATE RECORD
        con1 = functionbase.connection()
        cur1 = con1.cursor() 
        phonenumber = request.form["phonenumber"],
        description = request.form["description"]
        amount = request.form["amount"]
        paymentdate = request.form["paymentdate"]
        paymenttype = request.form["paymenttype"]
        cashcollector = request.form["cashcollector"]

        cur1.execute( 
        '''INSERT INTO paymenttransactions 
        (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,status) VALUES (%s,%s,%s,%s,%s,%s,%s)''', 
        (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,'PENDING')) 
        con1.commit()
        cur1.close() 
        con1.close() 
        return render_template("Success.html", messageText = f"Payment Successfully added for {phonenumber}")

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

@app.route('/edit_profile/<varprofile>')
def edit_profile(varprofile):
    resvarprofile = ast.literal_eval(varprofile) # this converst String Dict to Python Dict
    return render_template("edit_profile.html", profile=resvarprofile)

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/feeslist')
def feeslist():
    return render_template("feeslist.html")

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/<name>')
def greet(name):
    return f'Hello there {name}!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)