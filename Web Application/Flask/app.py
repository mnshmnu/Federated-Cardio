
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
import sqlite3
import random
app = Flask(__name__)
app.secret_key = "This is a secret key!! SShhhh...."


def getPatientlist(did):
    plist=[]
    conn = sqlite3.connect('federatedhealth.db')
    cursor = conn.execute("SELECT pid, pname, age, gender, condition from patients WHERE did='{}'".format(did))
    for row in cursor:
        plist.append([row[0],row[1],row[2],row[3],row[4]])
    conn.close()
    if(len(plist)>0):
        return plist
    else:
        return None

def getPatientdetails(pid):
    conn = sqlite3.connect('federatedhealth.db')
    cursor = conn.execute("SELECT pname, age, gender, condition, cpercentage, strftime('%d/%m/%Y',dt), remarks from patients WHERE pid='{}'".format(pid))
    patient=cursor.fetchone()
    conn.close()
    if(patient):
        return {'pid':str(pid),'name':patient[0],'age':patient[1],'gender':patient[2],'condition':patient[3],'cpercentage':patient[4], 'date': patient[5], 'remark': patient[6]}
    else:
        return {'name':'','age':'','gender':'','condition':'','cpercentage':'','date':'','remark':''}

def getpremark(pid):
    conn = sqlite3.connect('federatedhealth.db')
    cursor = conn.execute("SELECT remarks from patients WHERE pid='{}'".format(pid))
    remark=cursor.fetchone()
    conn.close()
    if(remark):
        return remark[0]
    else:
        return None

def getmedicationlist(pid):
    mlist=[]
    conn = sqlite3.connect('federatedhealth.db')
    cursor = conn.execute("SELECT name, amount, dpd from prescription WHERE pid='{}'".format(pid))
    for row in cursor:
        mlist.append([row[0],row[1],row[2]])
    conn.close()
    if(len(mlist)>0):
        return mlist
    else:
        return None
    
def predict():
    cls=['Normal','Abnormal']
    percent = (random.randint(75,89)+(random.randint(1,99)/100))
    return random.choice(cls), percent


@app.route('/')
def home():
    if(session):
        return render_template('index.html',plist=getPatientlist(session['userid']))
    else:
        return render_template('login.html', userdetail=None, error=None)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(session):
        return render_template('index.html')
    if (request.method == 'POST'):
        if(request.form['uname']):
            conn = sqlite3.connect('federatedhealth.db')
            cursor = conn.execute("SELECT uID, uname, username, password from users WHERE username='{}'".format(request.form['uname']))
            user=cursor.fetchone()
            conn.close()
            if(user):
                if(user[3]==request.form['upassword']):
                    session['userid'] = user[0]
                    session['uname'] = user[1]
                    return render_template('index.html', plist=getPatientlist(session['userid']))
                else:
                    return render_template('login.html', userdetail=[request.form['uname'],request.form['upassword']], error="Incorrect Password.")
            else:
                return render_template('login.html', userdetail=[request.form['uname']], error="Username not found.")
        else:
            return render_template('login.html', userdetail=None, error="Please try again.")
    else:
        return render_template('login.html', userdetail=[request.form['uname']], error="Not post.")


@app.route('/viewpid')
def viewpid():
    pid = request.args.get("pid")
    if(pid):
        if(session):
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
        else:
            return render_template('login.html', userdetail=None, error=None)
    else:
        return render_template('index.html', plist=getPatientlist(session['userid']))

@app.route('/deletepid')
def deletepid():
    pid = request.args.get("pid")
    if(pid):
        if(session):
            conn = sqlite3.connect('federatedhealth.db')
            conn.execute("DELETE from patients where pid = {};".format(pid))
            conn.commit()
            conn.close()
            return render_template('index.html',plist=getPatientlist(session['userid']))
        else:
            return render_template('login.html', userdetail=None, error=None)
    else:
        return render_template('index.html', plist=getPatientlist(session['userid']))


@app.route('/updateremark', methods = ['GET', 'POST'])
def updateremark():
    pid=request.form['pid']
    if (request.method == 'POST'):
        if(request.form['remark']):
            conn = sqlite3.connect('federatedhealth.db')
            conn.execute("UPDATE patients set remarks = '{}' WHERE pid = {}".format(request.form['remark'],pid))
            conn.commit()
            conn.close()
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
        else:
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
    else:
        return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))


@app.route('/addmedication', methods = ['GET', 'POST'])
def addmedication():
    pid=request.form['pid']
    if (request.method == 'POST'):
        if(request.form['mname'] and request.form['amount'] and request.form['dpd']):
            conn = sqlite3.connect('federatedhealth.db')
            conn.execute("INSERT INTO prescription (pid,name,amount,dpd) VALUES ({},'{}',{},{})".format(pid,request.form['mname'],request.form['amount'],request.form['dpd']))
            conn.commit()
            conn.close()
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
        else:
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
    else:
        return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))


@app.route('/deletemed', methods = ['GET', 'POST'])
def deletemed():
    pid = request.args.get("pid")
    if(pid):
        if(session):
            conn = sqlite3.connect('federatedhealth.db')
            conn.execute("DELETE from prescription where pid = {} AND name = '{}' AND amount = {} AND dpd = {} ;".format(pid,request.args['name'],request.args['amount'],request.args['dpd']))
            conn.commit()
            conn.close()
            return render_template('patient.html',mlist=getmedicationlist(str(pid)),remarks=getpremark(str(pid)),pdetails=getPatientdetails(str(pid)))
        else:
            return render_template('login.html', userdetail=None, error=None)
    else:
        return render_template('index.html', plist=getPatientlist(session['userid']))


@app.route('/addpatient',methods = ['GET', 'POST'])
def addpatient():
    if (request.method == 'POST'):
        if(request.form['name'] and request.form['age'] and request.form['gender'] and request.form['Audio']):
            label,percent = predict()
            conn = sqlite3.connect('federatedhealth.db')
            conn.execute("INSERT INTO patients (pname,age,gender,condition,cpercentage,did,remarks) VALUES ('{}',{},'{}','{}',{},{},'')".format(request.form['name'],request.form['age'],request.form['gender'],label,percent,str(session['userid'])))
            conn.commit()
            conn.close()
            return render_template('index.html',plist=getPatientlist(session['userid']))
        else:
            return render_template('index.html',plist=getPatientlist(session['userid']))
    else:
        return render_template('index.html',plist=getPatientlist(session['userid']))


@app.route('/api/getprescription',methods=['GET'])
def get_prescription():
    response = {}
    if ('id' in request.args and 'date' in request.args):
        pDetails = getPatientdetails(str(request.args['id']))
        if(pDetails['pid']=='' or (pDetails['date'] != request.args['date'])):
            print(pDetails['date'],pDetails['pid'],request.args['date'])
            return "Invalid request..!",404
        response[int(request.args['id'])]=pDetails
        #{'pid':str(pid),'name':patient[0],'age':patient[1],'gender':patient[2],'condition':patient[3],'cpercentage':patient[4], 'date': patient[4], 'remark': patient[5]}
        response[int(request.args['id'])]['Medications']=[]
        mDetails=getmedicationlist(str(request.args['id']))
        if(mDetails):
            for m in mDetails:
                response[int(request.args['id'])]['Medications'].append({'name':str(m[0]),'Amount':str(m[1]),'DpD':str(m[2])})
        return jsonify(response[int(request.args['id'])])
    else:
        return "Invalid request.",403


@app.route('/logout')
def logout():
    session.pop('userid', None)
    session.pop('uname', None)
    return redirect(url_for('home'))


