/*
Emily Litton 
October 14, 2021
This file contains commands to create tables from olympic data in sql. 
*/

CREATE TABLE noc_countries (
    noc text,
    country_name text);

CREATE TABLE athletes (
    id int,
    last_name text,
    full_name text,
    sex text,
    age int,
    cm_height int,
    kg_weight float,
    noc text);

CREATE TABLE events (
    athlete_id int,
    competition_year int,
    season text,
    city text,
    sport text,
    event_competed text,
    medal text);