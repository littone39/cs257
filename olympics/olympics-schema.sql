/*
Emily Litton
October 14, 2021
CS257: Software Design

This file contains commands to create tables from olympic data in sql. 

*/

/* NOC abreviations with country name */
CREATE TABLE noc_countries (
    noc text,
    country_name text);

/* olympic athletes */
CREATE TABLE athletes (
    id int,
    surname text,
    full_name text,
    sex text,
    age int,
    cm_height int,
    kg_weight float );

/* olympic event competition instances */
CREATE TABLE events (
    id int,
    noc text,
    sport text,
    event_competed text, 
    medal text );

/* connects event instances with athletes */ 
CREATE TABLE events_athletes (
    event_id int,
    athlete_id int);

/* all olympic games */
CREATE TABLE games (
    id serial,
    competition_year int,
    season text,
    city text);

/* connects events to games */
CREATE TABLE events_games (
    event_id int,
    game_id int);