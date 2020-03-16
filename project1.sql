CREATE database project1;

USE project1;

CREATE table Restaurants(
    Res_ID INT(5) AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    Type VARCHAR(20) NOT NULL,
    Price VARCHAR(4) NOT NULL
);

CREATE table Destination(
    Des_ID INT(5) AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    Type VARCHAR(30) NOT NULL,
    Opening_Time VARCHAR(5) NOT NULL
);

CREATE table Daytrip(
    Trip_ID INT(5) AUTO_INCREMENT PRIMARY KEY,
    First_Name_on_Booking VARCHAR(50) NOT NULL,
    Last_Name_on_Booking VARCHAR(50) NOT NULL,
    No_of_People INT(5) NOT NULL,
    Trip_Res_ID INT(5), 
    FOREIGN KEY (Trip_Res_ID) REFERENCES Restaurants(Res_ID)
);

CREATE table DesJoin(
    Trip_ID INT(5),
    Destination_ID INT(5), 
    FOREIGN KEY (Trip_ID) REFERENCES Daytrip(Trip_ID),
    FOREIGN KEY (Destination_ID) REFERENCES Destination(Des_ID)
);


INSERT INTO Restaurants(Name,Address,Type,Price)
VALUES ('Select an Option:', 'Default Address', 'Def type', '££££'),
('Rudys Neapolitan Pizza', '9 Cotton St, Ancoats, Manchester, M4 5BF','Italian','£'),
('Northern Soul Grilled Cheese','10 Church St, Manchester, M4 1PN','American','£'),
('The Pasta Factory','77 Shudehill, Manchester, M4 4AN','Italian','££'),
('Wah Ji Wah','37 King Street West, Manchester, M3 2PW','Indian','££'),
('MyLahore','14-18 Wilmslow Road, Manchester, M14 5TQ','Indian','££'),
('The Alchemist MediaCityUk','The Bund, The Quays, MediacityUK, Salford, M50 3AB', 'Cocktail Bar', '£££' ),
('Peter Street Kitchen', 'Free Trade Hall, Peter St, Manchester, M2 5GP','Japanese','££'),
('Alabamas','8 , 10 Tariff St, Manchester, M1 2FF','American','££'),
('Revolution','90-94 Oxford St, Manchester, M1 5WH','British','££'),
('20 Stories','NO.1, 1 Hardman Square, Manchester, M3 3EB','European','££££'),
('Gaucho Manchester','2A St Marys St, Manchester, M3 2LB','Argentinian','££');


INSERT INTO Destination(Name,Address,Type)
VALUES ('Select an Option:', 'Default Address','Default type'),
('Old Trafford','Sir Matt Busby Way, Trafford Park, Stretford, Manchester, M16 0RA','Sporting Events'),
('Etihad Stadium','Ashton New Rd, Manchester, M11 3FF','Sporting Events'),
('Trafford Centre','The Orient, Trafford Park, Stretford, Manchester, M17 8AA','Leisure'),
('Whitworth Art Gallery', 'Oxford Rd, Manchester, M15 6ER', 'Art Gallery'),
('Manchester Art Gallery','Mosley St, Manchester, M2 3JL', 'Art Gallery'),
('Manchester Museum', 'University of, Oxford Rd, Manchester, M13 9PL', 'Museum'),
('Chill Factore', '7 Trafford Way, Trafford Park, Stretford, Manchester, M41 7JA', 'Sporting'),
('Science and Industry Museum', 'Liverpool Rd, Manchester, M3 4FP', 'Museum'),
('Printworks', '27 Withy Grove, Manchester, M4 2BS', 'Leisure'),
('Manchester Arena', 'Victoria Station Approach, Hunts Bank, Manchester, M3 1AR', 'Events'),
('Albert Hall, City Centre', '27 Peter St, Manchester, M2 5QR', 'Events'),
('Arndale', 'New Cannon Street Mall, Manchester, M4 3AQ', 'Leisure'),
('Adventure Medlock', 'Gardenfold Way, Droylsden, Manchester, M43 7XU', 'Sporting'),
('Heaton Park', 'Middleton Rd, Manchester, M25 2SW', 'Parks'),
('Crystal Maze Live Experience', 'The Crystal Maze Studios, Lower Byrom St, Manchester, M3 4FP', 'Escape Room'),
('Chorlton Water Park', '74 Maitland Ave, Manchester, M21 7WH', 'Parks');