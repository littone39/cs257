/*
Emily Litton 
October 14, 2021
This file contains commands to create tables from olympic data in sql. 
*/

CREATE TABLE noc_regions (
    id SERIAL,
    abreviation text,
    country_name text,
);

CREATE TABLE athletes {
    id int,
    full_name text;
    sex text;
    age int;
    cm_height int;
    kg_weight int;
    noc text;
}

CREATE TABLE events {
    athlete_id int;
    competition_year int;
    season text;
    city text;
    sport text;
    event_competed text;
    medal text;
}