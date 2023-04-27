from flask import Flask,flash,redirect,request,url_for,render_template,session,send_file
from flask_session import Session
from flask_mysqldb import MySQL
from otp import genotp
from cmail import sendmail
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tokenreset import token
from io import BytesIO
app=Flask(__name__)
app.secret_key='anisha@2003'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='pms'
Session(app)
mysql=MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/registration',methods=['GET','POST'])
def register():
    cursor=mysql.connection.cursor()
    cursor.execute('select count(*) from admin')
    count=cursor.fetchone()[0]
    cursor.close()
    if (count>=0):
        return 'admin already registered'
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select name from admin')
        data=cursor.fetchall()
        cursor.execute('SELECT email from admin')
        edata=cursor.fetchall()            
        if (email,) in edata:
            flash('Email id already exists')
            return render_template('register.html')
        cursor.close()
        otp=genotp()
        sendmail(email,otp)
        return render_template('otp.html',otp=otp,name=name,password=password,email=email)
    else:
        return render_template('register.html')
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.form)
        name=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where name=%s and password=%s',[name,password])
        count=cursor.fetchone()[0]
        if count==0:
            print(count)
            flash('Invalid username or password')
            return render_template('login.html')
        else:
            session['user']=name
            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/home')
def home():
    if session.get('user'):
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
@app.route('/forgetpassword',methods=['GET','POST'])
def forget():
    if request.method=='POST':
        name=request.form['name']
        cursor=mysql.connection.cursor()
        cursor.execute('select name from admin')
        data=cursor.fetchall()
        cursor.close()
        if (name,) in data:
            cursor=mysql.connection.cursor()
            cursor.execute('select email from admin where name=%s',[name])
            data=cursor.fetchone()[0]
            cursor.close()
            subject=f'Reset Password for {data}'
            body=f'Reset the passwword using-{request.host+url_for("createpassword",token=token(name,360))}'
            sendmail(data,subject,body)
            flash('Reset link sent to your mail')
            return redirect(url_for('login'))
        else:
            return 'Invalid user name'
    return render_template('forgot.html')
@app.route('/createpassword/<token>',methods=['GET','POST'])
def createpassword(token):
    try:
        s=Serializer(app.config['SECRET_KEY'])
        name=s.loads(token)['user']
        if request.method=='POST':
            npass=request.form['npassword']
            cpass=request.form['cpassword']
            if npass==cpass:
                cursor=mysql.connection.cursor()
                cursor.execute('update admin set password=%s where name=%s',[npass,name])
                mysql.connection.commit()
                return 'Password reset Successfull'
            else:
                return 'Password mismatch'
        return render_template('newpassword.html')
    except Exception as e:
        print(e)
        return 'Link expired try again'
@app.route('/otp/<otp>/<name>/<password>/<email>',methods=['GET','POST'])
def otp(otp,name,password,email):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mysql.connection.cursor()
            lst=[name,password,email]
            query='insert into admin values(%s,%s,%s)'
            cursor.execute(query,lst)
            mysql.connection.commit()
            cursor.close()
            flash('Details Registered')
            return redirect(url_for('login'))
        else:
            flash('Wrong OTP')
            return render_template('otp.html',otp=otp,name=name,password=password,email=email)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    else:
        flash('already logged out')        
        return redirect(url_for('login'))
    
@app.route('/patientshome')
def patientshome():
    if session.get('user'):
        patientname=session.get('user')
        cursor=mysql.connection.cursor()
        cursor.execute('select * from patients')
        patients_data=cursor.fetchall()
        print(patients_data)
        cursor.close()
        return render_template('addpatienttable.html',data=patients_data)
    else:
        return redirect(url_for('login'))
@app.route('/addpatient',methods=['GET','POST'])
def addpatient():
    if session.get('user'):
        if request.method=='POST':
            patientname=request.form['patientname']
            mobileno=request.form['mobileno']
            age=request.form['age']
            address=request.form['address']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into patients(patientname,mobileno,age,address)values(%s,%s,%s,%s)',[patientname,mobileno,age,address])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('patientshome'))
        return render_template('patients.html')
    else:
        return redirect(url_for('login'))

@app.route('/updatepatients/<mobileno>',methods=['GET','POST'])
def updatepatients(mobileno):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select patientname,mobileno,age,address from patients where mobileno=%s',[mobileno])
        data=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
            patientname=request.form['patientname']
            mobileno=request.form['mobileno']
            age=request.form['age']
            address=request.form['address']
            cursor=mysql.connection.cursor()
            cursor.execute('update patients set patientname=%s,mobileno=%s,age=%s,address=%s where mobileno=%s',[patientname,mobileno,age,address,mobileno])
            mysql.connection.commit()
            cursor.close()
            flash('Patients updated successfully')
            return redirect(url_for('patientshome'))
        return render_template('updatepatients.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/deletepatients/<mobileno>')
def deletepatients(mobileno):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from patients where mobileno=%s',[mobileno])
    mysql.connection.commit()
    cursor.close()
    flash(' Patients deleted successfully')
    return redirect(url_for('patientshome'))
@app.route('/patientsrecordshome')
def patientsrecordshome():
    if session.get('user'):
        name=session.get('user')
        cursor=mysql.connection.cursor()
        cursor.execute('select * from records')
        records_data=cursor.fetchall()
        print(records_data)
        cursor.close()
        return render_template('patientsrecordstable.html',data=records_data)
    else:
        return redirect(url_for('login'))
@app.route('/patientsrecords',methods=['GET','POST'])
def patientsrecords():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT mobileno from patients')
        data=cursor.fetchall()
        mobile=request.args.get('name') if request.args.get('name') else None
        cursor.execute('SELECT mobileno,patientname from patients where mobileno=%s',[mobile])
        details=cursor.fetchone()
        print(details)
        cursor=mysql.connection.cursor()
        cursor.execute('select * from records')
        records=cursor.fetchall()
        cursor.close()
        if request.method=='POST':
            mobileno = request.form['mobileno']
            name = request.form['name']
            print(name)
            print(mobile)
            if mobileno =='' or name=='':
                flash('Submit patient mobileno first')  
                return render_template('patientsrecords.html',data=data,details=details,records=records)
            cursor=mysql.connection.cursor()
            cursor.execute('insert into records(name,mobileno)values(%s,%s)',[name,mobileno])
            mysql.connection.commit()
            cursor.close()
            flash('Record added successfully')
            return redirect(url_for('patientsrecords'))
        return render_template('patientsrecords.html',data=data,details=details,records=records)
    else:
        return redirect(url_for('login'))

@app.route('/doctorhome/<id1>',methods=['GET','POST'])
def doctorhome(id1):
    if session.get('user'):
        if request.method=='POST':
            doctorname=request.form['doctorname']
            purposetovisit=request.form['purposetovisit']
            appointmenttime=request.form['appointmenttime']
            cursor=mysql.connection.cursor()
            cursor.execute('update records set doctorname=%s,purposetovisit=%s,appointmenttime=%s where rid=%s',[doctorname,purposetovisit,appointmenttime,id1])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('patientsrecords'))
        return render_template('doctor.html')
    else:
        return redirect(url_for('login'))
 
@app.route('/testhome')
def testhome():
    if session.get('user'):
        testname=session.get('user')
        cursor=mysql.connection.cursor()
        cursor.execute('select * from test')
        test_data=cursor.fetchall()
        print(test_data)
        cursor.close()
        return render_template('testview.html',data=test_data)
    else:
        return redirect(url_for('login'))
@app.route('/addtest',methods=['GET','POST'])
def addtest():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT mobileno from patients')
        data=cursor.fetchall()
        if request.method=='POST':
            mobileno=request.form['mobileno']
            testname=request.form['testname']
            testresult=request.form['testresult']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into test(mobileno,testname,testresult)values(%s,%s,%s)',[mobileno,testname,testresult])
            mysql.connection.commit()
            cursor.close()
            flash('test added successfully')
            return redirect(url_for('testhome'))
        return render_template('test.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/checkinupdate/<id1>')
def checkinupdate(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkin=now() where rid=%s',[id1])
    mysql.connection.commit()
    return redirect(url_for('patientsrecords'))
@app.route('/checkoutupdate/<id1>')
def checkoutupdate(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkout=now() where rid=%s',[id1])
    mysql.connection.commit()
    return redirect(url_for('patientsrecords'))

                    
    

@app.route('/updatetest/<mobileno>',methods=['GET','POST'])
def updatetest(mobileno):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select mobileno,testname,testresult from test where mobileno=%s',[mobileno])
        data=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
            mobileno=request.form['mobileno']
            testname=request.form['testname']
            testresult=request.form['testresult']
            cursor=mysql.connection.cursor()
            cursor.execute('update test set mobileno=%s,testname=%s,testresult=%s where mobileno=%s',[mobileno,testname,testresult,mobileno])
            mysql.connection.commit()
            cursor.close()
            flash('Test updated successfully')
            return redirect(url_for('testhome'))
        return render_template('updatetest.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/deletetest/<mobileno>')
def deletetest(mobileno):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from test where mobileno=%s',[mobileno])
    mysql.connection.commit()
    cursor.close()
    flash(' test deleted successfully')
    return redirect(url_for('testhome'))
    


app.run(debug=True,use_reloader=True,port='8000')
    
