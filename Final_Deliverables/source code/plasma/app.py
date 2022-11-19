from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
# from flask_mail import Mail, Message
import re

app = Flask(__name__)
# mail = Mail(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'psuswin00@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Su$i0410'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

app.secret_key='a'

conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;USERNAME=zxd72229;PASSWORD=XEdSEnZ2jpYUndqg;SECURITY=SSL;SSLSERVERCERTIFICATE=DigiCertGlobalRootCA.crt;","","")

@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template("wel.html")

@app.route("/",methods=['GET', 'POST'])
def home1():
    return render_template("home.html")

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

@app.route("/register-recipient",methods=['GET', 'POST'])
def register_recipient():
    msg=''
    if request.method=='POST':
        Name =request.form['Name']
        email =request.form['email']
        password =request.form['password']
        Address =request.form['Address']
        phone = request.form['phone']
        sql="SELECT * FROM recip WHERE name =?"
        stmt= ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1, Name)
        ibm_db.execute(stmt)
        account =ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', Name):
            msg='name must contain only characters and numbers !'
        else:
            insert_sql="INSERT INTO recip VALUES (?, ?, ?, ?, ?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,Name)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,Address)
            ibm_db.bind_param(prep_stmt,5,phone)
            ibm_db.execute(prep_stmt)
            msg='You have successfully registered !'
    elif request.method=='POST':
        msg='Please fill out the form !'
    return render_template('reg2.html',msg=msg)

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
            return render_template('home_donor.html',msg=msg)
        else:
            msg='Incorrect username / password !'
    return render_template('login1.html',msg=msg)
@app.route('/logout') 
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None) 
   return redirect(url_for('login_donor'))

@app.route("/login2",methods=['GET', 'POST'])
def login_recipient():
    global userid
    msg=''

    if request.method=='POST':
        email =request.form['email']
        password =request.form['password']
        sql="SELECT * FROM recip WHERE email =? AND password=?"
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
            return render_template('home_recipient.html',msg=msg)
        else:
            msg='Incorrect username / password !'
    return render_template('login2.html',msg=msg)



@app.route('/logout2') 
def logout2():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None) 
   return render_template('login2.html')

# @app.route('/send_email', methods = ['POST'])
# def send():     
#     if 'blood' in request.form:
#         type = request.form['blood']
#         stmt = ibm_db.prepare(conn, 'SELECT email FROM samp WHERE blood = ?')
#         ibm_db.bind_param(stmt,1,type)
#         ibm_db.execute(stmt)
#         tb = ibm_db.fetch_tuple(stmt)
#         mails = []
#         while tb != False:
#             mails.append(tb[0])
#             tb = ibm_db.fetch_tuple(stmt)

#         msg = Message('Blood Request', recipients=mails)
#         msg.body = "Here the " + request.form['blood'] + " Blood Requested"
#         mail.send(msg)
#         return render_template('display.html', state="SENT")

#     return 'Please Provide Blood in Form'

# @app.route('/display', methods =['GET', 'POST'])
# def display():
#     if 'id' in session:
#         if 'blood' in request.form:
#             type = request.form['blood']
#             stmt = ibm_db.prepare(conn, 'SELECT Fullname FROM samp WHERE blood = ?')
#             ibm_db.bind_param(stmt,1,type)
#             ibm_db.execute(stmt)
#             tb = ibm_db.fetch_tuple(stmt)
#             data = []
#             while tb != False:
#                 data.append(tb[0])
#                 tb = ibm_db.fetch_tuple(stmt)
        
#             return render_template('display.html', data=data, blood=request.form['blood'], state="NOTSENT")
#         return redirect('login2')
#     return 'Not Authed'    


if __name__ =='__main__':
    app.debug=True
    app.run(host='0.0.0.0')
    
