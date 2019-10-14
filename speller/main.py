# main.py
#Adapted from https://github.com/PrettyPrinted/flask_auth_scotch

from flask import Blueprint, render_template, redirect,request,flash,url_for
from flask_login import login_required, current_user
import random
from .sanitize import sanitize
import os
import subprocess

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
     f = open("./speller/"+temp+".txt","w+")
     f.write(text)
     f.close()
     #check words
     cmd = "./speller/a.out "+f.name+" ./speller/wordlist.txt"
     #run file through spell checker c program
     checkedtext = subprocess.check_output(cmd, shell=True)
     #decode to string from bytes
     checkedtext = checkedtext.decode('ascii')
     #delete file to prevent resource depletion attacks
     os.remove(f.name)
     return render_template('spellcheckpost.html',inputtext=text,outtext=checkedtext)