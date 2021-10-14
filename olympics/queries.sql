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

SELECT athletes.full_name, noc_countries.country_name 
FROM athletes, events, noc_countries, events_athletes
WHERE noc_countries.country_name LIKE 'Kenya'
AND noc_countries.noc = events.noc
AND athletes.id = events_athletes.athlete_id
AND events.id = events_athletes.event_id
ORDER BY athletes.surname;

SELECT athletes.full_name, events.medal, 
    events.event_competed, games.city, games.competition_year
FROM athletes, events, games, events_athletes, events_games
WHERE athletes.surname LIKE 'Louganis'
AND athletes.id = events_athletes.athlete_id
AND events.id = events_athletes.event_id
AND events.id = events_games.event_id
AND games.id = events_games.game_id
AND events.medal LIKE '%'
ORDER BY games.competition_year;

SELECT noc_countries.noc, COUNT(events)
FROM noc_countries, events
WHERE events.medal LIKE 'Gold'
AND noc_countries.noc = events.noc
GROUP BY noc_countries.noc
ORDER BY COUNT(events) DESC;
