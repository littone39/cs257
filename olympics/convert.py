'''
Emily Litton
October 14, 2021
This program converts raw olympic data csv files to csv files organized to load the 
data into SQL database. 

The following csv files have have the format:

READING
athlete_events.csv: ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
noc_regions.csv: [NOC, Country, Notes]

WRITING
athletes.csv: [ID, Surname, Full Name, Sex, Age, Height, Weight, NOC], 
events.csv: [ID, NOC, Sport, Event, Medal]
athletes_events.csv: [Athlete ID, Event ID]
games.csv: [ID, Year, Season, City]
events_games.csv: [Event ID, Game ID]
noc_countries.csv: [NOC, Country]
'''
import csv

with open('athlete_events.csv', 'r') as csvfile:
    readdata = csv.reader(csvfile)
    next(readdata)
    athlete_ids =[]
    oly_games = {}
    games_id = 0
    event_id = 0
    
    
    with open('athletes.csv', 'w') as athlete_f:
        athlete_writer = csv.writer(athlete_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open('events.csv', 'w') as events_f:
            event_writer = csv.writer(events_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            with open('events_athletes.csv', 'w') as athlete_event_f:
                athlete_event_writer = csv.writer(athlete_event_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open('games.csv', 'w') as games_f:
                    games_writer = csv.writer(games_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    with open('events_games.csv', 'w') as events_games_f:
                        events_games_writer = csv.writer(events_games_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        
                        for row in readdata:
                            for i in range(len(row)):
                                if row[i] == 'NA':
                                    row[i] = 'NULL'
                            athlete_id, full_name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal = row
                            event_id += 1
                            event_writer.writerow([event_id, noc, sport, event, medal]) #write event to file
                            athlete_event_writer.writerow([event_id, athlete_id]) #connect athlete id and event id
                            surname = full_name.split(' ')[-1] 
                            if len(surname) > 0:
                                if surname[0] == '(':
                                    surname = full_name.split(' ')[-2]

                            if athlete_id not in athlete_ids:
                                athlete_writer.writerow([athlete_id, surname, full_name, sex, age, height, weight]) #add athlete if not there
                                athlete_ids.append(athlete_id) 
                            if games not in oly_games.keys(): #add game if not already added and connect games with events
                                games_id += 1
                                games_writer.writerow([games_id, year, season, city]) 
                                oly_games[games] = games_id
                                events_games_writer.writerow([event_id, games_id]) 
                            else:
                                events_games_writer.writerow([event_id, oly_games[games]]) 
                                # get games id 

                    events_games_f.close()
                games_f.close()
            athlete_event_f.close()
        events_f.close()
    athlete_f.close()

csvfile.close()

# convert noc_regions.csv to new file noc_countries with just NOC abreviation and country name
with open('noc_regions.csv') as noc_regions:
    readdata = csv.reader(noc_regions)
    next(readdata)
    with open('noc_countries.csv', 'w') as noc_countries:
        noc_writer = csv.writer(noc_countries, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in readdata:
            noc_writer.writerow([row[0], row[1]])
    noc_countries.close()
noc_regions.close()







