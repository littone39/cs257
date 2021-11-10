'''
Emily Litton, Jayti Arora 
CS257: final project
'''

import csv 

csvfile = open('world-happiness-report.csv', 'r')
readdata = csv.reader(csvfile)
next(readdata)

# country_ids = {}
outfile = open('happiness-report.csv', 'w')
happiness_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       

for country_line in readdata:
    for i in range(11):
        if country_line[i] == '':
            country_line[i] = 'NULL'
    name,year,life_ladder,gdp,social_support,life_expectancy,freedom,\
        generosity,corruption,pos_affect,neg_affect = [country_line[i] for i \
            in [0,1,2,3,4,5,6,7,8,9,10]]

    happiness_writer.writerow([name,year,life_ladder,gdp,social_support,life_expectancy,freedom,\
        generosity,corruption,pos_affect,neg_affect])

csvfile.close()
outfile.close()