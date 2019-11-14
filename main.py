# main.py
#Adapted from https://github.com/PrettyPrinted/flask_auth_scotch

from flask import Blueprint, render_template, redirect,request,flash,url_for
from flask_login import login_required, current_user
import random
from sanitize import sanitize
from app import db
from models import History, Logins
import os
import subprocess
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
     return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
   return render_template('profile.html', name=current_user.name, phone=current_user.phone)

@main.route('/spell_check',methods=['GET'])
@login_required
def spell_check():
     return render_template('spellcheck.html')

@main.route('/spell_check',methods=['POST'])
@login_required
def spell_check_post():
     text = request.form['inputtext']
     text = sanitize(text)
     x = [random.randint(0,9) for y in range (0,10)]
     temp = ''.join(map(str,x))
     f = open("./"+temp+".txt","w+")
     f.write(text)
     f.close()
     #check words
     cmd = "./a.out "+f.name+" ./wordlist.txt"
     #run file through spell checker c program
     checkedtext = subprocess.check_output(cmd, shell=True)
     #decode to string from bytes
     checkedtext = checkedtext.decode('ascii')
     checkedtext = checkedtext.replace("\n",",")
     #delete file to prevent resource depletion attacks
     os.remove(f.name)
     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     logquery = History(submit_text=text, returned_text=checkedtext, submit_user=current_user.email, timestamp=current_time)
     db.session.add(logquery)
     db.session.commit()
     return render_template('spellcheckpost.html',inputtext=text,outtext=checkedtext)

@main.route('/history',methods=['GET'])
@login_required
def query_history():
     if (current_user.email == "admin"):
          return render_template('adminhistory.html')

     history = History.query.filter_by(submit_user=current_user.email).all()
     return render_template('history.html',value = history, querycount = len(history))

@main.route('/history',methods=['POST'])
@login_required
def admin_history():
     user = request.form['userquery']
     history = History.query.filter_by(submit_user=user).all()
     return render_template('history.html',value = history, querycount = len(history))

@main.route('/history/<int:query>',methods=['GET'])
@login_required
def query_lookup(query):
     if (current_user.email == "admin"):
          querydata = History.query.filter_by(query_id=query).first()
          return render_template('querydetails.html', value = querydata)
     querydata = History.query.filter_by(query_id=query,submit_user=current_user.email).first()
     return render_template('querydetails.html', value = querydata)


@main.route('/login_history',methods=['GET'])
@login_required
def login_history():
     if (current_user.email == "admin"):
          return render_template('adminlogin.html')
     logins = Logins.query.filter_by(user_id=current_user.email).all()
     return render_template('loginhistory.html',value = logins)

@main.route('/login_history',methods=['POST'])
@login_required
def admin_login():
     user = request.form['userquery']
     logins = Logins.query.filter_by(user_id=user).all()
     return render_template('loginhistory.html',value = logins)

if __name__ == '__main__':
     main.run()
