/*
Emily Litton
October 14, 2021
CS257: Software Design

This file contains commands to create tables from olympic data in sql. 
Edits:
- take height and weight out of athletes and put it in events 
- abstract olympic events
- have one table with PERFORMANCES ? 

noc_countries (noc, country)
athletes (id, name, sex)
events (id, sport, event)
games (id, season, year, city)
performances (athlete_id, event_id, games_id, medal, height, weight, noc)

SELECT athletes.name, noc_countries.country
FROM athletes, performances, noc_countries
WHERE performances.athlete_id = athletes.id
AND performances.noc = noc_countries.noc
AND noc_countries.country LIKE 'Kenya'
GROUP BY athletes.name
SORT BY athletes.surname;

SELECT athletes.name, performances.medal ...
FROM athletes, performances, games
WHERE athlete.surname LIKE 'Louganis'
AND athletes.id = performances.athlete_id
AND performances.medal LIKE '%'
AND performances.games_id = games.id
SORT BY games.year;

SELECT performances.noc, COUNT(performances.medal)
FROM performances,
WHERE performances.medal LIKE 'Gold'
GROUP BY performances.noc
SORT BY COUNT(performances.noc) DESC;

Questions:
- should i be looping through multiple times in convert.py? or is it fine that I'm just doing it all at once?
- what do you think of the above code
- when I was doing this, I thought it was counter intuitive bc it seems harder to query. should I be trying to 
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