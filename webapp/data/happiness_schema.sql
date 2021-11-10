CREATE TABLE countries (
    id serial,
    country_name text,
    region text
)

CREATE TABLE world_happiness(
    country_id int,
    year int,
    life_ladder float,
    gdp float,
    social_support float,
    life_expectancy float,
    freedom float,
    generosity float,
    percieved_corruption float,
    positive_affect float,
    negative_affect float
)


