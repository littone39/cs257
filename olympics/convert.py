'''
Emily Litton
October 14, 2021
This program converts raw olympic data csv files to csv files organized to load the 
data into SQL database. 

The files have lines with the following format:
athlete_events.csv: ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
noc_regions.csv: [NOC, Country, Notes]
athletes.csv: [ID, Surname, Full Name, Sex, Age, Height, Weight, NOC], 
events.csv: [Athlete ID, Year, Season, City, Sport, Event, Medal]
noc_countries.csv: [NOC, Country]
'''
import csv

with open('athlete_events.csv', 'r') as csvfile:
    readdata = csv.reader(csvfile)
    next(readdata)
    athlete_names =[]
    ev_added = 0
    ath_added = 0
    with open('athletes.csv', 'w') as athlete_file:
        athlete_writer = csv.writer(athlete_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open('events.csv', 'w') as event_file:
            event_writer = csv.writer(event_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in readdata:
                for i in range(len(row)):
                    if row[i] == 'NA':
                        row[i] = 'NULL'
                event_writer.writerow([row[0], row[9], row[10], row[11], row[12], row[13], row[14]])
                ev_added += 1 
                surname = row[1].split(' ')[-1]
                if row[1] not in athlete_names:
                    athlete_writer.writerow([row[0], surname, row[1], row[2], row[3], row[4], row[5], row[7]])
                    athlete_names.append(row[1])
                    ath_added += 1
        event_file.close()
    athlete_file.close()

csvfile.close()

# file with corresponding noc and country names
with open('noc_regions.csv') as noc_regions:
    readdata = csv.reader(noc_regions)
    next(readdata)
    with open('noc_countries.csv', 'w') as noc_countries:
        noc_writer = csv.writer(noc_countries, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in readdata:
            noc_writer.writerow([row[0], row[1]])
    noc_countries.close()
noc_regions.close()







