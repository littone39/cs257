/* 
Emily Litton
October 14, 2021
CS257: Software Design

This file contains query commands for the olympics database.

1) list abreviations alphabetically 
2) list all athletes from Kenya sorted by last name
3) list all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.
4) list all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
*/

SELECT noc_countries.noc FROM noc_countries
ORDER BY noc_countries.noc;

SELECT DISTINCT athletes.surname, athletes.full_name, noc_countries.country_name 
FROM athletes, performances, noc_countries
WHERE athletes.id = performances.athlete_id
AND performances.noc = noc_countries.noc
AND noc_countries.country_name LIKE 'Kenya'
ORDER BY athletes.surname;

SELECT athletes.full_name, performances.medal, events.event_competed, games.competition_year
FROM athletes, performances, games, events
WHERE athletes.surname LIKE 'Louganis'
AND athletes.id = performances.athlete_id
AND performances.medal LIKE '%'
AND performances.game_id = games.id
AND performances.event_id = events.id
ORDER BY games.competition_year;

SELECT performances.noc, COUNT(performances.medal)
FROM performances
WHERE performances.medal LIKE 'Gold'
GROUP BY performances.noc
ORDER BY COUNT(performances.noc) DESC;
