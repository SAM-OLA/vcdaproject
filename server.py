from flask import Flask, redirect, url_for, flash, render_template, request, send_file
#from flask_mail import Mail, Message
from flask_mailman import Mail, EmailMessage
from decimal import Decimal
from openpyxl.styles import Alignment
#from numpy import integer
import functionbase
import datetime
import pandas as pd
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#from sqlalchemy import Integer, String, Float
import sqlite3
import ast, os
#import cryptography

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'email-smtp.us-east-1.amazonaws.com' 
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'AKIARSU7K3NOXT55DK46'  
app.config['MAIL_PASSWORD'] = 'BO+qoW01L+T7XyTd6Nx5wSNj+jOBHWlhCm1i3UEd0cSe' 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.update(SECRET_KEY=os.urandom(24)
)
mail = Mail()
mail.init_app(app)
  
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        conn1 = functionbase.connection()
        conn2 = functionbase.connection()
        conn3 = functionbase.connection()

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="register")

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
        phonenumber1=request.form["mobilenumber1"]
        phonenumber2 = request.form["mobilenumber2"]
        print(5 * '*')
        print(phonenumber1)
        print(phonenumber2)
        if phonenumber2.startswith('0'):
            phonenumber2 = phonenumber2.lstrip('0')
        phonenumber1 = (phonenumber1.lstrip('+')).rstrip()
        phonenumber = phonenumber1+phonenumber2
        print(phonenumber)
        #phonenumber = "".join(char for char in phonenumber if char.isnumeric())
        today = datetime.datetime.now()
        dateregistered = f'{today.strftime("%d")}/{today.strftime("%m")}/{today.strftime("%Y")} {today.strftime("%H")}:{today.strftime("%M")}:{today.strftime("%S")}'
        cur1.execute( 
        '''INSERT INTO register 
        (title,surname, firstname,othernames,address,apartmenttype,groupid,phonenumber,acct_number,status,landlordid) VALUES (%s,%s,%s, %s,%s, %s,%s,%s,%s,%s,%s)''', 
        (title,surname, firstname,othernames,address,apartmenttype,groupid,phonenumber,phonenumber,'ACTIVE','00')) 
        
        # Define the password to be hashed
        password = 'resident'
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
            return render_template("failure.html", messageText = "Data Error - Phone Number Already Exists", redirecturl = "register")

@app.route("/updateregister", methods=["GET", "POST"])
def updateregister():
    if request.method == "POST":
        # CREATE RECORD
        
        conn1 = functionbase.connection()

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
  
        cur1 = conn1.cursor() 
  
        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        address=request.form["houseaddress"],
        apartmenttype=request.form["apartmenttype"],
        groupid=request.form["pspgroups"],
        landlord=request.form["landlord"]
        phonenumber=request.form["mobilenumber"]
    
        
        cur1.execute("UPDATE register SET title=%s, surname=%s, firstname=%s, othernames=%s, address=%s, apartmenttype=%s, groupid= %s, landlordid=%s WHERE phonenumber=%s",(title,surname,firstname,othernames,address,apartmenttype,groupid,landlord,phonenumber))
     
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl="login")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Update Error", redirecturl="login")
            
    
    
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
        con7 = functionbase.connection()

        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")

        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        cur3 = con3.cursor() 
        cur4 = con4.cursor() 
        cur5 = con5.cursor() 
        cur6 = con6.cursor() 
        cur7 = con7.cursor() 

        phonenumber=request.form["phonenumber"],
        password=request.form["password"]
        dictdata = {}
  
        sql1 = 'SELECT * from users where username=%s and password=crypt(%s,password)'
        sql2 = 'SELECT * from register where phonenumber=%s'      
        sql5 = "SELECT * from paymenttransactions where groupid=%s and transtype=%s and TO_NUMBER(amount,'9G99999D99') <> 0.00 order by To_DATE(paymentdate,'DD/MM/YYYY')"
        sql7 = 'SELECT * from outstanding2025 where phonenumber=%s'      
        #0
        param = (phonenumber,password)
        param2 = (phonenumber)

        
        cur1.execute(sql1,param)
        cur2.execute(sql2,param2)
        
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
           
            myresult1 = cur1.fetchone()
            myresult2 = cur2.fetchone()
            sql4 = "SELECT * from apartment_type where code='{}'".format(str(myresult2[6]))
            cur4.execute(sql4)
            myresult4 = cur4.fetchone()
            #myresult3 = cur3.fetchall()
            sql3 = "SELECT * from paymenttransactions where phonenumber=%s and transtype=%s order by To_DATE(paymentdate,'DD/MM/YYYY')"
            param3 = (myresult2[9],"ESTATE DUE")
            cur3.execute(sql3,param3)
            myresult3 = [item for item in cur3.fetchall()]
            cur7.execute(sql7,param2)
            numrows7 = cur7.rowcount
            if numrows7 > 0:
                myresult7 = [item for item in cur7.fetchone()]
            cur1.close() 
            con1.close() 
            cur2.close() 
            con2.close() 
            cur3.close() 
            con3.close() 
            cur7.close() 
            con7.close() 
            totalpaid=0
            #print(myresult7)
            for payamt in myresult3:
                totalpaid = totalpaid + float(payamt[3].replace(',',''))
                #payamt[3] = f'{float(payamt[3]):,}'

            amttopaynormal = float(myresult4[3])
            if numrows7 > 0:
                outstandingpayments = float(myresult7[2].replace(',',''))
            else:
                outstandingpayments = 0.00

            dictdata['title'] = myresult2[1]
            dictdata['surname'] = myresult2[2]
            dictdata['firstname'] = myresult2[3]
            dictdata['othernames'] = myresult2[4]
            dictdata['address'] = myresult2[5]
            dictdata['groupid'] = myresult2[7]
            dictdata['phonenumber'] = myresult2[8]
            dictdata['apartmenttypecode'] = myresult4[1]
            dictdata['apartmenttype'] = myresult4[2]
            dictdata['apartmenttypeamount'] = f'{amttopaynormal + outstandingpayments:,}'
            dictdata['totalpaid'] = f'{totalpaid:,}'
            dictdata['balancetopay'] = f'{amttopaynormal + outstandingpayments - totalpaid:,}'
            dictdata['outstandingpay'] = True if amttopaynormal - totalpaid > 0 else False
            dictdata['payments'] = myresult3
            if numrows7 > 0:
                dictdata['outstandingpayments'] = f'{outstandingpayments:,}'
        
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
            return render_template("failure.html", messageText = f"Login NOT Successful for {phonenumber}",redirecturl="login")
        

@app.route("/add_payment", methods=["GET", "POST"])
def add_payment():
    if request.method == "POST":
        # CREATE RECORD
        transcode= ''
        groupid=0
        try:
            con1 = functionbase.connection()
            con2 = functionbase.connection()

            if con1 is None:
                return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="payment")

            cur1 = con1.cursor() 
            cur2 = con2.cursor() 
        
            transtype = request.form["transtype"],
            phonenumber = request.form["phonenumber"],
            description = request.form["description"]
            amount = request.form["amount"]
            paymentdate = request.form["paymentdate"]
            paymenttype = request.form["paymenttype"]
            cashcollector = request.form["cashcollector"]
            

            print('=== Phone Number ==='*3)
            print(phonenumber)
            if (transtype[0] == '1'):
                transcode='ESTATE DUE'
            else:
                transcode='OTHER FEES'
            param2 = (phonenumber)
            sql2 = "select groupid from register where phonenumber = %s"
            cur2.execute(sql2,param2)
            myresult = cur2.fetchone()
            if len(myresult) > 0:
                groupid = myresult[0]
        

            cur1.execute( 
            '''INSERT INTO paymenttransactions 
            (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,transtype,groupid,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''', 
            (phonenumber,description,amount,paymentdate,paymenttype,cashcollector,transcode,groupid,'PENDING')) 
            con1.commit()
            cur1.close() 
            con1.close()
            return render_template("success.html", messageText = f"Payment Successfully added for {phonenumber}", redirecturl="add_multiplepayment")
        except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="add_multiplepayment")


@app.route("/add_multiplepayment", methods=["GET", "POST"])
def add_multiplepayment():
        try:
            con1 = functionbase.connection()
            
            if con1 is None:
                return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="payment")
            dictdata = {}
            cur1 = con1.cursor() 
           
            sql1 = " select title,surname, firstname, othernames, phonenumber from register where status='ACTIVE' order by 2"
            cur1.execute(sql1)
            myresult = [item for item in cur1.fetchall()]
            dictdata = myresult
            cur1.close()
            con1.close()
            
            return render_template('payment_multiple.html',residentinfo = dictdata)
        except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="payment")
    

@app.route('/')
def home():
    return render_template('index.html',)

@app.route('/aboutus')
def about_us():
    return render_template("aboutus.html")

@app.route('/contactus', methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        # Retrieve form data using request.form
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # *** Process the form data here ***
        # e.g., print to console for testing
        msg = EmailMessage('Contact Us Form Submission', 'Senders Email :'+email+'\n\n'+name+'\n\n'+message,'corporateservices@victory-estate.com',['corporateservices@victory-estate.com'])
        msgbody = print(f"Name: {name}, Email: {email}, Message: {message}")
        msg.send()
        # In a real application, you might add logic to:
        # * Validate input (e.g., check for empty fields, valid email format)
        # * Sanitize data (e.g., remove leading/trailing spaces, convert email to lowercase)
        # * Send an email using Flask-Mail or Python's smtplib
        # * Save the details to a database using Flask-SQLAlchemy

        # Use flash messages for user feedback
        flash("Thank you for contacting us! We will respond shortly.", "success")
        
        # Redirect the user after successful POST to prevent resubmission issues
    #return redirect(url_for("contactus"))
        #return ("Email Sent Successfully")

    return render_template("contactus.html")
 
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/landlordregister')
def landlordregister():
    return render_template("landlord_profile.html")

@app.route('/edit_profile/<varphonenumber>')
def edit_profile(varphonenumber):
    #print(varprofile)
    #resvarprofile = ast.literal_eval(varprofile) # this converts String Dict to Python Dict
    #print('*'*24)
    #print(resvarprofile)
    varprofile = {}
    try:
        con = functionbase.connection()
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        if con is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")

        

        dictdata = {}
        cur1 = con1.cursor()
        cur2 = con2.cursor()
        sql1 = "select title,surname,firstname, address1,address2,phonenumber,index from houseowner order by 2"
        sql2 = "select groupname,address,unit,groupid from psparrangement order by 1"
        cur1.execute(sql1)
        cur2.execute(sql2)
        myresult1 = [item for item in cur1.fetchall()]
        myresult2 = [item for item in cur2.fetchall()]
        dictdata = myresult1
        dictdata2 = myresult2
        cur1.close()
        cur2.close()
        con1.close()
        con2.close()
        

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
        varprofile['groupid'] = myresult[7]
        varprofile['phonenumber'] = myresult[8]
        varprofile['acct_number'] = myresult[9]
        varprofile['status'] = myresult[10]
        varprofile['landlordid'] = int(myresult[11])
        return render_template("edit_profile.html", profile=varprofile, landlordinfo = dictdata, groupinfo = dictdata2)
    except Exception as ep:
        return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="login")

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

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")

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
                #print(er)
                return render_template("failure.html", messageText = "Password Change Failed", redirecturl="login")
        else:
            return render_template("failure.html", messageText = "Resident with this Phone Number Does Not Exists", redirecturl="login")

@app.route('/feeslist')
def feeslist():
    return render_template("feeslist.html")

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route('/full_residents_list', methods=["GET", "POST"])
def full_residents_list():
    # CREATE RECORD
   
    try:
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        dictdata = {}
        dictdata2 = {}
        sql1 = "select title,surname,firstname,address,phonenumber from register where status = 'ACTIVE' order by surname"    
        cur1.execute(sql1)
        sql2 = 'select title,surname,firstname,othernames,phonenumber,index from houseowner order by surname'    
        cur2.execute(sql2)
        myresult2 = [item for item in cur2.fetchall()]
        dictdata2 = myresult2
        cur2.close()
        con2.close()
   
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
            myresult1 = [item for item in cur1.fetchall()]
            dictdata['data'] = myresult1   
            cur1.close() 
            con1.close() 
            df = pd.DataFrame(dictdata['data'], columns=['Title', 'Surname', 'Firstname', 'Address', 'Phonenumber'])
            #df_modified = df.drop(['Status', 'ID','ID2'], axis=1) 
            with pd.ExcelWriter('residentsfulllist.xlsx') as writer:
                df.to_excel(writer,sheet_name='residents list')
                workbook = writer.book
                worksheet = writer.sheets['residents list']
                # Set width for column A (index 0) to 20
                worksheet.column_dimensions['A'].width = 7
                worksheet.column_dimensions['B'].width = 8
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 20
                worksheet.column_dimensions['E'].width = 25
                worksheet.column_dimensions['F'].width = 15
            return render_template("full_residents_list.html", residentdata = dictdata, landlordinfo = dictdata2)
        else:
            return render_template("failure.html", messageText = f"The Selected Landlord Does Not Have a Resident attached to it", redirecturl="/full_residents_list")
    except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="landlord_residents_list")

@app.route('/full_residents_list_download', methods=["GET", "POST"])
def full_residents_list_download():
    path_to_file = "residentsfulllist.xlsx" 
    return send_file(path_to_file, as_attachment=True)

@app.route('/edit_resident_profile/<varphonenumber>')
def edit_resident_profile(varphonenumber):
    varprofile = {}
    try:
        con = functionbase.connection()
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        con3 = functionbase.connection()
        if con is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")

        

        dictdata = {}
        dictdata3 = {}
        cur1 = con1.cursor()
        cur2 = con2.cursor()
        cur3 = con3.cursor()

        sql1 = "select title,surname,firstname, address1,address2,phonenumber,index from houseowner order by 2"
        sql2 = "select groupname,address,unit,groupid from psparrangement order by 1"
        sql3 = " select title,surname, firstname, othernames, phonenumber from register where status='ACTIVE' order by 2"
        
        cur1.execute(sql1)
        cur2.execute(sql2)
        cur3.execute(sql3)

        myresult1 = [item for item in cur1.fetchall()]
        myresult2 = [item for item in cur2.fetchall()]
        myresult3 = [item for item in cur3.fetchall()]
            
        dictdata = myresult1
        dictdata2 = myresult2
        dictdata3 = myresult3
        cur1.close()
        cur2.close()
        cur3.close()
        con1.close()
        con2.close()
        con3.close()
        

        cur = con.cursor() 
        sql = f"SELECT * from register where phonenumber='{varphonenumber}'"
        #param = (varphonenumber)
        cur.execute(sql)
        myresult = cur.fetchone()
        varprofile['title'] = myresult[1]
        varprofile['surname'] = myresult[2]
        varprofile['firstname'] = myresult[3]
        varprofile['othernames'] = myresult[4]
        varprofile['houseaddress'] = myresult[5]
        varprofile['apartmenttypecode'] = myresult[6]
        varprofile['groupid'] = myresult[7]
        varprofile['phonenumber'] = myresult[8]
        varprofile['acct_number'] = myresult[9]
        varprofile['status'] = myresult[10]
        varprofile['landlordid'] = int(myresult[11])
        return render_template("edit_resident_profile.html", profile=varprofile, landlordinfo = dictdata, groupinfo = dictdata2, residentinfo = dictdata3)
    except Exception as ep:
        return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="login")


@app.route("/updateresidentregister", methods=["GET", "POST"])
def updateresidentregister():
    if request.method == "POST":
        # CREATE RECORD
        
        conn1 = functionbase.connection()

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
  
        cur1 = conn1.cursor() 
  
        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        housenumber=request.form["housenumber"],
        houseaddress=request.form["houseaddress"],
        phonenumber=request.form["mobilenumber"]
    
        
        cur1.execute("UPDATE register SET title=%s, surname=%s, firstname=%s, othernames=%s, address1=%s, address2=%s WHERE phonenumber=%s",(title,surname,firstname,othernames,housenumber,houseaddress,phonenumber))
     
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl="full_residents_list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Update Error", redirecturl="login")

@app.route("/updateresidentprofile", methods=["GET", "POST"])
def updateresidentprofile():
    if request.method == "POST":
        # CREATE RECORD
        
        conn1 = functionbase.connection()

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
  
        cur1 = conn1.cursor() 
  
        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        houseaddress=request.form["houseaddress"],
        apartmenttype=request.form["apartmenttype"],
        landlordid=request.form["landlordid"],
        pspgroups=request.form["pspgroups"],
        status=request.form["status"],
        phonenumber=request.form["phonenumber"],
        mobilenumber=request.form["mobilenumber"]
    
        
        cur1.execute("UPDATE register SET title=%s, surname=%s, firstname=%s, othernames=%s, address=%s, apartmenttype=%s, groupid=%s, acct_number=%s, status=%s, landlordid=%s WHERE phonenumber=%s",(title,surname,firstname,othernames,houseaddress,apartmenttype,pspgroups,phonenumber,status,landlordid,mobilenumber))
     
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl="full_residents_list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Update Error", redirecturl="login")


@app.route('/landlord_residents_list/<varlandlordid>', methods=["GET", "POST"])
def landlord_residents_list(varlandlordid):
    # CREATE RECORD
   
    try:
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        dictdata = {}
        dictdata2 = {}
        sql1 = f"select title,surname,firstname,address,phonenumber from register where landlordid='{ varlandlordid }' and status = 'ACTIVE' order by surname"    
        cur1.execute(sql1)
        sql2 = 'select title,surname,firstname,othernames,phonenumber,index from houseowner order by surname'    
        cur2.execute(sql2)
        myresult2 = [item for item in cur2.fetchall()]
        dictdata2 = myresult2
        cur2.close()
        con2.close()
   
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
            myresult1 = [item for item in cur1.fetchall()]
            dictdata['data'] = myresult1   
            cur1.close() 
            con1.close()
            df = pd.DataFrame(dictdata['data'], columns=['Title', 'Surname', 'Firstname', 'Address', 'Phonenumber'])
            #df_modified = df.drop(['Status', 'ID','ID2'], axis=1) 
            with pd.ExcelWriter('residentlistbylandlord.xlsx') as writer:
                df.to_excel(writer,sheet_name='resident list')
                workbook = writer.book
                worksheet = writer.sheets['resident list']
                # Set width for column A (index 0) to 20
                worksheet.column_dimensions['A'].width = 7
                worksheet.column_dimensions['B'].width = 8
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 20
                worksheet.column_dimensions['E'].width = 25
                worksheet.column_dimensions['F'].width = 15

            return render_template("landlord_residents_list.html", residentdata = dictdata, landlordinfo = dictdata2, selectedtext=int(varlandlordid))
        else:
            return render_template("failure.html", messageText = f"The Selected Landlord Does Not Have a Resident attached to it", redirecturl="/full_residents_list")
    except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="landlord_residents_list")

@app.route('/residentlistbylandlord_download', methods=["GET", "POST"])
def residentlistbylandlord_download():
    path_to_file = "residentlistbylandlord.xlsx" 
    return send_file(path_to_file, as_attachment=True)



@app.route('/payments_list', methods=["GET", "POST"])
def payments_list():
    # CREATE RECORD
   
    try:
        con1 = functionbase.connection()
        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
        cur1 = con1.cursor() 
        dictdata = {}
        sql1 = "select register.title, register.surname, register.firstname, register.address,register.phonenumber,paymenttransactions.paymentdate,amount,cast(replace(amount,',','') as decimal),paymenttransactions.status,paymenttransactions.id from register inner join paymenttransactions ON register.phonenumber = paymenttransactions.phonenumber where paymenttransactions.transtype='ESTATE DUE' and paymenttransactions.status != 'REJECTED' and register.phonenumber != '0' order by surname";    
        cur1.execute(sql1)
   
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
            myresult1 = [item for item in cur1.fetchall()]
            totallist = [val[7] for val in myresult1]
            total = sum(totallist)
            #print(total)
            dictdata['data'] = myresult1
            df = pd.DataFrame(dictdata['data'], columns=['Title', 'Surname', 'Firstname', 'Address', 'Phonenumber', 'PaymentDate', 'Amount', 'Status', 'ID','ID2'])
            df_modified = df.drop(['Status', 'ID','ID2'], axis=1) 
            with pd.ExcelWriter('paymentlist.xlsx') as writer:
                df_modified.to_excel(writer,sheet_name='payment list')
                workbook = writer.book
                worksheet = writer.sheets['payment list']
                # Set width for column A (index 0) to 20
                worksheet.column_dimensions['A'].width = 7
                worksheet.column_dimensions['B'].width = 8
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 20
                worksheet.column_dimensions['E'].width = 20
                worksheet.column_dimensions['F'].width = 15
                worksheet.column_dimensions['G'].width = 15
                worksheet.column_dimensions['H'].width = 15
            cur1.close() 
            con1.close() 
            return render_template("payments_list.html", residentdata = dictdata,sumtotal=format(total,","))
    except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="admin")

@app.route('/payment_list_download', methods=["GET", "POST"])
def payment_list_download():
    path_to_file = "paymentlist.xlsx" 
    return send_file(path_to_file, as_attachment=True)

@app.route('/approve_payments', methods=["GET", "POST"])
def approve_payments():
    # CREATE RECORD

    conn1 = functionbase.connection()

    if conn1 is None:
        return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
  
    cur1 = conn1.cursor() 
    btnapprove = request.form.get('approve')
    btnreject = request.form.get('reject')
    btnok = request.form.get('btngo')
    
    if btnapprove == 'approve':
        selected_items = request.form.getlist('status')
        integer_selected_items = tuple([int(s) for s in selected_items])
        #print(integer_selected_items)     
        if len(integer_selected_items) > 1:
            strupdateQuery = f"UPDATE paymenttransactions SET status='APPROVED' WHERE id IN {integer_selected_items}"
        elif len(integer_selected_items) ==1:
            strupdateQuery = f"UPDATE paymenttransactions SET status='APPROVED' WHERE id ={integer_selected_items[0]}"
        cur1.execute(strupdateQuery)
    
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Approve Successful", redirecturl="payments_list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Approve Error", redirecturl="login")

    elif btnreject == 'reject':
        selected_items = request.form.getlist('status')
        integer_selected_items = tuple([int(s) for s in selected_items])
        #print(integer_selected_items)     
        if len(integer_selected_items) > 1:
            strupdateQuery = f"UPDATE paymenttransactions SET status='REJECTED' WHERE id IN {integer_selected_items}"
        elif len(integer_selected_items) ==1:
            strupdateQuery = f"UPDATE paymenttransactions SET status='REJECTED' WHERE id = {integer_selected_items[0]}"
        cur1.execute(strupdateQuery)
    
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("failure.html", messageText = "Payment Rejected", redirecturl="payments_list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Reject Error", redirecturl="login")
    if btnok == 'go':
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        tx_type = request.form.get('transtype')
        try:
            con1 = functionbase.connection()
            if con1 is None:
                return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
            cur1 = con1.cursor() 
            dictdata = {}
            sql1 = f"select register.title, register.surname, register.firstname, register.address,register.phonenumber,paymenttransactions.paymentdate,amount,cast(replace(amount,',','') as decimal),paymenttransactions.status,paymenttransactions.id from register inner join paymenttransactions ON register.phonenumber = paymenttransactions.phonenumber where paymenttransactions.transtype='{tx_type}' and to_date(paymenttransactions.paymentdate,'dd/mm/yyyy') >= to_date('{startdate}','dd/mm/yyyy') and to_date(paymenttransactions.paymentdate,'dd/mm/yyyy') <= to_date('{enddate}','dd/mm/yyyy') and paymenttransactions.status != 'REJECTED' and register.phonenumber != '0' order by to_date(paymenttransactions.paymentdate,'dd/mm/yyyy')";    
            #print(sql1)
            cur1.execute(sql1)
   
            numrows = cur1.rowcount
            print(f'row numbers is {numrows}')
            if(numrows > 0):
                myresult1 = [item for item in cur1.fetchall()]
                totallist = [val[7] for val in myresult1]
                total = sum(totallist)
                #print(total)
                dictdata['data'] = myresult1
                df = pd.DataFrame(dictdata['data'], columns=['Title', 'Surname', 'Firstname', 'Address', 'Phonenumber', 'PaymentDate', 'Amount', 'Status', 'ID','ID2'])
                df_modified = df.drop(['Status', 'ID','ID2'], axis=1) 
                with pd.ExcelWriter('paymentlist.xlsx') as writer:
                    df_modified.to_excel(writer,sheet_name='payment list')
                    workbook = writer.book
                    worksheet = writer.sheets['payment list']
                    # Set width for column A (index 0) to 20
                    worksheet.column_dimensions['A'].width = 7
                    worksheet.column_dimensions['B'].width = 8
                    worksheet.column_dimensions['C'].width = 20
                    worksheet.column_dimensions['D'].width = 20
                    worksheet.column_dimensions['E'].width = 20
                    worksheet.column_dimensions['F'].width = 15
                    worksheet.column_dimensions['G'].width = 15
                    worksheet.column_dimensions['H'].width = 15
                cur1.close() 
                con1.close() 
                return render_template("payments_list.html", residentdata = dictdata,sumtotal=format(total,","))
            else:
                return render_template("failure.html", messageText = f"No Data For the Selected Period", redirecturl="payments_list")
        except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="payments_list")
        
      
    
 
@app.route('/outstanding_list', methods=["GET", "POST"])
def outstanding_list():
    # CREATE RECORD
   
    try:
        con1 = functionbase.connection()
        con2 = functionbase.connection()
        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
        cur1 = con1.cursor() 
        cur2 = con2.cursor() 
        dictdata = {}
        newlistmain = []
        #newlistsub=[]
        sql1 = "select title,surname,firstname, address, apartmenttype,acct_number,amount from register inner join apartment_type on register.apartmenttype=apartment_type.code where status ='ACTIVE' and phonenumber=acct_number order by surname;"    
        sql2 = "select phonenumber, sum(cast(replace(amount,',','') as decimal)) from paymenttransactions where transtype='ESTATE DUE' group by phonenumber"    
        cur1.execute(sql1)
        cur2.execute(sql2)

        numrows1 = cur1.rowcount
        numrows2 = cur2.rowcount
        print(f'row numbers is {numrows1}')
        if(numrows1 > 0):
            myresult1 = [item for item in cur1.fetchall()]
            myresult2 = [item for item in cur2.fetchall()]
            #dictdata['data'] = myresult1   
            message=""
            total=0
            for i in range(len(myresult1)):
                flag=False
                amount=0
                
                for j in range(len(myresult2)):
                    if myresult1[i][5] == myresult2[j][0]:
                        #print(f'Balance Pay =N={myresult1[i][6]}-{myresult2[j][2]}')
                        #message= f'myresult1[i][5] PAID'
                        flag=True
                        amount=myresult2[j][1]
                        break
                if(flag):
 #                   print(f'{myresult1[i][5]} PAID *** BALANCE {Decimal(myresult1[i][6])-amount}')
                    #myresult1[i][6]= Decimal(myresult1[i][6])-amount
                    if Decimal(myresult1[i][6])-amount > 0:
                        total = total + Decimal(myresult1[i][6])-amount
                        newlistsub = [myresult1[i][0],myresult1[i][1],myresult1[i][2],myresult1[i][3],myresult1[i][4],myresult1[i][5],format(Decimal(myresult1[i][6])-amount,",")]
                        newlistmain.append(newlistsub)
                else:
  #                  print(f'{myresult1[i][5]} DID NOT PAY *** BALANCE {myresult1[i][6]}')
                    total = total + Decimal(myresult1[i][6])
                    newlistsub = [myresult1[i][0],myresult1[i][1],myresult1[i][2],myresult1[i][3],myresult1[i][4],myresult1[i][5],format(Decimal(myresult1[i][6]),",")]
                    newlistmain.append(newlistsub)                
#            print("============HELO===============")
#            print(newlistmain)
            dictdata['data'] = newlistmain
            #print("============ HELO START===============")
            #print(dictdata )
            #print("============ HELO END ===============")

            df = pd.DataFrame(dictdata['data'], columns=['Title', 'Surname', 'Firstname', 'Address', 'Apartment Type', 'Phonenumber', 'Amount'])
            df_modified = df.drop('Apartment Type', axis=1) 
            with pd.ExcelWriter('outstandinglist.xlsx') as writer:
                df_modified.to_excel(writer,sheet_name='outstanding list')
                workbook = writer.book
                worksheet = writer.sheets['outstanding list']
                # Set width for column A (index 0) to 20
                worksheet.column_dimensions['A'].width = 7
                worksheet.column_dimensions['B'].width = 8
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 20
                worksheet.column_dimensions['E'].width = 25
                worksheet.column_dimensions['F'].width = 15
                worksheet.column_dimensions['G'].width = 15
            print(total)
            cur1.close() 
            con1.close()
            
            return render_template("outstanding_list.html", residentdata = dictdata, sumtotal=format(total,","))
    except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="admin")


@app.route('/outstanding_list_download', methods=["GET", "POST"])
def outstanding_list_download():
    path_to_file = "outstandinglist.xlsx" 
    return send_file(path_to_file, as_attachment=True)


@app.route('/landlord_list', methods=["GET", "POST"])
def landlord_list():
    # CREATE RECORD
   
    try:
        con1 = functionbase.connection()
        if con1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
        
        cur1 = con1.cursor() 
        dictdata = {}
        sql1 = "select title,concat(surname,' ',firstname,' ',othernames) as name,address1,address2,phonenumber from houseowner order by name";    
        cur1.execute(sql1)
   
        numrows = cur1.rowcount
        print(f'row numbers is {numrows}')
        if(numrows > 0):
            myresult1 = [item for item in cur1.fetchall()]
            dictdata['data'] = myresult1   
            cur1.close() 
            con1.close() 
            return render_template("landlord_list.html", residentdata = dictdata)
    except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="admin")



@app.route('/edit_landlord_profile/<varphonenumber>')
def edit_landlord_profile(varphonenumber):
    #print(varprofile)
    #resvarprofile = ast.literal_eval(varprofile) # this converts String Dict to Python Dict
    #print('*'*24)
    #print(resvarprofile)
    varprofile = {}
    try:
        con = functionbase.connection()
        con1 = functionbase.connection()
        if con is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")

        cur = con.cursor() 
        sql = f"SELECT * from houseowner where phonenumber='{varphonenumber}'"
        #param = (varphonenumber)
        cur.execute(sql)
        myresult = cur.fetchone()
        varprofile['title'] = myresult[1]
        varprofile['surname'] = myresult[2]
        varprofile['firstname'] = myresult[3]
        varprofile['othernames'] = myresult[4]
        varprofile['address1'] = myresult[5]
        varprofile['address2'] = myresult[6]
        varprofile['phonenumber'] = myresult[7]
        return render_template("edit_landlord_profile.html", profile=varprofile)
    except Exception as ep:
        return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="/landlord_list")

@app.route("/updatelanlordregister", methods=["GET", "POST"])
def updatelanlordregister():
    if request.method == "POST":
        # CREATE RECORD
        
        conn1 = functionbase.connection()

        if conn1 is None:
            return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="login")
  
        cur1 = conn1.cursor() 
  
        title=request.form["title"],
        surname=request.form["surname"],
        firstname=request.form["firstname"],
        othernames=request.form["othername"],
        housenumber=request.form["housenumber"],
        houseaddress=request.form["houseaddress"],
        phonenumber=request.form["mobilenumber"]
    
        
        cur1.execute("UPDATE houseowner SET title=%s, surname=%s, firstname=%s, othernames=%s, address1=%s, address2=%s WHERE phonenumber=%s",(title,surname,firstname,othernames,housenumber,houseaddress,phonenumber))
     
        try:
            # commit the changes 
            conn1.commit()
            # close the cursor and connection 
            cur1.close() 
            conn1.close() 
            return render_template("success.html", messageText = "Data Successfully Saved", redirecturl="landlord_list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("failure.html", messageText = "Update Error", redirecturl="login")
            
@app.route("/add_landlord", methods=["GET", "POST"])
def add_landlord():
    if request.method == "POST":
        # CREATE RECORD
        try:
            con1 = functionbase.connection()
            

            if con1 is None:
                return render_template("failure.html", messageText = f"Connection Error!!! Server Cannot be reached",redirecturl="landlord_list")

            cur1 = con1.cursor() 
            
        
            title=request.form["title"],
            surname=request.form["surname"],
            firstname=request.form["firstname"],
            othernames=request.form["othername"],
            housenumber=request.form["housenumber"],
            houseaddress=request.form["houseaddress"],
            phonenumber=request.form["mobilenumber"]

            cur1.execute( 
            '''INSERT INTO houseowner 
            (title,surname,firstname,othernames,address1,address2,phonenumber) VALUES (%s,%s,%s,%s,%s,%s,%s)''', 
            (title,surname,firstname,othernames,housenumber,houseaddress,phonenumber)) 
            con1.commit()
            cur1.close() 
            con1.close()
            return render_template("success.html", messageText = f"LandLord Successfully added for {phonenumber}", redirecturl="landlord_list")
        except Exception as ep:
            return render_template("failure.html", messageText = f"Error Occured -  {str(ep)}", redirecturl="landlord_list")

    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(host="0.0.0.0", port=5000, debug=True, ssl_context='adhoc')


'''
SELECT sum(TO_NUMBER(amount,'9G99999D99')) FROM paymenttransactions where transtype='ESTATE DUE' and phonenumber IN (select phonenumber from register where apartmenttype='002' AND status='ACTIVE');
select count(*) from register where apartmenttype='002' AND status='ACTIVE' AND phonenumber=acct_number;;

''' 

'''
select 'Bungalow',COUNT(*) from register where apartmenttype='001' and status = 'ACTIVE'
union
select 'Flats',COUNT(*) from register where apartmenttype='002' and status = 'ACTIVE'
union
select 'Duplex',COUNT(*) from register where apartmenttype='003' and status = 'ACTIVE'
union
select 'Single Room',COUNT(*) from register where apartmenttype='004' and status = 'ACTIVE'
union
select 'Mini Flats',COUNT(*) from register where apartmenttype='005' and status = 'ACTIVE'
union
select 'Self Contained',COUNT(*) from register where apartmenttype='006' and status = 'ACTIVE'
union
select 'Commercial',COUNT(*) from register where apartmenttype='007' and status = 'ACTIVE'
union
select 'Network Mast',COUNT(*) from register where apartmenttype='008' and status = 'ACTIVE';
'''