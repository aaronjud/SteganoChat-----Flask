from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
import os
import base64
import cv2
import numpy as np
import os
from main import encode,decode
import random
import sys
from datetime import date


secret_key = os.urandom(24)
app = Flask(__name__)
app.secret_key = secret_key

database="final1.db"

def createtable():
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("create table if not exists register (id integer primary key autoincrement, name text, userid text,phone text, password text)")
    cursor.execute("create table if not exists encrypt(id integer primary key autoincrement, reciver_name text, sender_name text,sender_userid text,sender_phone text, filename,imagefile1 blob)")
    conn.commit()
    conn.close()
createtable()



@app.route('/')
@app.route('/index',methods=["GET","POST"])
def index():
        return render_template('login.html')



    
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
         name=request.form['name']
         userid=request.form['userid']
         phone=request.form['phone']
         v1=str(phone)
         if len(v1)!=10:
            return display_popup1(" please enter a valid mobile number ")
         password=request.form['password']
         confirm_pass= request.form['confirm_pass']
         if password != confirm_pass:
            return display_popup1(" sorry your password does not match")
         con=sqlite3.connect(database)
         cur=con.cursor()
         cur.execute("SELECT userid FROM register WHERE userid=?", (userid,))
         registered = cur.fetchall()
         if registered:
            return display_popup1 (" your userid already registered")
         else:   
             cur.execute("insert into register(name, userid, phone, password  )values(?,?,?,?)",(name, userid, phone, password))
             con.commit()
             return render_template('login.html')
    return render_template('login.html')




log=[]
file=[]
@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method=="POST":
        userid=request.form['userid']
        password=request.form['password']
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute("select * from register where userid=? and password=?",(userid,password))
        data=cur.fetchone()
        if data is None:
                return "Password Mismatch"        
        else:  
            log.append(userid)
            con=sqlite3.connect(database)
            cur=con.cursor()
            userid=log[-1]
            cur.execute("select *from register where userid=?",(userid,))
            results = cur.fetchone()
            cur.execute("select * from encrypt  where reciver_name=?",(userid,))
            results1 = cur.fetchall()
            count=len(results1)
            con.commit()
            return render_template('data.html',name=results[1],userid=results[2],phone=results[3],count=count)
    return render_template('login.html')



@app.route('/data', methods=["GET","POST"])
def data():
    con=sqlite3.connect(database)
    cur=con.cursor()
    userid=log[-1]
    cur.execute("select *from register where userid=?",(userid,))
    results = cur.fetchone()
    return render_template('data.html',name=results[1],userid=results[2],phone=results[3])



@app.route('/input', methods=["GET","POST"])
def input():
    #if system:
        if request.method=="POST":
                data = request.form['data']
                image_file = request.files['image']
                filename = image_file.filename
                upload_folder = os.path.join(os.getcwd(), 'uploads')  
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file_path = os.path.join(upload_folder, 'encode.png')
                image_file.save(file_path)
                otp = "".join(random.choice('0123456789') for _ in range(6))
                filename= f"{otp}.png"
                file.append(filename)
                img=encode(data,filename)
                con=sqlite3.connect(database)
                cur=con.cursor()
                cur.execute("select id,name,userid,phone from register")
                results = cur.fetchall()
                con.commit()
                return render_template('register_details.html', results=results)
        return render_template('input.html')


@app.route('/register_details', methods=["GET","POST"])
def register_details():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("select id,name,userid,phone from register")
    results = cur.fetchall()
    con.commit()
    return render_template('register_details.html', results=results)


@app.route('/send', methods=["GET","POST"])
def send():
    if request.method == "POST":
            userid = request.form['number']
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute('SELECT userid FROM register WHERE  userid= ?', (userid ,))
            send_data = cursor.fetchone()
            userid1=log[-1]
            cursor.execute('SELECT name,userid,phone FROM register WHERE  userid= ?', (userid1 ,))
            send_data1 = cursor.fetchone()
            folder_path = 'uploads/encode.png'
            with open(folder_path, 'rb') as image_file:
                image_data = image_file.read()
            reciver_name=send_data[0]
            sender_name=send_data1[0]
            sender_userid=send_data1[1]
            sender_phone=send_data1[2]
            filename=file[-1]
            #imagefile1=image_data
            cursor.execute("INSERT INTO encrypt (reciver_name, sender_name, sender_userid, sender_phone,filename, imagefile1) VALUES (?,?, ?, ?, ?, ?)", (reciver_name, sender_name, sender_userid, sender_phone, filename,image_data))
            conn.commit()
    return render_template("data.html")

@app.template_filter('b64encode')
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')

@app.route('/receive', methods=["GET","POST"])
def receive():
    con=sqlite3.connect(database)
    cur=con.cursor()
    userid2=log[-1]
    cur.execute("select * from encrypt WHERE reciver_name=?",(userid2 ,))
    results = cur.fetchall()
    con.commit()
    return render_template('receive.html', results=results)


@app.route('/decrypt', methods=["GET","POST"])
def decrypt():
            Id = request.form['number']
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute('SELECT filename FROM encrypt WHERE  id= ?', (Id ,))
            filename  = cursor.fetchone()
            file=(filename[0])
            result=decode(file)
            return render_template('result.html', result=result)
 

















def display_popup1(message):
    flash(message)
    return redirect(url_for('register'))
if __name__=="__main__":
    app.run(debug=False,port=600,)
