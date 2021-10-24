/*
Emily Litton
October 14, 2021
CS257: Software Design

This file contains commands to create tables from olympic data in sql. 
 
*/

CREATE TABLE noc_countries (
    noc text,
    country_name text);

CREATE TABLE athletes (
    id int,
    surname text,
    full_name text,
    sex text );

CREATE TABLE events (
    id int,
    sport text,
    event_competed text);

CREATE TABLE games (
    id int,
    competition_year int,
    season text,
    city text);

CREATE TABLE performances (
    athlete_id int,
    event_id int,
    game_id int,
    cm_height int, 
    kg_weight float, 
    noc text, 
    medal text
);