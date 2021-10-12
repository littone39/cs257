/* 
Emily Litton
October 14, 2021

This file contains the following queries.

list abreviations alphabetically 
list all athletes from Kenya sorted by last name
list all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.
list all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
*/

SELECT noc_countries.noc FROM noc_countries;

SELECT athletes.full_name, noc_countries.country_name 
FROM athletes, noc_countries
WHERE noc_countries.country_name LIKE 'Kenya'
AND noc_countries.noc = athletes.noc
ORDER BY athletes.last_name;


SELECT athletes.full_name, events.medal, 
    events.event_competed, events.city, events.competition_year
FROM athletes, events
WHERE athletes.last_name LIKE 'Louganis'
AND athletes.id = events.athlete_id
AND events.medal LIKE '%'
ORDER BY events.competition_year;

SELECT noc_countries.noc, COUNT(events)
FROM noc_countries, events
WHERE events.medal LIKE 'Gold'
GROUP BY noc_countries.noc
ORDER BY COUNT(events) DESC;
