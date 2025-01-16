from flask import Flask, render_template, request, redirect, url_for
import random
import smtplib
import mysql.connector as ab
app = Flask(__name__)

# Stored value for comparison

a = ab.MySQLConnection(user="root",passwd="thar123",host="localhost",database="otp")
ab="Failed"
b=a.cursor()
@app.route("/", methods=["GET"])
def index():
    return render_template("web.html", stage=1)

@app.route("/otp", methods=["POST"])
def otp():
    global val
    global mail
    # Retrieve the name from the form
    mail = request.form.get("mail")
    print(mail)
    val = str(random.randint(100000,999999))

    senders="tharab1408@gmail.com"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(senders,"vbbd bjyc xxau cfiv")
    msg= f'''Subject: OTP Verification\n\nHere is your mail verification {val}'''
    server.sendmail(senders,mail,msg)
    # Pass the name to stage 2
    return render_template("web.html", stage=2, mail=mail)

@app.route("/verify", methods=["POST"])
def verify():
    # Retrieve the number from the form
    number = request.form.get("number")
  
    b.execute("select*from otpapp;")
    c=b.fetchall()
    
    success = number == val
    if number==val:
            
        ab="Verified"
    else:
        
        ab="Failed"
    
    for i in c:
        if mail in i:
      
            query="update otpapp set Authentication='{}' where mail='{}'".format(ab,mail)
            b.execute(query)
            a.commit()
            break
    else:
        
        query="insert into otpapp values ('{}',{},'{}')".format(mail,number,ab)
        
        b.execute(query)
        a.commit()
       
    
    
    
    
    
    
    # Check if the input matches the stored value
    success = number == val
    return render_template("web.html", stage=3, success=success)

if __name__ == "__main__":
    app.run(debug=True)
