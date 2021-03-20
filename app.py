from flask import Flask,render_template,flash,request,redirect,url_for
from flask_mysqldb import MySQL 

import MySQLdb.cursors

app=Flask(__name__)

app.secret_key = 'SPARK'

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6400328'
app.config['MYSQL_PASSWORD'] = 'eRiZVFhYTA'
app.config['MYSQL_DB'] = 'sql6400328'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/custlist")
def cust():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customer")
    detail=cursor.fetchall()
    return render_template('custlist.html', value=detail)

@app.route("/transactions", methods=['GET', 'POST'])
def tra():
    if  request.method == 'POST' and 'reciever'in request.form and 'amount' in request.form and 'c_name' in request.form and 'c_bal' in request.form:
        reciever=request.form['reciever']
        #print(reciever)
        amount=float(request.form['amount'])
        amount1=float(request.form['amount'])
        sender=request.form['c_name']
        scurrbal=float(request.form['c_bal'])
        cursor = mysql.connection.cursor()
        sbal=scurrbal-amount
        cursor.execute("SELECT c_bal FROM customer WHERE c_name=%s",(reciever,))
        rc_bal=cursor.fetchone()
        rcurrbal=float(rc_bal[0])
        rbal=rcurrbal+amount1
        #cursor.execute("SELECT * FROM transact WHERE sender=%s",(sender,))

        #tid=cursor.fetchall()
        #print("checking")
        if scurrbal>=amount:
            cursor.execute("UPDATE customer SET c_bal=%s where c_name=%s", (rbal, reciever,))
            cursor.execute("UPDATE customer SET c_bal=%s where c_name=%s", (sbal, sender,))           
            cursor.execute("INSERT INTO transact(sender,reciever,amount) VALUES ( %s, %s,%s)", (sender, reciever, amount,))
            mysql.connection.commit()
            #return redirect(url_for('transdis'))
        else:
            return "CHOOSE A SMALLER AMOUNT!"  
        return redirect(url_for('transdis'))
        #return render_template('transact.html',value=tid)


@app.route("/transactdisplay",methods=['GET', 'POST'])
def transdis():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transact ORDER BY td desc")
    cdata=cursor.fetchall()
    print(cdata)
    return render_template('transact.html',value=cdata)  

@app.route("/prof", methods=['GET', 'POST'])
def prof():
    if request.method == 'POST' and 'custid'in request.form and 'c_name' in request.form  and 'c_email' in request.form  and 'c_bal' in request.form:
        cNAME=request.form['c_name']
        i_d=request.form['custid']
        Cemail=request.form['c_email']
        Cbal=request.form['c_bal']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customer WHERE custid=%s",(i_d,))
        pinfo=cursor.fetchall()
        cursor.execute("SELECT * FROM customer WHERE not custid=%s",(i_d,))
        sopt=cursor.fetchall()
        #print(sopt)
        #print(pinfo)
        return render_template('profile.html',value=pinfo,value1=cNAME,value2=i_d,value3=Cemail,value4=Cbal,data=sopt)



if __name__=="__main__":
    app.run(debug=True);  
