from flask import Flask
from flask_mysqldb import MySQL
import os
import urllib3
import time
import pytest
app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST') #-ip address of SQL DB - environ variable: MYSQLHOST="ip address"
app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER') #-Username for DB - environ variable: MYSQLUSER="root"
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD') #Password for DB - environ variable: MYSQLPASSWORD="whatever the password is"
app.config['MYSQL_DB'] = os.environ.get('MYSQLDB') #Database thats being used - environ variable: MYSQLDB="whatever database you want to use"
app.secret_key = os.environ.get('MYSQLSECRETKEY') # Secret Key for use with session

mysql = MySQL(app)


def test_mainurl():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://34.89.78.75:5000/') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection

def test_createurl():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://34.89.78.75:5000/DaytripCreate') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection

def test_managerurl():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://34.89.78.75:5000/DaytripManager') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection

def test_destinationsurl():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://34.89.78.75:5000/Destinations') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection

def test_restauranturl():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://34.89.78.75:5000/Restaurants') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection


############################################## Database Testing Loop ##############################################


#### Global Test Vars ####

firstN = "TestFirstName"             
lastN = "TestLastName"              
NoFPeople = "10"       
Restaurant_ID = "9"    
Destination1 = "10"      
Destination2 = "11"
tripidold = "0"
tripidnew = "0"
pytest.x = "0"

def test_create():

    with app.app_context():

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")
        mysql.connection.commit()                                                                                                                   
        tripold = cur.fetchall()                                                                                                                                                              
        tripidold = tripold[0]                                                                                                                                                                    
        tripidold = tripidold[0]
        pytest.x = tripidold
        cur = mysql.connection.cursor()                                                                                                                                                     
        cur.execute("INSERT INTO Daytrip (First_Name_on_Booking, Last_Name_on_Booking, No_of_People, Trip_Res_ID) VALUES (%s, %s, %s, %s)", (firstN, lastN, NoFPeople, Restaurant_ID))      
        mysql.connection.commit()                                                                                                                                                          
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")                                                                                                                  
        tripnew = cur.fetchall()                                                                                                                                                              
        tripidnew = tripnew[0]                                                                                                                                                                    
        tripidnew = tripidnew[0]                                                                                                                                                                 
        cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripidnew,Destination1))                                                                                    
        cur.execute("INSERT INTO DesJoin (Trip_ID,Destination_ID) VALUES (%s,%s)",(tripidnew,Destination2))                                                                                    
        mysql.connection.commit()                                                                                                                                                           
        cur.close()
        assert 1 == (tripidnew - tripidold)

time.sleep(2)

def test_read():

    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")      
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)
        tripid = daytriplist[0]
        firstname = daytriplist[1]
        lastname = daytriplist[2]
        NoOfPeople = daytriplist [3]                                                                                                                                                                                                    
        resid = daytriplist [4]                                                                                                                                                                                                     
        cur.execute("SELECT Destination_ID FROM Destination JOIN DesJoin ON Destination.Des_ID = DesJoin.Destination_ID WHERE DesJoin.Trip_ID = (%s)",[tripid])                                         
        destinationinfo = cur.fetchall()                                                                                                                                                                                       
        d1 = list(destinationinfo[0])                                                                                                                                                                                                
        d2 = list(destinationinfo[1])
        desid1 = d1[0]
        desid2 = d2[0]
        cur.close()
        
        assert (firstname == firstN) == True and (lastname == lastN) == True and (int(NoFPeople) == NoOfPeople) == True and (resid == int(Restaurant_ID)) == True and (desid1 == int(Destination1)) == True and (desid2 == int(Destination2)) == True
 
time.sleep(2)

def test_update():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")      
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)
        
        tripid = daytriplist[0] 
        firstNew = "TestFirstNameNew"
        lastNew = "TestLastNameNew"
        NoPeopleNew = "21"
        resnew = "5"
        d1old = Destination1       
        d2old = Destination2
        d1new = "3"
        d2new = "4"

        cur = mysql.connection.cursor()
        cur.execute("UPDATE DesJoin SET Destination_ID = %s WHERE Trip_ID = %s AND Destination_ID = %s", (d1new, tripid, d1old))
        mysql.connection.commit()
        cur.execute("UPDATE DesJoin SET Destination_ID = %s WHERE Trip_ID = %s AND Destination_ID = %s", (d2new, tripid, d2old))
        mysql.connection.commit()
        cur.execute("UPDATE Daytrip SET First_Name_on_Booking = %s, Last_Name_on_Booking = %s WHERE Trip_ID = %s", (firstNew, lastNew, int(tripid)))
        mysql.connection.commit()
        cur.execute("UPDATE Daytrip SET No_of_People = %s, Trip_Res_ID = %s WHERE Trip_ID = %s", (NoPeopleNew, resnew, int(tripid)))
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")      
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)

        firstupdated = daytriplist[1]
        lastupdated= daytriplist[2]
        nopupdated = daytriplist [3]                                                                                                                                                                                                    
        residupdated = daytriplist [4]     
        cur.execute("SELECT Des_ID FROM Destination JOIN DesJoin ON Destination.Des_ID = DesJoin.Destination_ID WHERE DesJoin.Trip_ID = (%s)",[tripid])
        destinationinfo = cur.fetchall()
        d1 = list(destinationinfo[0])
        d2 = list(destinationinfo[1])
        desid1updated = d1[0]
        desid2updated = d2[0]

        assert (firstupdated == firstNew) == True and (lastupdated == lastNew) == True and (nopupdated == int(NoPeopleNew)) == True and (residupdated == int(resnew)) == True and (desid1updated == int(d1new)) == True and (desid2updated == int(d2new)) == True

time.sleep(2)

def test_delete():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")      
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)
        tripidnew = daytriplist[0] 

        cur.execute("DELETE FROM DesJoin WHERE Trip_ID = %s", [tripidnew])
        mysql.connection.commit()
        cur.execute("DELETE FROM Daytrip WHERE Trip_ID = %s", [tripidnew])
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Daytrip ORDER BY Trip_id DESC LIMIT 1")      
        daytripinfo = cur.fetchall()
        daytriplist = []
        for i in daytripinfo:
            for j in i:
                daytriplist.append(j)
        tripidold = daytriplist[0]
        
        value = int(tripidold) - int(tripidnew)

        cur.execute("ALTER TABLE Daytrip AUTO_INCREMENT = %s", [pytest.x])
        
        assert -1 == value




