'''
Emily Litton, Jayti Arora 
CS257: final project

 name,year,life_ladder,gdp,social_support,life_expectancy,freedom,
        generosity,corruption,pos_affect,neg_affect
 Country name0,Regional indicator1,Ladder score2,Standard error of 
 ladder score3,upperwhisker4,lowerwhisker5,Logged GDP per capita6,
 Social support7,Healthy life expectancy8,Freedom to make life choices9,
 Generosity10,Perceptions of corruption11,Ladder score in Dystopia12,
 Explained by: Log GDP per capita13,Explained by: Social support14,
 Explained by: Healthy life expectancy15,Explained by: Freedom to make life choices16,
 Explained by: Generosity17,Explained by: Perceptions of corruption,Dystopia + residual
    
'''

import csv 

report_all_years = open('world-happiness-report.csv', 'r')
read_happy_data = csv.reader(report_all_years)
next(read_happy_data)

report_2021 = open('world-happiness-report-2021.csv')
read_2021_data = csv.reader(report_2021)
next(read_2021_data)

happiness_file = open('world-happiness.csv', 'w')
happiness_writer = csv.writer(happiness_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

country_file = open('country_data.csv', 'w')
country_writer = csv.writer(country_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

# keeps track of all countries already seen
countries = {}
country_id = 0

for entry in read_2021_data:
    country_id += 1
    countries[entry[0]] = country_id

    country_to_write = [country_id, entry[0], entry[1]]
    country_writer.writerow(country_to_write)
    year_to_write = [country_id, 2021, entry[2], entry[6],entry[7],entry[8],entry[9],entry[10],entry[11],'NULL', 'NULL']
    happiness_writer.writerow(year_to_write)

for entry in read_happy_data:
    for i in range(11):
        if entry[i] == '':
            entry[i] = 'NULL'
    if entry[0] not in countries:
        country_id +=1
        countries[entry[0]] = country_id
        country_writer.writerow([country_id, entry[0], 'NULL'])
        id = country_id
    else:
        id = countries[entry[0]]
    
    happiness_writer.writerow([id] + entry[1:])

country_file.close()
happiness_file.close()