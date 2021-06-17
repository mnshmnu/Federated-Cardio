from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "This is a secret key!! SShhhh...."

db = {1122334455:{'name':'Rashi M','id':1122334455,'date':'10/06/2021','anomaly':'Murmur','remarks':'Take medication.','Medications':[{'name':'Med 1','Amount':'25g','DpD':'2'},{'name':'Med 2','Amount':'10g','DpD':'3'}]},1122334456:{'name':'Maneesh Manoj','id':256,'date':'10/06/2021','anomaly':'Abnormal','remarks':'Take medication.','Medications':[{'name':'Med 1','Amount':'10g','DpD':'2'}]}}

@app.route('/')
def home():
    return render_template('index1.html', pred = None)


# request eg = URL/api/login?id=1122334455&date=10/06/2021

@app.route('/api/login',methods=['GET'])
def api_login():
    response = {}
    if ('id' in request.args and 'date' in request.args):
        if(int(request.args['id']) in db.keys() and request.args['date'] == db[int(request.args['id'])]['date']):
            response = db[int(request.args['id'])]
        else:
            return 'Not Found.',404
    else:
        return "Invalid request.",403
    return jsonify(response)