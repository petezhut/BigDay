#!/usr/bin/python

from flask import Flask, request, render_template, url_for, redirect
from database import db_method
from datetime import *
import string
import backup

NAME = 'BigDay'
app = Flask(__name__)
app.debug = True

def daysUntil():
    today=date.today()
    # You will need to add your own special date here
    givenDate=date(2014,1,1)
    diff=today-givenDate
    return abs(diff.days)

@db_method
def insert(**kwargs):
    try:
        db = kwargs.pop('db')
        db.rsvp.insert(kwargs['data'])
    except:
        print("Didn't find one of the keys....")
    finally:
        backup.RSVPBackup()

@db_method
def checkRSVP(**kwargs):
    db = kwargs.pop('db')
    return bool(db.rsvp.find({
        'rsvp_fname' : kwargs['fname'],
        'rsvp_lname' : kwargs['lname']
        }).count())

@db_method
def getList(**kwargs):
    db = kwargs.pop('db')
    return db.rsvp.find()

@db_method
def DropDB(**kwargs):
    db = kwargs.pop('db')
    db.rsvp.drop()

@app.route("/list")
def list():
    ret = {} 
    attending = {}
    for count, data in enumerate(backup.getAttending()):
        rsvp_name = "%s %s" % (data['rsvp_fname'][0], data['rsvp_lname'][0])
        attending[rsvp_name] = []
        for a in range(int(data['count'][0])):
            ref = {}
            ref['guest_name'] = data['guest_%d_name' % (a)][0]
            ref['guest_meal'] = data['guest_%d_meal' % (a)][0]
            if data.has_key('guest_%d_age' % (a)):
                ref['guest_age'] = data['guest_%d_age' % (a)][0]
            attending[rsvp_name].append(ref)

    not_attending = []
    for data in backup.getAttending(attending = 'No'):
        not_attending.append("%s %s" % (data['rsvp_fname'][0], data['rsvp_lname'][0]))

    ret['not_attending'] = not_attending
    ret['attending'] = attending
    return render_template("list.html", title=NAME, daysleft=str(daysUntil()), data=ret)

# Uncomment this to empty the database.  
# Do not leave this enabled on a live site, bad things could happen
#@app.route("/clear")
#def clear():
#    DropDB()
#    return redirect(url_for('index'))

@app.route("/rsvp", methods=['GET', 'POST'])
def rsvp():
    if request.method == 'POST':
        name = "%s %s" % (request.form['rsvp_fname'], request.form['rsvp_lname'])
        if not checkRSVP(fname=request.form['rsvp_fname'], lname=request.form['rsvp_lname']):
            insert(data=dict(request.form))
            return render_template("thanks.html", daysleft=str(daysUntil()), title=NAME, rsvpdata = {'name': string.capwords(name), 'attending' : request.form['attending']})
        else:
            return render_template("problem.html", daysleft=str(daysUntil()), title=NAME, rsvpdata = {'name': string.capwords(name)})
    else:
        return render_template("form.html", title=NAME, daysleft=str(daysUntil()))

@app.route("/")
def index():
    return render_template("home.html", title=NAME, daysleft=str(daysUntil()))

if __name__ == '__main__':
    app.run(host="0.0.0.0")    
