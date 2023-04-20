create table airline
(
    code    varchar(20) not null
        primary key,
    name    varchar(50) null,
    country varchar(20) null
);

create table airport
(
    code    varchar(20) not null
        primary key,
    name    varchar(50) null,
    country varchar(20) null
);

create table flight
(
    flight_id      varchar(20)               not null
        primary key,
    airline_code   varchar(20)               null,
    departure      varchar(20) default 'BRU' null,
    destination    varchar(20)               null,
    departure_time date                      null,
    arrival_time   date                      null,
    stops          int                       null,
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
    flight_id    varchar(20) not null,
    time_of_data date        not null,
    price        float       null,
    seats_left   int         null,
    primary key (flight_id, time_of_data),
    constraint flight_data_ibfk_1
        foreign key (flight_id) references flight (flight_id)
);

