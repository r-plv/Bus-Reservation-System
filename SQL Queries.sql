USE codespyder;

CREATE TABLE UserLogin (
    Name VARCHAR(30) NOT NULL,
    Username VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(16) NOT NULL,
    E_mail VARCHAR(30) NOT NULL,
    BirthDate DATE NOT NULL
);

CREATE TABLE BusDetails (
	BusId VARCHAR(5) PRIMARY KEY,
    Arrive VARCHAR(30) NOT NULL,
    Destination VARCHAR(30) NOT NULL,
    Arrival_Time TIME NOT NULL,
    Departure_Time TIME NOT NULL,
    Travel_Time VARCHAR(8) NOT NULL,
    Fare INT NOT NULL,
    PassengerNo INT,
    Ava_Seats INT
);

CREATE TABLE Bookings (
	BusId VARCHAR(5),
    Username VARCHAR(10),
    Arrive VARCHAR(30) NOT NULL,
    Destination VARCHAR(30) NOT NULL,
    Travel_Date DATE NOT NULL,
    Arrival_Time TIME NOT NULL,
    Departure_Time TIME NOT NULL,
    PassengerNo INT NOT NULL,
    Total_Fare INT NOT NULL,
    Booking_Id INT PRIMARY KEY
);

INSERT INTO BusDetails VALUES ('PM1','Pune','Mumbai','08:00:00','08:30:00','4 hrs',400,1,20);
INSERT INTO BusDetails VALUES ('PM2','Pune','Mumbai','20:00:00','20:30:00','3 hrs',400,1,20);
INSERT INTO BusDetails VALUES ('MP1','Mumbai','Pune','08:00:00','08:30:00','4 hrs',400,1,20);
INSERT INTO BusDetails VALUES ('MP2','Mumbai','Pune','20:00:00','20:30:00','3 hrs',400,1,20);
INSERT INTO BusDetails VALUES ('MA1','Mumbai','Amravati','08:00:00','08:30:00','14 hrs',2200,1,20);
INSERT INTO BusDetails VALUES ('MA2','Mumbai','Amravati','20:00:00','20:30:00','12 hrs',2200,1,20);
INSERT INTO BusDetails VALUES ('AM1','Amravati','Mumbai','08:00:00','08:30:00','14 hrs',2200,1,20);
INSERT INTO BusDetails VALUES ('AM2','Amravati','Mumbai','20:00:00','20:30:00','12 hrs',2200,1,20);
INSERT INTO BusDetails VALUES ('PA1','Pune','Amravati','08:00:00','08:30:00','17 hrs',2000,1,20);
INSERT INTO BusDetails VALUES ('PA2','Pune','Amravati','20:00:00','20:30:00','15 hrs',2000,1,20);
INSERT INTO BusDetails VALUES ('AP1','Amravati','Pune','08:00:00','08:30:00','17 hrs',2000,1,20);
INSERT INTO BusDetails VALUES ('AP2','Amravati','Pune','20:00:00','20:30:00','15 hrs',2000,1,20);
INSERT INTO BusDetails VALUES ('MS1','Mumbai','Shirpur','08:00:00','08:30:00','12 hrs',1000,1,20);
INSERT INTO BusDetails VALUES ('MS2','Mumbai','Shirpur','20:00:00','20:30:00','10 hrs',1000,1,20);
INSERT INTO BusDetails VALUES ('SM1','Shirpur','Mumbai','08:00:00','08:30:00','12 hrs',1000,1,20);
INSERT INTO BusDetails VALUES ('SM2','Shirpur','Mumbai','20:00:00','20:30:00','10 hrs',1000,1,20);
INSERT INTO BusDetails VALUES ('PS1','Pune','Shirpur','08:00:00','08:30:00','12 hrs',800,1,20);
INSERT INTO BusDetails VALUES ('PS2','Pune','Shirpur','20:00:00','20:30:00','10 hrs',800,1,20);
INSERT INTO BusDetails VALUES ('SP1','Shirpur','Pune','08:00:00','08:30:00','12 hrs',800,1,20);
INSERT INTO BusDetails VALUES ('SP2','Shirpur','Pune','20:00:00','20:30:00','10 hrs',800,1,20);