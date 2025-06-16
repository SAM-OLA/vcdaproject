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

        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        address=request.form["houseaddress"],
        apartmenttype=request.form["apartmenttype"],
        groupid='0',
        phonenumber=request.form["mobilenumber"]
        today = datetime.datetime.now()
        dateregistered = f'{today.strftime("%d")}/{today.strftime("%m")}/{today.strftime("%Y")} {today.strftime("%H")}:{today.strftime("%M")}:{today.strftime("%S")}'
        cur1.execute( 
        '''INSERT INTO register 
        (title,surname, firstname,othernames,address,apartmenttype,groupid,phonenumber) VALUES (%s,%s,%s, %s,%s, %s,%s,%s)''', 
        (title,surname, firstname,othernames,address,apartmenttype,groupid,phonenumber)) 
        
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
            (username, password,status,dateregistered,defaultpwd, logindate) VALUES (%s, %s,%s, %s,%s,%s)''',
            (phonenumber, hashed_password, '1',dateregistered,'1',dateregistered))
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
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl = "register")
        except:
            return render_template("Failure.html", messageText = "Data Error - Phone Number Already Exists", redirecturl = "register")

@app.route("/updateregister", methods=["GET", "POST"])
def updateregister():
    if request.method == "POST":
        # CREATE RECORD
        
        conn1 = functionbase.connection()
  
        cur1 = conn1.cursor() 
  
        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        address=request.form["houseaddress"],
        apartmenttype=request.form["apartmenttype"],
        groupid='0',
        phonenumber=request.form["mobilenumber"]
    
        
        cur1.execute("UPDATE register SET title=%s, surname=%s, firstname=%s, othernames=%s, address=%s, apartmenttype=%s WHERE phonenumber=%s",(title,surname,firstname,othernames,address,apartmenttype,phonenumber))
     
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl="login")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("Failure.html", messageText = "Update Error", redirecturl="login")
            
    
    
@app.route("/login_confirm", methods=["GET", "POST"])
def login_confirm():
    if request.method == "POST":
        # CREATE RECORD
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        con3 = functionbase.connection()
        con4 = functionbase.connection()
        con5 = functionbase.connection()
        con6 = functionbase.connection()

        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        cur3 = con3.cursor() 
        cur4 = con4.cursor() 
        cur5 = con5.cursor() 
        cur6 = con6.cursor() 

        phonenumber=request.form["phonenumber"],
        password=request.form["password"]
        dictdata = {}
         
        sql1 = 'SELECT * from users where username=%s and password=crypt(%s,password)'
        sql2 = 'SELECT * from register where phonenumber=%s'
        sql3 = 'SELECT * from paymenttransactions where phonenumber=%s and transtype=%s'
        sql5 = 'SELECT * from paymenttransactions where groupid=%s and transtype=%s'
        
        param = (phonenumber,password)
        param2 = (phonenumber)
        param3 = (phonenumber,"ESTATE DUE")
        
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
            #print(myresult3)
            for payamt in myresult3:
                totalpaid = totalpaid + float(payamt[3].replace(',',''))
                #payamt[3] = f'{float(payamt[3]):,}'

            dictdata['title'] = myresult2[1]
            dictdata['surname'] = myresult2[2]
            dictdata['firstname'] = myresult2[3]
            dictdata['othernames'] = myresult2[4]
            dictdata['address'] = myresult2[5]
            dictdata['groupid'] = myresult2[7]
            dictdata['phonenumber'] = myresult2[8]
            dictdata['apartmenttypecode'] = myresult4[1]
            dictdata['apartmenttype'] = myresult4[2]
            dictdata['apartmenttypeamount'] = f'{myresult4[3]:,}'
            dictdata['totalpaid'] = f'{totalpaid:,}'
            dictdata['balancetopay'] = f'{float(myresult4[3]) - totalpaid:,}'
            dictdata['outstandingpay'] = True if float(myresult4[3]) - totalpaid > 0 else False
            dictdata['payments'] = myresult3
        
            param5 = (int(dictdata['groupid']),"OTHER FEES")
            cur5.execute(sql5,param5)
            try:
                today = datetime.datetime.now()
                logindate = f'{today.strftime("%d")}/{today.strftime("%m")}/{today.strftime("%Y")} {today.strftime("%H")}:{today.strftime("%M")}:{today.strftime("%S")}'
                param6 = logindate
                sql6 = "UPDATE users SET logindate = '{logdate}' WHERE username = '{uname}';".format(logdate=logindate,uname=dictdata['phonenumber'])
                cur6.execute(sql6)
                con6.commit()
            except Exception as ee:
                print(f"An error occurred: {str(ee)}")
            myresult5 = [item for item in cur5.fetchall()]
            cur5.close() 
            con5.close() 
            cur6.close() 
            con6.close() 
            dictdata['otherfees'] = myresult5
            #print(dictdata)
            #if(numrows > 0):

            return render_template("dashboard.html", customerdata = dictdata)
        else:
            return render_template("Failure.html", messageText = f"Login NOT Successful for {phonenumber}",redirecturl="login")
        

@app.route("/add_payment", methods=["GET", "POST"])
def add_payment():
    if request.method == "POST":
        # CREATE RECORD
        transcode= ''
        groupid=0
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        
        transtype = request.form["transtype"],
        phonenumber = request.form["phonenumber"],
        description = request.form["description"]
        amount = request.form["amount"]
        paymentdate = request.form["paymentdate"]
        paymenttype = request.form["paymenttype"]
        cashcollector = request.form["cashcollector"]
        
        if (transtype[0] == '1'):
            transcode='ESTATE DUE'
        else:
            transcode='OTHER FEES'
        param2 = (phonenumber)
        sql2 = "select groupid from register where phonenumber = %s"
        cur2.execute(sql2,param2)
        myresult = cur2.fetchone()
        groupid = myresult[0]
        

        cur1.execute( 
        '''INSERT INTO paymenttransactions 
        (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,transtype,groupid,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''', 
        (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,transcode,groupid,'PENDING')) 
        con1.commit()
        cur1.close() 
        con1.close() 
        return render_template("Success.html", messageText = f"Payment Successfully added for {phonenumber}", redirecturl="payment")

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

@app.route('/edit_profile/<varphonenumber>')
def edit_profile(varphonenumber):
    #print(varprofile)
    #resvarprofile = ast.literal_eval(varprofile) # this converts String Dict to Python Dict
    #print('*'*24)
    #print(resvarprofile)
    varprofile = {}
    con = functionbase.connection()
    cur = con.cursor() 
    sql = f"SELECT * from register where phonenumber='{varphonenumber}'"
    #param = (varphonenumber)
    cur.execute(sql)
    myresult = cur.fetchone()
    varprofile['title'] = myresult[1]
    varprofile['surname'] = myresult[2]
    varprofile['firstname'] = myresult[3]
    varprofile['othernames'] = myresult[4]
    varprofile['address'] = myresult[5]
    varprofile['apartmenttypecode'] = myresult[6]
    varprofile['phonenumber'] = myresult[8]

    return render_template("edit_profile.html", profile=varprofile)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/changepassword')
def changepassword():
    return render_template("changepassword.html")


@app.route("/processchangepassword", methods=["GET", "POST"])
def processchangepassword():
    if request.method == "POST":
        # CREATE RECORD
        conn1 = functionbase.connection()
        conn2 = functionbase.connection()
        conn3 = functionbase.connection()
        conn4 = functionbase.connection()

        cur1 = conn1.cursor() 
        cur2 = conn2.cursor() 
        cur3 = conn3.cursor() 
        cur4 = conn4.cursor() 

        phonenumber=request.form["phonenumber"]
        newpassword=request.form["newpassword"]
        retypepassword=request.form["retypepassword"]

        param1 = phonenumber
        sql1 = "select * from users where username ='{}'".format(str(param1))
        
        cur1.execute(sql1)
        myresult = cur1.fetchone()
        if myresult:
            nooftimes = myresult[5]   
            # Define the new password to be hashed
            password = newpassword
            # Generate a salt using gen_salt
            cur3.execute("SELECT gen_salt('md5')")
            salt = cur3.fetchone()[0]
            # Hash the password using crypt
            cur4.execute("SELECT crypt(%s, %s)", (password, salt))
            hashed_password = cur4.fetchone()[0]
            try:
            
                cur2.execute("UPDATE users SET password = %s, defaultpwd=%s WHERE username = %s",(hashed_password, (int(nooftimes)+1),phonenumber))
                # commit the changes 
                conn2.commit()

                # close the cursor and connection 
                cur1.close() 
                cur2.close() 
                cur3.close() 
                cur4.close() 
                conn1.close() 
                conn2.close() 
                conn3.close() 
                conn4.close() 
                return render_template("success.html", messageText = "Password Changed Successfully", redirecturl="login")
            except Exception as er:
                print(er)
                return render_template("Failure.html", messageText = "Password Change Failed", redirecturl="login")
        else:
            return render_template("Failure.html", messageText = "Resident with this Phone Number Does Not Exists", redirecturl="login")

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