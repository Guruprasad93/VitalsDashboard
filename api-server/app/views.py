#!usr/bin/python

from app import app, db, models
#from flask import Flask
from flask import jsonify, request, render_template
import smtplib, subprocess, json, datetime
from models import SWJsonify, User, Post, Device, Vital, SOS, Notification, NotificationContact
#app = Flask(__name__)
import json

def send_email(text):
    gmail_user = "pcsvitals@gmail.com"
    gmail_pwd = "slativscp"
    FROM = 'pcsvitals@gmail.com'
    TO = ['sharvil2009@gmail.com']
    SUBJECT = "Health vital information"
    TEXT = text

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent'
    except:
        print 'Failed to send!'



def ruleEngine(vitals_data, device_id):
    #checking HR threshold
    print "inside rule engine"
    #print vitals_data['HR'] 
    
    if int(vitals_data['HR'])>70 and int(vitals_data['HR'])<140: 
        print "You're fine"
    else:
        print "Sending notification via Email and Text"
        text = "Unusual Health vitals!"
        send_email(text)

        #Notification object
        notif_obj = Notification(device_id, text, 'email')
        db.session.add(notif_obj)
        db.session.commit()
        #bashCommand = "curl -X POST http://textbelt.com/intl -d number=971507646637 -d 'message=Api-called-Testing' "
        #subprocess.Popen(bashCommand)
    

@app.route("/")
def hello():
    return render_template('layoutDash.html')
    #return "Hello World"


@app.route("/index")
def index():
    sos = SOS.query.all()
    sos_userid = []
    for sosObj in sos:
        sos_userid.append(sosObj.user_id)

    #print sos
    notifs = Notification.query.all()
    users = User.query.all()
    notifs = notifs[::-1]
    id_notif = []
    for notif in notifs:
        id_notif.append(notif.user_id)
        print datetime.datetime.now() - notif.timestamp
    unique_Users = len(set(id_notif))
    size_SOS = len(sos)
    size_notif = len(notifs)
    return render_template('index.html', sos_Trigger=size_SOS, SOS=sos, SOS_users= list(set(sos_userid)), notif_len = size_notif, user_danger = unique_Users, notifs = notifs[0:7], users=users, token=0)
    #return "My name is guru"

@app.route("/api/<device_id>/vitals", methods= ['POST'])
def postVitals(device_id):
    #print request.method, request.headers
    print "Device id =  ", device_id

    if request.headers['Content-Type'] == 'application/json':
        #print "posted some data"
        json_dict=request.get_json() 
        print json_dict.keys(), json_dict.values()
        [HR, bloodoxy, temp_body, temp_env, baro] = map(lambda x: float(x), json_dict.values())

        ruleEngine(json_dict, device_id) 

        #Make into Vital Object
        vit_obj = Vital(device_id, temp_body, temp_env, HR, bloodoxy, baro)
        db.session.add(vit_obj)
        db.session.commit()


        #print json_dict['message']
        #return "Received JSON Message: " + jsonify(**request.json)
       
        return "JSON Message" + json.dumps(json_dict)

@app.route("/api/<device_id>/SOS", methods= ['POST'])
def SOS_Trigger(device_id):
    if request.headers['Content-Type'] == 'text/plain':
        text = "SOS Trigger activated!"
        send_email(text)

        #making object to store in SOS table
        sos_obj = SOS(device_id, text)
        db.session.add(sos_obj)
        db.session.commit()

        notif_obj = Notification(device_id, text, 'email')
        db.session.add(notif_obj)
        db.session.commit()


        data_recd = request.data
        print data_recd
        return data_recd

@app.route("/api/dashboard", methods= ['GET'])
def dashboard():
    users = User.query.all()    
    usersJSON=SWJsonify({'users':users })
    sos = SOS.query.all()
    sosJSON = SWJsonify({'sos':sos })
    return render_template("dashboard.html", usersJSON = json.loads(usersJSON), sosJSON = json.loads(sosJSON))


@app.route("/api/users")
def usersList():
    users = User.query.all()
    usersJSON=SWJsonify({'users':users })
    return render_template("users-list.html", usersJSON = json.loads(usersJSON))

@app.route("/api/<user_id>/vitals")
def userVitals(user_id):
    user = User.query.get(user_id)
    vitals = user.vitals.all()
    vitalsJSON = SWJsonify({'vitals':vitals })
    sos = SOS.query.all()
    notifs = Notification.query.all()
    users = User.query.all()
    notifs = notifs[::-1]
    id_notif = []
    sos_userid = []
    for sosObj in sos:
        sos_userid.append(sosObj.user_id)

    for notif in notifs:
        id_notif.append(notif.user_id)
        print datetime.datetime.now() - notif.timestamp
    unique_Users = len(set(id_notif))
    size_SOS = len(sos)
    size_notif = len(notifs)

   #return  render_template('flot.html', vitalsJSON = json.loads(vitalsJSON), user=user, token=1)
    return  render_template('index.html', vitalsJSON = json.loads(vitalsJSON), SOS_users=list(set(sos_userid)), user=user, sos_Trigger=size_SOS, notif_len = size_notif, user_danger = unique_Users, notifs = notifs[0:5], users=users, token=1)
    #return render_template("user-vitals.html", vitalsJSON = json.loads(vitalsJSON),name=user.nickname)

@app.route("/api/sos")
def sostxt():
    print request
    sos = SOS.query.all()
    return SWJsonify({'sos':sos })    


@app.route("/Trial", methods= ['GET', 'POST'])
def Trial():
    
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            json_dict = request.get_json()

    
            return render_template("index.html", messages=json.dumps(json_dict))
    else:
        # v = Vital.query.get(1)
        # dict_vital = v.__dict__
        # print dict_vital
        # del dict_vital['_sa_instance_state']
        # dict_vital['timestamp'] = str(dict_vital['timestamp'])



        # return json.dumps(dict_vital)
        vitals = Vital.query.all()
        sos = SOS.query.all()
        return render_template('flot.html')
        #return json.loads(SWJsonify({'vitals':vitals }))

if __name__ == '__main__':
    app.debug= True
    app.run()
