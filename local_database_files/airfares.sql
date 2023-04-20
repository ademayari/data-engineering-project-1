﻿create schema airfares;
use airfares;

create table airline
(
    code    varchar(50) not null
        primary key,
    airline_name    varchar(50) not null,
    country varchar(50) not null
);

create table airport
(
    code    varchar(50) not null
        primary key,
    airport_name    varchar(50) not null,
    country varchar(20) not null
);

create table flight
(
    flight_id      varchar(100)               not null
        primary key,
    airline_code   varchar(50)               not null,
    departure      varchar(20) default 'BRU' not null,
    destination    varchar(20)               not null,
    departure_date date                     not null,
    departure_time time                      not null,
    arrival_date    date                    not null,
    arrival_time   time                      not null,
    duration        time                    not null,
    stops          int                       null,
    flightnumber    varchar(20)                 not null,
    constraint flight_ibfk_1
        foreign key (airline_code) references airline (code),
    constraint flight_ibfk_2
        foreign key (departure) references airport (code),
    constraint flight_ibfk_3
        foreign key (destination) references airport (code)
);

create index airline_code
    on flight (airline_code);

create index departure
    on flight (departure);

create index destination
    on flight (destination);

create table flight_data
(
    flight_data_id  int auto_increment not null unique,
    flight_id    varchar(100) not null,
    time_of_data date        not null,
    price        float       not null,
    seats_left   int         null,
    primary key (flight_data_id),
    constraint flight_data_ibfk_1
        foreign key (flight_id) references flight (flight_id)
);

INSERT INTO airline (code, airline_name, country) 
VALUES 
    ('SN', 'Brussels Airlines', 'Belgium'),
    ('HV', 'Transavia', 'Belgium'),
    ('FR', 'Ryanair', 'Belgium'),
    ('TB', 'TUI', 'Belgium');


INSERT INTO airport (code, airport_name, country) 
VALUES 
    ('ALC', 'Alicante–Elche Airport', 'Spain'),
    ('IBZ', 'Ibiza Airport', 'Spain'),
    ('AGP', 'Málaga Airport', 'Spain'),
    ('PMI', 'Palma de Mallorca Airport', 'Spain'),
    ('TCI', 'Tenerife–Ciudad de La Laguna Airport', 'Spain'),
    ('BDS', 'Brindisi – Salento Airport', 'Italy'),
    ('NAP', 'Naples International Airport', 'Italy'),
    ('PMO', 'Falcone–Borsellino Airport', 'Italy'),
    ('FAO', 'Faro Airport', 'Portugal'),
    ('HER', 'Heraklion International Airport', 'Greece'),
    ('RHO', 'Rhodes International Airport', 'Greece'),
    ('CFU', 'Corfu International Airport', 'Greece'),
    ('BRU', 'Brussels Airport', 'Belgium'),
    ('CRL', 'Brussels South Charleroi Airport', 'Belgium'),
    ('LGG', 'Liège Airport', 'Belgium'),
    ('OST', 'Ostend–Bruges International Airport', 'Belgium'),
    ('ANR', 'Antwerp International Airport', 'Belgium');