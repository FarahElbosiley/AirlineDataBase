create database airlinemysql;
use airlinemysql;
-- Create the Routes table
CREATE TABLE Routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY
);

-- Create the Airports table
CREATE TABLE Airports (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100)
);

-- Create the Crew-Members table
CREATE TABLE Crew_Members (
    crew_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    experience INT CHECK (experience >= 0)
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
    FOREIGN KEY (route_id) REFERENCES Routes(route_id),
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
    payment_status ENUM('0', '1'),
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
    seat_number VARCHAR(20),
    booking_id INT,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
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
    capacity INT NOT NULL,
    airline_id INT,
    airport_id INT,
    FOREIGN KEY (airline_id) REFERENCES Airlines(airline_id),
    FOREIGN KEY (airport_id) REFERENCES Airports(airport_id)
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

-- Create a MySQL function
DELIMITER $$

CREATE FUNCTION total_flights_for_airline(input_airline_name VARCHAR(255)) RETURNS INT
BEGIN
    DECLARE total_flights INT;
    
    -- Get the total number of flights operated by the given airline
    SELECT COUNT(*) INTO total_flights
    FROM Flights
    INNER JOIN Airlines ON Flights.airline_id = Airlines.airline_id
    WHERE Airlines.airline_name = input_airline_name;
    
    RETURN total_flights;
END$$

DELIMITER ;
