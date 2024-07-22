from flask import *
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import yaml
import json
from yaml.loader import SafeLoader
import pandas as pd
from datetime import datetime, date
import os
import logging

app = Flask(__name__)
# setup logging 
logger =logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelno)s,%(filename)s,%(funcName)s,%(message)s')
# file_handler = logging.FileHandler('/home/ubuntu/SMS/test.log')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app.secret_key = "secret key"

db = yaml.load(open('db.yaml'), Loader=SafeLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)
# print(mysql)


today=date.today()

# home page
@app.route('/', methods=['GET', 'post'])
def home():
    msg=[]
    if request.method=='POST':
        cursor = mysql.connection.cursor()
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        comment=request.form['comment']
        result=cursor.execute("INSERT INTO `enquiry1` ( `name`, `phone`, `email`, `comment`, `status`, `dateCreated`) VALUES (%s, %s, %s, %s, 'active', current_timestamp());",(name,phone,email,comment))
        if result:
            mysql.connection.commit()
            msg.append('Success')
            msg.append('Your details has been submitted successfully')

    return render_template('index.html', msg=msg)



@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        uname=request.form['username']
        email=request.form['email']
        password=request.form['password']
        company=request.form['company']
        sql=cursor.execute('select * from company where username=%s',(uname,))
        if sql:
            return render_template('auth-signup.html', msg="username already exist")
        else:
            sql=cursor.execute("INSERT INTO `company` (`username`, `password`, `Name`, `contact`, `status`, `datetime`) VALUES (%s, %s, %s, %s, 'active', current_timestamp())",(uname,password,company,email))
            if sql:
                mysql.connection.commit()
                sql=cursor.execute('select * from company where username=%s',(uname,))
                user=cursor.fetchone()
                session['serial_No']= user[0]
                session['type'] = 'company' 
                return redirect(url_for('dashboard'))
            else:
                return render_template('auth-signup.html',msg="incorrect information unable to signup")

    return render_template('auth-signup.html', msg="")

@app.route('/signin', methods=['GET','POST'])
def signin():
    if 'serial_No' in session:
        return redirect(url_for('dashboard'))
    else:
        msg=''
        if request.method == 'POST':
            cursor=mysql.connection.cursor()
            name=request.form['username']
            password=request.form['password']
            ty=request.form['type']
            print('hello')
            if ty=='company':
                sql=cursor.execute('select * from company where username=%s',(name,))
            else:
                sql=cursor.execute('Select * from employee where username=%s',(name,))
            if sql:
                res=cursor.fetchone()
                if password == res[2]:
                    session['serial_No']=res[0]
                    session['type']=ty
                    print('hello')
                    return redirect(url_for('dashboard'))
                else:
                    msg='Password do not match'
            else:
                msg='no user exist'


        return render_template('auth-signin.html', msg=msg)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'serial_No' in session:
        cursor=mysql.connection.cursor()
        if session['type'] == 'company':
            sql=cursor.execute('select * from company where sno=%s',(session['serial_No'],))
            res=cursor.fetchone() 
        else:                                                                                                                                                    
            sql=cursor.execute('select * from employee where sno=%s',(session['serial_No'],))
            res=cursor.fetchone()                                                                                                                                                     
        return render_template('dashboard.html', data=res)
    else:
        return redirect(url_for('signin'))

@app.route('/add-employee', methods=['GET','POST'])
def add_employee():
    if 'serial_No' in session:
        if request.method=='POST':
            cursor=mysql.connection.cursor()
            name=request.form['name']
            email=request.form['email']
            gender=request.form['Gender']
            dob=request.form['dob']
            password=request.form['password']
            designation=request.form['designation']
            uname=name.split()[0]+'111'
            sql=cursor.execute("INSERT INTO `employee` (`username`, `password`, `name`, `companyID`, `dob`, `gender`, `profile`, `email`, `status`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active', current_timestamp())",
            (uname,password,name,session['serial_No'],dob,gender,designation,email,))
            if sql:
                msg="employee added successfully"
                mysql.connection.commit()
                return redirect('/view-employee')
            else:
                msg="error in adding employee"
        return render_template('add_employee.html')

    else:
        return redirect('/signin')


@app.route('/view-employee', methods=['GET','POST'])
def view_employee():
    if 'serial_No' in session:
        cursor=mysql.connection.cursor()
        result=[]
        sql=cursor.execute("select * from employee where companyID=%s",(session['serial_No'],))
        if sql:
            result=cursor.fetchall()
        return render_template('view_employee.html',data=result)
    else:
        return redirect('/signin')

@app.route('/payroll-management', methods=['GET','POST'])
def payroll():
    if 'serial_No' in session:
        if request.method == 'POST':
            cursor=mysql.connection.cursor()
            desig=['fresher','assistant software engineer','software engineer','project manager','manager']
            for i in range(1,6):
                basic=request.form['ba'+str(i)]
                hr=request.form['hr'+str(i)]
                food=request.form['f'+str(i)]
                overtime=request.form['bo'+str(i)]
                pf=request.form['pf'+str(i)]
                sql=cursor.execute('select * from salary where companyID=%s and designation=%s',(session['serial_No'],desig[i-1],))
                if sql:
                    result=cursor.fetchone()
                    sql=cursor.execute("UPDATE `salary` SET `hra` = %s, basic_pay=%s,food=%s,overtime=%s,pf=%s WHERE `salary`.`sno` = %s;",(hr,basic,food,overtime,pf,result[0],))
                else:
                    sql=cursor.execute("INSERT INTO `salary` (`companyID`, `designation`, `basic_pay`, `hra`, `food`, `overtime`, `pf`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s, %s, current_timestamp())",
                    (session['serial_No'],desig[i-1],basic,hr,food,overtime,pf,))
                if sql:
                    mysql.connection.commit()
            return redirect('/show-payroll')
        return render_template('salary-manage.html')
    else:
        return redirect('/dashboard')

@app.route('/show-payroll')
def show_payroll():
    if 'serial_No' in session:
        result=[]
        cursor=mysql.connection.cursor()
        sql=cursor.execute('select * from salary where companyID=%s',(session['serial_No'],))
        if sql:
            result=cursor.fetchall()
        return render_template('show_payroll.html', data=result)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('serial_No',None)
    session.pop('type',None)
    session.pop('admin',None)
    session.clear()
    return redirect("/")


#  running server at 8000 port 
if __name__ == "__main__":
    app.run(debug=True, port=8000)