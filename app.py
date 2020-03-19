from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mysqldb import MySQL
#from forms import PostForm
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST') #-ip address of SQL DB - environ variable: MYSQLHOST="ip address"
app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER') #-Username for DB - environ variable: MYSQLUSER="root"
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD') #Password for DB - environ variable: MYSQLPASSWORD="whatever the password is"
app.config['MYSQL_DB'] = os.environ.get('MYSQLDB') #Database thats being used - environ variable: MYSQLDB="whatever database you want to use"
app.secret_key = os.environ.get('MYSQLSECRETKEY') # Secret Key for use with session
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #NOT USED

mysql = MySQL(app)


############################################################# Home Page ##############################################################

@app.route("/") 
def home():
    return render_template("index.html" , title = '0161 Manny on the Map')

######################################################## Daytrip Create Page ##########################################################

@app.route("/DaytripCreate", methods=['GET','POST'])
def daytrip():

    ############## Pull Restaurant and Destination Name Info for use in a dropdown list #############

    cur = mysql.connection.cursor()
    cur.execute("SELECT Res_ID, Name FROM Restaurants")
    resname=cur.fetchall()
    cur.close()
    x = mysql.connection.cursor()
    x.execute("SELECT Des_ID, Name FROM Destination")
    destname=x.fetchall()
    x.close()

    ################## Inserting information into Database if the Form is submitted ###################
    
    if request.method == "POST":                ## Checks to see if the Form is submitted as a POST Request
        details = request.form                  ## Pulls the Data from the Form
        firstN = details['UFName']              ## First Name on Daytrip Booking
        lastN = details['ULName']               ## Last Name on Daytrip Booking
        NoFPeople = details['NoPeople']         ## No of People on Daytrip Booking
        Restaurant_ID = details['Res_ID']       ## Restaurant selected on Daytrip Booking
        Destination1 = details['Des_ID1']       ## 1st Dest selected on Daytrip Booking
        Destination2 = details['Des_ID2']       ## 2nd Dest selected on Daytrip Booking
        
    ######## Data Validation Section ########

    ## Checking to ensure that all fields have data entered into it and also if name field character limit < 50:

        if firstN == '' or lastN == '' or NoFPeople == '':
            flash('You must fill in all fields! Please try again!', 'danger')
            return redirect(url_for('daytrip'))
        if len(firstN) > 50 or len(lastN) > 50:
            flash('Your name cannot be longer than 50 characters, Please enter it again', 'danger')
            return redirect(url_for('daytrip')) 
        if Destination1 == '1' or Destination2 == '1' or Restaurant_ID =='1':
            flash('You must fill in all fields! Please try again!', 'danger')
            return redirect(url_for('daytrip'))

    ## Checking to ensure name fields only have letters entered into it:

        lettertest=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
        nametest1 = list(firstN.lower())
        nametest2 = list(lastN.lower())
        for i in nametest1:
            if i not in lettertest:
                flash('You can only enter letters in the name Field, Please try again', 'danger')
                return redirect(url_for('daytrip'))    
        for i in nametest2:
            if i not in lettertest:
                flash('You can only enter letters in the name Field, Please try again', 'danger')
                return redirect(url_for('daytrip'))

    ## Checking to ensure No of People Field only has numbers entered into it (or if blank -> 0)

        if NoFPeople == '':
            nop = 0
        else:
            nop = list(NoFPeople)
        a = ['1','2','3','4','5','6','7','8','9','0']
        for i in nop:
            if i not in a:
                flash('You can only enter numbers in the No of People Field, Please try again', 'danger')
                return redirect(url_for('daytrip')) 
            else:
                nop = int(NoFPeople)

    ## Checking to see if no of people value > 30:

        if nop > 30:
            flash('You have too many people in your booking, Please contact us directly for large group bookings (30+)', 'danger')
            return redirect(url_for('daytrip'))

    ## Checking to see if both destinations selected are the same:

        if Destination1 == Destination2:
            flash('You cannot select the same Destination twice! Please try again', 'danger')
            return redirect(url_for('daytrip'))

    ## Inserting Info into MySQL Database:
        else:
            cur = mysql.connection.cursor()                                                                                                                                                     ## Opens Connection to Database
            cur.execute("INSERT INTO Daytrip (First_Name_on_Booking, Last_Name_on_Booking, No_of_People, Trip_Res_ID) VALUES (%s, %s, %s, %s)", (firstN, lastN, NoFPeople, Restaurant_ID))      ## Inserts First Name, Last Name, No of People and Selected Restaurant ID information into Database                            
            mysql.connection.commit()                                                                                                                                                           ## Commits commands to Database
            cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")                                                                                                                  ## Pulls the Trip_ID created
            trip = cur.fetchall()                                                                                                                                                               ## ^^^^                        
            tripid = trip[0]                                                                                                                                                                    ## Extracts Trip_ID Value from list that was returned back
            tripid = tripid[0]                                                                                                                                                                  ## ^^^^
            cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripid,Destination1))                                                                                    ## Inserts Destination 1 into joining table with the current Trip_ID
            cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripid,Destination2))                                                                                    ## Inserts Destination 2 into joining table with the current Trip_ID
            mysql.connection.commit()                                                                                                                                                           ## Commits commands to Database
            cur.close()                                                                                                                                                                         ## Closes Connection to Database
            return redirect(url_for('posttripcreate'))                                                                                                                                          ## Redirects to Daytrip Create Confirmation Page
                                                                                                                                                    
    ## Returns Template page for daytrip create:                                                                                                                                             
    else:
        return render_template("daytripcreate.html" , title = 'Daytrips', resname=resname, destname=destname)                                                                                   

################################################## Daytrip Create Confirmation Page ####################################################

@app.route("/bookingconf", methods =['GET'])
def posttripcreate():
    
    ############## Displays All Info for the Booking that was just created #############

    cur = mysql.connection.cursor()                                                 ## Opens Connection to Database
    cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")              ## Selects the most recent daytrip created from the Daytrip Table
    daytripinfo = cur.fetchall()                                                    ## Fetches the info
    allinfo = daytripinfo[0]                                                        ## ^^^^
    daytriplist = []                                                                
    for i in daytripinfo:                                                           ## Converts the tuple returned to a list
        for j in i:
            daytriplist.append(j)

    tripid = allinfo[0]                                                                                                                                                                                                     ## Selects the Trip_ID from the list
    resid = allinfo [4]                                                                                                                                                                                                     ## Selects the Restaurant ID from the list
    cur.execute("SELECT Destination.Name, Destination.Address FROM Destination JOIN DesJoin ON Destination.Des_ID = DesJoin.Destination_ID WHERE DesJoin.Trip_ID = (%s)",[tripid])                                          ## Pulls info for both Destinations using the current Trip_ID 
    destinationinfo = cur.fetchall()                                                                                                                                                                                        ## ^^^^
    d1 = list(destinationinfo[0])                                                                                                                                                                                           ## Converts all info for Destination 1 from Tuple to a list     
    d2 = list(destinationinfo[1])                                                                                                                                                                                           ## Converts all info for Destination 2 from Tuple to a list
    cur.execute("SELECT Restaurants.Name, Restaurants.Address, Restaurants.Type, Restaurants.Price FROM Restaurants JOIN Daytrip on Daytrip.Trip_Res_ID = Restaurants.Res_ID WHERE Daytrip.Trip_Res_ID = (%s)", [resid])    ## Pulls info for the Restaurant using the current Trip_ID
    resinfo = cur.fetchall()                                                                                                                                                                                                ## ^^^^                           
    r1 = list(resinfo[0])                                                                                                                                                                                                   ## Converts the info for the Restaurant from Tuple to a list                                
    mysql.connection.commit()
    cur.close()                                                                                                                                                                                                             ## Closes the connection to the Database  

    ## Returns Template page for the Booking Confirmation                                    
    return render_template("bookingconf.html", title = 'Your Created Trip:', allinfo=daytriplist, r1=r1, d1=d1, d2=d2)                                                                                                      ## Passes the pulled information for use in the HTML template

#################################################### Daytrip Manager Main Page ##########################################################

@app.route("/DaytripManager", methods = ['POST','GET'])
def daytripmanage():
   

    ################## Selecting information into Database if the Form is submitted in the Manager Page ###################

    if request.method == "POST":                        ## Checks to see if the Form is submitted as a POST Request
        cur = mysql.connection.cursor()                 ## Creates a cursor and opens the connection to the database
        details = request.form                          ## Pulls the Data from the Form
        tripidval = details['UTripID']                  ## Trip_ID Value the user has input
        firstN = details['UFName']                      ## First Name the user has input
        lastN = details['ULName']                       ## Last Name the user has input
        
        cur.execute("SELECT First_Name_on_Booking, Last_Name_on_Booking FROM Daytrip WHERE Trip_ID = %s", [tripidval])      ## Pulls First and Last Name from database for the Trip_ID value that the User has input in the form
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

################################################## Daytrip Management Console Page ######################################################

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
            lettertest=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
            nametest1 = list(firstN.lower())
            for i in nametest1:
                if i not in lettertest:
                    flash('You can only enter letters in the name Field, Please try again', 'danger')
                    return redirect(url_for('daytripmanagementconsole'))    
        
        if details['ULName'] == '':
            lastN = daytriplist[1]
        else:
            lastN = details['ULName']
            lettertest=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
            nametest2 = list(lastN.lower())
            for i in nametest2:
                if i not in lettertest:
                    flash('You can only enter letters in the name Field, Please try again', 'danger')
                    return redirect(url_for('daytripmanagementconsole'))
        if details['NoPeople'] == '':
            NoFPeople = daytriplist[2]
        else:
            NoFPeople = details['NoPeople']
            nop = list(NoFPeople)
            a = ['1','2','3','4','5','6','7','8','9','0']
            for i in nop:
                if i not in a:
                    flash('You can only enter numbers in the No of People Field, Please try again', 'danger')
                    return redirect(url_for('daytripmanagementconsole')) 
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
        if len(firstN) > 50 or len(lastN) > 50:
            flash('Your first or last name cannot be longer than 50 characters, Please enter it again', 'danger')
            return redirect(url_for('daytripmanagementconsole')) 
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

################################################## Daytrip Delete Confirmation Page ######################################################

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

##################################################### Daytrip Destinations Page ###########################################################

@app.route("/Destinations")
def destinations():
    return render_template("destinations.html" , title = 'Destinations')

##################################################### Daytrip Restaurants Page ###########################################################    

@app.route("/Restaurants")
def restaurants():
    return render_template("restaurants.html" , title = 'Restaurants')

if __name__ == "__main__":
    app.run('0.0.0.0', debug = True)