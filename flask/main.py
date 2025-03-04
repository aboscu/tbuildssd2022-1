from flask import Blueprint,render_template, redirect,url_for, request, flash, Markup
from flask_login import  login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from . models import User
import os

main = Blueprint('main', __name__)

'''
# This should probably be moved to file view & download
def getclientpath(cid,arcid):
    if arcid == 14:
        clientpath = "/opt/balam/clients/{}/datamgmt/14".format(cid)
    elif arcid == 30:
        clientpath = "/opt/balam/clients/{}/datamgmt/30".format(cid)
    elif arcid == 90:
        clientpath = "/opt/balam/clients/{}/datamgmt/90".format(cid)
    else:
        clientpath = "/opt/balam/clients/{}/datamgmt/99".format(cid)
    return clientpath
'''

# This is the home page for the data users 
# This should test for valid login and if so we should present a second
# version of the page that shows they are loggged in with an account
# and display the groups that user is a member of, as well as the current
# session ID. (use this for valdiating )
# Login button set to logout
#  ----- extended capabilities ----------
# Also looking at messages of the day.  
# Possibly a way to monitor for state changes, explore threading library
# and cleary identify all the risks of rolling your own threading based app
# instead of using well developed solutions like an MQTT callback.

@main.route('/')
def index():
    print(current_user.is_authenticated)
    return render_template('index.html')

# If no valid session and access ID then redirect to login page.  Use
# Flask-login get_id method instead of writing something new. 
@main.route('/home')
@login_required
def presenthome():
    #print(current_user.is_authenticated)
    #if current_user.is_authenticated:
    sessioncid=current_user.get_id()
    account=User.query.filter_by(id=sessioncid).first()
    return render_template('home.html', scid=sessioncid,scname=account.clientname )
    
# File search and download, 
# Place holder page for now, just validate for login
# This will be the main page for interacting with files the user has access to
# Format will be a list of up to 6 files, radio button selection and three buttons
# They can select a file for download, (one at a time)
# They can select a file to be shared with others (one at a time, also used to remove sharing if user is owner)
# They can select a file to be deleted (one at a time, they must be owner)
@main.route('/fsd1')
@login_required
def presentfileview():
    #print(current_user.is_authenticated)
    #if current_user.is_authenticated:
    #sessioncid=current_user.get_id()
    #account=User.query.filter_by(id=sessioncid).first()
    return render_template('fileview.html')
    #return render_template('fileview.html', scid=sessioncid,scname=account.clientname )
    

# File upload 
# Place holder page for now, just validate for login
# Possible IDS monitoring option, insider threat exploring the app once authenticated.
# Queries for active pages that don't end with a known valid number would generate 404 events
# Attacker would have no idea which ones were valid and we could also create a honeypot page
# that can only be accessed via indirect reference.
# replies with a 200, captures attacker data and triggers an alert, while presenting an old help page
@main.route('/flup7')
@login_required
def presentupload():
    return render_template('fileup.html')

@main.route('/flup2')
@login_required
def proccessupload():
    return render_template('fileupresp.html')


# File Share

@main.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    clientid = request.form.get('clientid')
    password = request.form.get('password')
    account= User.query.filter_by(email=email).first()
    if account:
        flash('Sorry, the email address {} appears to be in use'.format(email))
        return redirect(url_for('auth.register'))
    account= User.query.filter_by(id=clientid).first()
    if not account:
        msg=Markup('Sorry, the account identifier does not appear to preregistered, double check you have input the 5 digit code correctly.<br/> If you are still encountering issues please contact Balam customer support: <br/> 1-888-BALAM27 (1-888-225-2627)')
        flash(msg)
        return redirect(url_for('auth.register'))
        #return '<h1> Sorry, the account identifier does not appear to preregistered, double check you have input the 6 digit code correctly</h1><h2>If you are still encountering issues please contact Balam customer support at 1-888-BALAM27 (1-888-225-2627)</h2>'
    if account.email:
        msg=Markup('Sorry, the account identifier {} is currently associated with the email {}'.format(account.id, account.email))
        flash(msg)
        return redirect(url_for('auth.register'))
        #return '<h1> Sorry, the account identifier {} is currently associated with the email {}</h1>'.format(account.id, account.email)
    else:
        # Do the SQL update here
        pwdstr = generate_password_hash(password)
        account.email= email
        account.pwd = pwdstr 
        db.session.commit()
        #User.query.filter_by(id=clientid).update(dict(email=email,pwd=pwdstr))
        return render_template('signup.html',id=clientid,email=email,clientname=account.clientname)
        #return '<h1> Input cid: {}, email: {}, pwd: {} for company {}'.format(clientid,email,password,account.clientname)

#@main.route('/data-access')
#@login_required
#def dm14():
#    sessioncid=current_user.get_id()
#    account=User.query.filter_by(id=sessioncid).first()
#    # list directory content to make URLs
#    cpath = getclientpath(sessioncid,14)
#    files=os.listdir(cpath)
#    urllist=[]
#    for file in files:
#        url="https://datahub.balam.ca/{}/dm14/{}".format(sessioncid,file)
#        urllist.append(url)
#    # To do, get second list of file names to make things prettier on the other end
#    return render_template('dataaccess.html', scid=sessioncid,scname=account.clientname,filelinklist=urllist)