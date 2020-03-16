from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mysqldb import MySQL
from forms import PostForm
import os

app = Flask(__name__)


app.config['MYSQL_HOST'] = os.environ['MYSQLHOST'] #-ip address of SQL DB - environ variable: MYSQLHOST="ip address"
app.config['MYSQL_USER'] = os.environ['MYSQLUSER'] #-Username for DB - environ variable: MYSQLUSER="root"
app.config['MYSQL_PASSWORD'] = os.environ['MYSQLPASSWORD'] #Password for DB - environ variable: MYSQLPASSWORD="whatever the password is"
app.config['MYSQL_DB'] = os.environ['MYSQLDB'] #Database thats being used - environ variable: MYSQLDB="whatever database you want to use"
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = b'_5#bfgolas(^(^(*sklngdaslxec]/'

mysql = MySQL(app)

@app.route("/")
def home():
    #cur = mysql.connection.cursor() #- connect to SQL database
    #cur.execute("Select * from accounts;") #- SQL commands to run (ID Int(3) , name Varchar(20));"
    #mysql.connection.commit() #- Executes MYSQL command
    #x = cur.fetchall() # local variable
    #cur.close() #- closes the connection to the DB
    
    #info =[]

    #for row in x:
    #    info.append(row)
    #print(info)

    return render_template("index.html" , title = '0161 Manny on the Map')

@app.route("/world")
def world():
    return render_template("world.html" , title = 'BOTTLERS')

@app.route("/DaytripCreate", methods=['GET','POST'])
def daytrip():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Res_ID, Name FROM Restaurants")
    resname=cur.fetchall()
    cur.close()
    x = mysql.connection.cursor()
    x.execute("SELECT Des_ID, Name FROM Destination")
    destname=x.fetchall()
    x.close()
    if request.method == "POST":
        details = request.form
        firstN = details['UFName']
        lastN = details['ULName']
        NoFPeople = details['NoPeople']
        Restaurant_ID = details['Res_ID']
        Destination1 = details['Des_ID1']
        Destination2 = details['Des_ID2']
        
        if NoFPeople == '':
            nop = 0
        else:
            nop = int(NoFPeople)
        if type(nop) != int:
            nop = 100

        if firstN == '' or lastN == '' or NoFPeople == '':
            flash('You must fill in all fields! Please try again!', 'danger')
            return redirect(url_for('daytrip'))
        if Destination1 == '1' or Destination2 == '1' or Restaurant_ID =='1':
            flash('You must fill in all fields! Please try again!', 'danger')
            return redirect(url_for('daytrip')) 
        if nop > 30:
            flash('You have too many people in your booking, Please contact us directly for large group bookings (30+)', 'danger')
            return redirect(url_for('daytrip'))
        if Destination1 == Destination2:
            flash('You cannot select the same Destination twice! Please try again', 'danger')
            return redirect(url_for('daytrip'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Daytrip (First_Name_on_Booking, Last_Name_on_Booking, No_of_People, Trip_Res_ID) VALUES (%s, %s, %s, %s)", (firstN, lastN, NoFPeople, Restaurant_ID))
            mysql.connection.commit()
            cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")
            trip = cur.fetchall()
            tripid = trip[0]
            tripid = tripid[0]
            #print(tripid)
            cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripid,Destination1))
            cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripid,Destination2))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('posttripcreate'))
    else:
        return render_template("daytripcreate.html" , title = 'Daytrips', resname=resname, destname=destname)

@app.route("/bookingconf", methods =['GET'])
def posttripcreate():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")
    daytripinfo = cur.fetchall()
    allinfo = daytripinfo[0]
    daytriplist = []
    for i in daytripinfo:
        for j in i:
            daytriplist.append(j)
    tripid = allinfo[0]
    resid = allinfo [4]
    cur.execute("SELECT Destination.Name, Destination.Address FROM Destination JOIN DesJoin ON Destination.Des_ID = DesJoin.Destination_ID WHERE DesJoin.Trip_ID = (%s)",[tripid])
    destinationinfo = cur.fetchall()
    d1 = list(destinationinfo[0])
    d2 = list(destinationinfo[1])
    cur.execute("SELECT Restaurants.Name, Restaurants.Address, Restaurants.Type, Restaurants.Price FROM Restaurants JOIN Daytrip on Daytrip.Trip_Res_ID = Restaurants.Res_ID WHERE Daytrip.Trip_Res_ID = (%s)", [resid])
    resinfo = cur.fetchall()
    r1 = list(resinfo[0])
    mysql.connection.commit()
    cur.close()
    return render_template("bookingconf.html", title = 'Your Created Trip:', allinfo=daytriplist, r1=r1, d1=d1, d2=d2)


@app.route("/DaytripManager", methods = ['POST','GET'])
def daytripmanage():
   
    if request.method == "POST":
        cur = mysql.connection.cursor()
        details = request.form
        tripidval = details['UTripID'] #tripidval
        firstN = details['UFName']
        lastN = details['ULName']
        cur.execute("SELECT First_Name_on_Booking, Last_Name_on_Booking FROM Daytrip WHERE Trip_ID = %s", [tripidval])
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)
        if len(daytriplist) == 0:
            flash('You have entered invalid credentials please try again', 'danger')
            return redirect(url_for('daytripmanage'))
        else:
            first_name_on_booking = daytriplist[0] #first name on booking
            last_name_on_booking = daytriplist[1] #last name on booking
            cur.close()
            if firstN.lower() == first_name_on_booking.lower() and lastN.lower() == last_name_on_booking.lower():
                session['tripid'] = tripidval
                session['firstn'] = firstN
                session['lastN'] = lastN
                if request.form['action'] == 'manage':
                    return redirect(url_for('daytripmanagementconsole'))
                if request.form['action'] == 'delete':
                    return redirect(url_for('deleteconf')) 
            else:
                flash('You have entered invalid credentials please try again', 'danger')
                return redirect(url_for('daytripmanage'))          
    return render_template("daytripmanager.html" , title = 'Daytrip Manager') 

@app.route("/DaytripManagementconsole", methods=['GET','POST'])
def daytripmanagementconsole():
    tripid = session['tripid']
    print(tripid)
    cur = mysql.connection.cursor()
    cur.execute("SELECT First_Name_on_Booking, Last_Name_on_Booking, No_of_People, Trip_Res_ID FROM Daytrip WHERE Trip_ID = %s", [tripid])
    daytripinfo = cur.fetchall()
    daytriplist = []
    for i in daytripinfo:
        for j in i:
            daytriplist.append(j)
    #first_name_on_booking = daytriplist[0] #first name on booking
    #last_name_on_booking = daytriplist[1] #last name on booking
    #nop = daytriplist[2]
    tripresid = daytriplist[3] #tripresid
    cur.execute("SELECT Restaurants.Name, Restaurants.Address, Restaurants.Type, Restaurants.Price FROM Restaurants JOIN Daytrip on Daytrip.Trip_Res_ID = Restaurants.Res_ID WHERE Daytrip.Trip_Res_ID = (%s)", [tripresid])
    resinfo = cur.fetchall()
    r1 = list(resinfo[0])
    cur.execute("SELECT Des_ID, Destination.Name, Destination.Address FROM Destination JOIN DesJoin ON Destination.Des_ID = DesJoin.Destination_ID WHERE DesJoin.Trip_ID = (%s)",[tripid])
    destinationinfo = cur.fetchall()
    d1 = list(destinationinfo[0])
    d2 = list(destinationinfo[1])
    d1old = d1[0]
    d2old = d2[0]
    cur = mysql.connection.cursor()
    cur.execute("SELECT Res_ID, Name FROM Restaurants")
    resname=cur.fetchall()
    cur.close()
    x = mysql.connection.cursor()
    x.execute("SELECT Des_ID, Name FROM Destination")
    destname=x.fetchall()
    x.close()
    if request.method == "POST":
        details = request.form
        if details['UFName'] == '':
            firstN = daytriplist[0]
        else:
            firstN = details['UFName']
        if details['ULName'] == '':
            lastN = daytriplist[1]
        else:
            lastN = details['ULName']
        if details['NoPeople'] == '':
            NoFPeople = daytriplist[2]
        else:
            NoFPeople = details['NoPeople']
        if details['Res_ID'] == '1':
            Restaurant_ID = daytriplist[3]
        else:
            Restaurant_ID = details['Res_ID']
        if details['Des_ID1'] == '1':
            Destination1 = d1[0]
        else:
            Destination1 = details['Des_ID1']
        if details['Des_ID2'] == '1':
            Destination2 = d2[0]
        else:    
            Destination2 = details['Des_ID2']
        print(Destination1)
        print(d1old)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE DesJoin SET Destination_ID = %s WHERE Trip_ID = %s AND Destination_ID = %s", (Destination1, tripid, d1old))
        mysql.connection.commit()
        cur.execute("UPDATE DesJoin SET Destination_ID = %s WHERE Trip_ID = %s AND Destination_ID = %s", (Destination2, tripid, d2old))
        mysql.connection.commit()
        cur.execute("UPDATE Daytrip SET First_Name_on_Booking = %s, Last_Name_on_Booking = %s WHERE Trip_ID = %s", (firstN, lastN, int(tripid)))
        mysql.connection.commit()
        cur.execute("UPDATE Daytrip SET No_of_People = %s, Trip_Res_ID = %s WHERE Trip_ID = %s", (NoFPeople, Restaurant_ID, int(tripid)))
        mysql.connection.commit()
        cur.close()
        flash('Booking has been updated', 'success')
        return redirect(url_for('daytripmanagementconsole'))

    return render_template("daytripmanagementconsole.html" , title = 'Daytrip Manager', tripid = tripid, daytriplist = daytriplist, r1=r1, d1=d1, d2=d2, resname=resname, destname=destname ) 

@app.route("/Daytripdeletion", methods = ['POST','GET'])
def deleteconf():
    tripidval = session['tripid']
    firstN = session['firstn']
    lastN = session['lastN']
    print("tripidval", tripidval)
    print("firstN", firstN)
    print("lastN", lastN)
    if request.method == "POST":   
        details = request.form
        tripidconf = details['UTripIDconf'] #tripidval
        firstNconf = details['UFNameconf']
        lastNconf = details['ULNameconf']
        print("tripidconf", tripidconf)
        print("firstNconf", firstNconf)
        print("lastNconf", lastNconf)
        if tripidval == tripidconf and firstN.lower() == firstNconf.lower() and lastN.lower() == lastNconf.lower():
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM DesJoin WHERE Trip_ID = %s", [tripidconf])
            mysql.connection.commit()
            cur.execute("DELETE FROM Daytrip WHERE Trip_ID = %s", [tripidconf])
            mysql.connection.commit()
            flash('You have deleted your booking successfully!', 'success')
            return redirect(url_for('daytripmanage'))
            cur.close()
        else:
            flash('You have not confirmed your details correctly, please try again', 'danger')
            return redirect(url_for('deleteconf'))
    return render_template("deleteconf.html" , title = 'Daytrip Deletion')



def goHome():
    return render_template("index.html" , title = 'Daytrips')


@app.route("/Destinations")
def destinations():
    return render_template("destinations.html" , title = 'Destinations')

@app.route("/Restaurants")
def restaurants():
    return render_template("restaurants.html" , title = 'Restaurants')

if __name__ == "__main__":
    app.run('0.0.0.0', debug = True)