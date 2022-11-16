#Team ID	: PNT2022PMID49597
#Project Name	: PLASMA DONOR APPLICATION
#Name	: SUSWIN P
#Roll Number	: 950019104049

from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app =Flask(__name__)

app.secret_key='a'

conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;USERNAME=zxd72229;PASSWORD=XEdSEnZ2jpYUndqg;SECURITY=SSL;SSLSERVERCERTIFICATE=DigiCertGlobalRootCA.crt;","","")

@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template("wel.html")

@app.route("/register-donor",methods=['GET', 'POST'])
def register_donor():
    msg=''
    if request.method=='POST':
        Fullname =request.form['Fullname']
        password =request.form['password']
        email =request.form['email']
        DOB = request.form['DOB']
        Gender = request.form['Gender']
        BloodGroup = request.form['BloodGroup']
        State = request.form['State']
        Pin = request.form['Pin']
        phone = request.form['phone']
        Issues = request.form['Issues']
        sql="SELECT * FROM samp WHERE fullname =?"
        stmt= ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1, Fullname)
        ibm_db.execute(stmt)
        account =ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', Fullname):
            msg='name must contain only characters and numbers !'
        else:
            insert_sql="INSERT INTO  samp VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,Fullname)
            ibm_db.bind_param(prep_stmt,2,password)
            ibm_db.bind_param(prep_stmt,3,email)
            ibm_db.bind_param(prep_stmt,4,DOB )
            ibm_db.bind_param(prep_stmt,5,Gender)
            ibm_db.bind_param(prep_stmt,6,BloodGroup)
            ibm_db.bind_param(prep_stmt,7,State)
            ibm_db.bind_param(prep_stmt,8,Pin)
            ibm_db.bind_param(prep_stmt,9,phone)
            ibm_db.bind_param(prep_stmt,10,Issues)
            ibm_db.execute(prep_stmt)
            msg='You have successfully registered !'
    elif request.method=='POST':
        msg='Please fill out the form !'
    return render_template('reg1.html',msg=msg)

@app.route("/login",methods=['GET', 'POST'])
def login_donor():
    global userid
    msg=''

    if request.method=='POST':
        email =request.form['email']
        password =request.form['password']
        sql="SELECT * FROM samp WHERE email =? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1, email)
        ibm_db.bind_param(stmt,2, password)
        ibm_db.execute(stmt)
        account =ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] =True
            session['id'] = account['EMAIL']
            userid= account['EMAIL']
            session['email'] = account['EMAIL']
            msg='Logged in successfully !'

            msg='Logged in successfully !'
            return render_template('home.html',msg=msg)
        else:
            msg='Incorrect username / password !'
    return render_template('login1.html',msg=msg)

if __name__ =='__main__':
    #app.run(host='0.0.0.0')
    app.run(debug=True)
