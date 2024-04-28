create database airlinemysql;
use airlinemysql;

-- use IDENTITY(1,1) in case of SQL server
-- use AUTO_INCREMENT in case of MYSQL

-- Create the Airports table
CREATE TABLE Airports (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100)
);

-- Create the Routes table
CREATE TABLE Routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
	Arrival_airport_id INT NOT NULL,
	Departure_airport_id INT NOT NULL,
    FOREIGN KEY (Arrival_airport_id) REFERENCES Airports(airport_id),
	FOREIGN KEY (Departure_airport_id) REFERENCES Airports(airport_id)
);

Drop table Routes;

-- Create the Crew-Members table
CREATE TABLE Crew_Members (
    crew_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    experience INT CHECK (experience >= 0)
);

-- Create the Airlines table
CREATE TABLE Airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    website VARCHAR(255)
);

-- Create the Aircrafts table
CREATE TABLE Aircrafts (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    aircraft_type VARCHAR(255) NOT NULL,
    registration_number VARCHAR(255) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    airline_id INT,
    airport_id INT,
    FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
    FOREIGN KEY (airport_id) REFERENCES Airports(airport_id)
);

-- Create the Flights table
CREATE TABLE Flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(255) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    departure_city VARCHAR(255) NOT NULL,
    arrival_city VARCHAR(255) NOT NULL,
    route_id INT,
    aircraft_id INT,
    airline_id INT,
	FOREIGN KEY (route_id) REFERENCES Routes(route_id),
    FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
    FOREIGN KEY (aircraft_id) REFERENCES Aircrafts(aircraft_id)
);


-- Create the Passengers table
CREATE TABLE Passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255)
);

-- Create the Bookings table
CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_date DATETIME NOT NULL,
    payment_status BIT NOT NULL,
    flight_id INT,
    passenger_id INT,
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);

-- Create the Tickets table
CREATE TABLE Tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2),
    ticket_type VARCHAR(255) NOT NULL,
    seat_number VARCHAR(20)
);

-- Create the Payment table
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_method VARCHAR(255) NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL CHECK(payment_amount > 0),
    payment_date DATETIME NOT NULL
);

-- Create the Operates AT table
CREATE TABLE Operates_AT (
    airline_id INT,
    airport_id INT,
    PRIMARY KEY (airline_id, airport_id),
    FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
    FOREIGN KEY (airport_id) REFERENCES Airports(airport_id)
);

-- Create the Works For table
CREATE TABLE Works_For (
    crew_id INT,
    airline_id INT,
    flight_id INT,
    PRIMARY KEY (crew_id, airline_id, flight_id),
    FOREIGN KEY (crew_id) REFERENCES Crew_Members(crew_id),
    FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);

-- Create the Paid With table
CREATE TABLE Paid_With (
    booking_id INT,
    payment_id INT,
    ticket_id INT,
    PRIMARY KEY (booking_id, payment_id, ticket_id),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id),
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id),
    FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id)
);


DELIMITER //
CREATE FUNCTION total_flights_for_airlines (input_airline_name VARCHAR(255)) 
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE total_flights INT;
    
    -- Get the total number of flights operated by the given airline
    SELECT COUNT(*) INTO total_flights
    FROM Flights
    INNER JOIN Airlines ON Flights.airline_id = Airlines.airline_id
    WHERE Airlines.airline_name = input_airline_name;
    
    RETURN total_flights;
END//
DELIMITER ;

-- Create the view to display airlines with their total flights
CREATE VIEW AirlinesWithTotalFlights AS
SELECT 
    a.airline_id,
    a.airline_name,
    a.country,
    a.website,
    total_flights_for_airlines(a.airline_name) AS total_flights
FROM 
    Airlines a;

-- Insert data into the Airlines table
INSERT INTO Airlines (airline_name, country, website)
VALUES ('Example Airlines', 'United States', 'http://www.example.com'),
    ('Another Airline', 'Canada', 'http://www.anotherairline.com'),
    ('Yet Another Airline', 'Australia', 'http://www.yetanotherairline.com');


-- Select data from the view
SELECT * FROM AirlinesWithTotalFlights;

INSERT INTO Flights (flight_number, departure_time, arrival_time, departure_city, arrival_city, airline_id)
VALUES ('FL1234', '2023-12-01 06:00:00', '2023-12-01 09:00:00', 'New York', 'Los Angeles', 1);

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';
FLUSH PRIVILEGES;


-- Sample data for Airports table
INSERT INTO Airports (airport_name, city, country) VALUES
('John F. Kennedy International Airport', 'New York City', 'United States'),
('Los Angeles International Airport', 'Los Angeles', 'United States'),
('Heathrow Airport', 'London', 'United Kingdom'),
('Charles de Gaulle Airport', 'Paris', 'France');

-- Sample data for Crew_Members table
INSERT INTO Crew_Members (first_name, last_name, position, experience) VALUES
('John', 'Doe', 'Pilot', 10),
('Jane', 'Smith', 'Co-Pilot', 8),
('Michael', 'Johnson', 'Flight Attendant', 5),
('Emily', 'Brown', 'Flight Attendant', 3);

-- Sample data for Aircrafts table
INSERT INTO Aircrafts (aircraft_type, registration_number, capacity, airline_id, airport_id) VALUES
('Boeing 737', 'N123AB', 150, 1, 1),
('Airbus A320', 'G456CD', 180, 2, 2),
('Boeing 747', 'F789EF', 400, 3, 3),
('Airbus A380', 'H101IJ', 550, 4, 4);

-- Sample data for Flights table
INSERT INTO Flights (flight_number, departure_time, arrival_time, departure_city, arrival_city, route_id, aircraft_id, airline_id) VALUES
('EK001', '2024-05-01 08:00:00', '2024-05-01 15:00:00', 'New York City', 'London', 1, 1, 1),
('AA101', '2024-05-02 09:00:00', '2024-05-02 12:00:00', 'Los Angeles', 'New York City', 2, 2, 1),
('AF301', '2024-05-04 11:00:00', '2024-05-04 14:00:00', 'Paris', 'New York City', 3, 3, 3);

-- Sample data for Passengers table
INSERT INTO Passengers (first_name, last_name, phone_number, email) VALUES
('Alice', 'Johnson', '1234567890', 'alice@example.com'),
('Bob', 'Smith', '9876543210', 'bob@example.com'),
('Charlie', 'Brown', '4567890123', 'charlie@example.com'),
('David', 'Miller', '7890123456', 'david@example.com');

-- Sample data for Bookings table
INSERT INTO Bookings (booking_date, payment_status, flight_id, passenger_id) VALUES
('2024-04-28 10:00:00', 1, 1, 1),
('2024-04-29 11:00:00', 1, 2, 2),
('2024-04-30 12:00:00', 1, 3, 3);

-- Sample data for Tickets table
INSERT INTO Tickets (price, ticket_type, seat_number) VALUES
(500.00, 'Economy', 'A123'),
(700.00, 'Business', 'B456'),
(900.00, 'First Class', 'C789'),
(600.00, 'Economy', 'D012');

-- Sample data for Payment table
INSERT INTO Payment (payment_method, payment_amount, payment_date) VALUES
('Credit Card', 500.00, '2024-04-28 10:00:00'),
('Credit Card', 700.00, '2024-04-29 11:00:00'),
('Credit Card', 900.00, '2024-04-30 12:00:00'),
('Credit Card', 600.00, '2024-05-01 13:00:00');

-- Sample data for Operates AT table
INSERT INTO Operates_AT (airline_id, airport_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4);

-- Sample data for Works For table
INSERT INTO Works_For (crew_id, airline_id, flight_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 3, 4);

-- Sample data for Paid With table
INSERT INTO Paid_With (booking_id, payment_id, ticket_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- Sample data for Routes table
INSERT INTO Routes (Arrival_airport_id, Departure_airport_id) VALUES
(1, 2), 
(2, 1), 
(1, 3),
(3, 1); 


Alter table Bookings 
Modify column payment_status INT NOT NULL;

Alter table Bookings 
ADD constraint payment_status check(payment_status in (1 ,0))
