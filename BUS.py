from flask import Flask, render_template, redirect, session, url_for, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import numpy as np
import pandas as pd
from datetime import datetime


BUS = Flask(__name__)

BUS.secret_key = 'root'

BUS.config['MYSQL_HOST'] = 'localhost'
BUS.config['MYSQL_USER'] = 'root'
BUS.config['MYSQL_PASSWORD'] = 'M@t0shri'
BUS.config['MYSQL_DB'] = 'codespyder'


mysql = MySQL(BUS)

@BUS.route("/")
@BUS.route('/home', methods = ['GET','POST'])
def home():
    return render_template('home.html')

@BUS.route('/admin', methods= ['GET', 'POST'])
def admin():
    msg = ''
    if request.method == 'POST' and 'Admin_name' in request.form and 'Password' in request.form :
        admin_name = request.form['Admin_name']
        password = request.form['Password']
        if (admin_name == 'CodeSpyder' and password == 'dsml19'):
            msg = 'Logged in successfully !'
            print('admin login')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Bookings')
            data = cursor.fetchall()
            return render_template('admin_page.html', msg = msg, data = data)
        else:
            msg = 'Invalid login'
            return render_template('admin.html', msg = msg)
    else:
        return render_template('admin.html', msg = msg)

@BUS.route('/admin_page', methods = ['GET', 'POST'])
def admin_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST' and 'Booking_Id' in request.form :
        booking_id = request.form['Booking_Id']
        cursor.execute('SELECT * FROM Bookings WHERE Booking_Id ='+str(booking_id))
        result = cursor.fetchone()
        
        if result:
            cursor.execute('DELETE FROM Bookings WHERE Booking_Id ='+str(booking_id))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM Bookings')
            data = cursor.fetchall()
            msg = 'Ticket of' +' '+ booking_id +' '+'has been cancelled.'
    return render_template('admin_page.html', msg = msg, data = data)



@BUS.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    return render_template('Dashboard.html')

@BUS.route('/login1', methods = ['GET','POST'])
def login1():
    return render_template('login.html')

@BUS.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form :
        username = request.form['Username']
        password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UserLogin WHERE Username = % s AND Password = % s',(username, password))
        account = cursor.fetchone()
        if account:
            session['username'] = account['Username']
            session['password'] = account['Password']
            print('Session Variable set....')
            msg = 'Logged in successfully !'
            return render_template('Dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html')

@BUS.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'Username' in request.form and 'Password' in request.form and 'BirthDate' in request.form and 'E_mail' in request.form :
        name = request.form['Name']
        username = request.form['Username']
        password = request.form['Password']
        email = request.form['E_mail']
        birthdate = request.form['BirthDate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM UserLogin WHERE Username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            return render_template('login.html', msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO UserLogin VALUES (% s, % s, % s, % s, % s)', (name, username, password, email, birthdate))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@BUS.route('/booking1', methods = ['GET','POST'])
def bookings1():
    return render_template('booking.html')

@BUS.route('/booking', methods=['GET','POST'])
def booking():
    msg = ''
    if request.method == 'POST' and 'Arrive' in request.form and 'Destination' in request.form and 'PassengerNo' in request.form and 'Travel_Date' in request.form and 'Arrival_time' in request.form :
        booking_id = np.random.randint(1000, 9999)
        uname = session['username']
        arrive = request.form['Arrive']
        destination = request.form['Destination']
        passengerno = int(request.form['PassengerNo'])
        date = request.form['Travel_Date']
        Arrival_time = request.form['Arrival_time']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BusDetails WHERE Arrive = % s AND Destination = % s AND Arrival_Time = % s', (arrive, destination, Arrival_time))
        account = cursor.fetchone()
        if account:
            cursor.execute('SELECT BusId, Fare, Departure_Time, Travel_Time , Ava_Seats FROM BusDetails WHERE Arrive = % s AND Destination = % s AND Arrival_Time = % s',(arrive, destination, Arrival_time))
            records = cursor.fetchone()
            busid = records['BusId']
            fare = records['Fare']
            Departure_time = records['Departure_Time']
            Travel_time = records['Travel_Time']
            Ava_Seats = int(records['Ava_Seats'])
            Total_Fare = fare*int(passengerno)

            datelist = pd.date_range(datetime.today(), periods=30).tolist()
            d1 = str(datelist[0]).split(' ')[0]
            d2 = str(datelist[-1]).split(' ')[0]

            if d1<= str(date)<= d2:
                cursor.execute('SELECT SUM(PassengerNo) as totalPassanger FROM Bookings WHERE BusId = % s AND Travel_Date = % s', (busid, date))
                tableData = cursor.fetchone()
                
                if tableData['totalPassanger'] is not None:
                    pass_count = int(tableData['totalPassanger'])
                    rem_seats = Ava_Seats - pass_count

                    if (rem_seats - passengerno) >= 0:
                        cursor.execute('INSERT INTO Bookings VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (busid , uname, arrive, destination, date, Arrival_time, Departure_time, passengerno , Total_Fare, booking_id))
                        mysql.connection.commit()
                        msg = 'Fare amount for single person is : ' + str(fare) + ' for date : ' + date + ' and time is - ' + Arrival_time + ' bus will departure at ' + str(Departure_time) + ' your journey is of ' + Travel_time +'.'
                        cursor.execute('SELECT * FROM Bookings WHERE Username = % s', [session['username']])
                        data = cursor.fetchall()
                        return render_template('status.html', msg = msg, data = data)
                    else:
                        msg = 'Not enough seats available'
                        return render_template('booking.html', msg=msg)
                
                else:
                    pass_count = 0
                    rem_seats = Ava_Seats - pass_count

                    if (Ava_Seats -  passengerno) >= 0:
                        cursor.execute('INSERT INTO Bookings VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (busid , uname, arrive, destination, date, Arrival_time, Departure_time, passengerno , Total_Fare, booking_id))
                        mysql.connection.commit()
                        msg = 'Fare amount for single person is : ' + str(fare) + ' for date : ' + date + ' and time is - ' + Arrival_time + ' bus will departure at ' + str(Departure_time) + ' your journey is of ' + Travel_time +'.'
                        cursor.execute('SELECT * FROM Bookings WHERE Username = % s', [session['username']])
                        data = cursor.fetchall()
                        return render_template('status.html', msg = msg, data = data)
                    
                    else:
                        msg = 'Not enough seats available'
                        return render_template('booking.html', msg = msg)
            else: 
                msg = 'Invalid Date'
                return render_template('booking.html', msg = msg)       
        else :
            msg = 'Bus Service Not Available!'
        return render_template('booking.html', msg=msg)

@BUS.route('/status', methods=['GET','POST'])
def status():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Bookings WHERE Username = %s',[session['username']])
    data = cursor.fetchall()
    return render_template('status.html', data = data)

@BUS.route('/cancellation1', methods=['GET','POST'] )
def cancellation1():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Bookings WHERE Username = %s', [session['username']])
    data = cursor.fetchall()
    return render_template('cancellation.html', data = data)


@BUS.route('/cancellation', methods=['GET', 'POST'])
def cancellation():
    msg = ''
    data = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Bookings WHERE Username = %s', [session['username']])
    data = cursor.fetchall()

    if request.method == 'POST' and 'Booking_Id' in request.form :
        booking_id = request.form['Booking_Id']
        cursor.execute('SELECT * FROM Bookings WHERE Booking_Id ='+str(booking_id))
        result = cursor.fetchone()
        
        if result:
            cursor.execute('DELETE FROM Bookings WHERE Username = % s AND Booking_Id = % s' , ([session['username']], booking_id))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM Bookings WHERE Username = % s', [session['username']])
            data = cursor.fetchall()
            msg = 'Your Ticket of' +' '+ booking_id +' '+'has been cancelled. you will get refund within 24hrs.'
            
        else:
            msg = 'Booking Id not found'
            return render_template('cancellation.html', msg = msg, data = data)

    return render_template('cancellation.html', msg = msg, data = data)

@BUS.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('home'))
    
if __name__ == "__main__":
     BUS.run(debug=True)

