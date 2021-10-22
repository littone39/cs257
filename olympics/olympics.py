'''
olympics.py
Emily Litton, October 20, 2021

This program is a command line interface for the olympics database (found in olympics.sql). Usage 
for this CLI is specified in usage.txt. The functions required for the assignment can be accessed 
via the following commands:

1) print usage: 
    python3 olympics.py -h
2) list names of athletes from specified NOC (NOC_string): 
    python3 olympics.py -a <NOC_string>
3) list NOCs and number of gold medals they have won in descending order: 
    python3 olympics.py -m
4) other functionalities (see usage.txt for specifics):
    - list all the events associated with specified sport
    - list NOCs and number of silver or bronze medals won in descending order
'''

import psycopg2
from config import database
from config import user
from config import password
import argparse

class OlympicSearchDispatcher:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database=database, user=user, password=password)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            exit()

    def search_NOC_olympians(self, noc):
        ''' searches database for athletes from a specified noc and prints 
        that list of athletes. If no NOC is specified, an error message and 
        usage statement is printed. '''
        if noc is None:
            print('Please specify an NOC to see corresponding athletes.')
            self.print_usage()

        else:
            noc_string = noc.lower()
            query = '''SELECT DISTINCT athletes.full_name, performances.noc 
                    FROM athletes, performances, noc_countries
                    WHERE athletes.id = performances.athlete_id
                    AND LOWER(performances.noc) LIKE %s
                    ORDER BY athletes.full_name;'''
            try:
                self.cursor.execute(query, (noc_string,))
            except Exception as e:
                print(e)
                exit()

            print('===== Athletes who competed for {0} ====='.format(noc_string))
            for row in self.cursor:
                print(row[0], row[1])

    def search_sport_events(self, sport):
        ''' searches database for events that were competed in a given sport and prints a list
        of those events. '''
        if sport is None:
            self.print_usage()
        
        sport_string = sport.lower()
        query = '''SELECT events.event_competed 
                    FROM events
                    WHERE LOWER(events.sport) LIKE %s 
                    ORDER BY events.event_competed'''
        try:
            self.cursor.execute(query, (sport_string,))
        except Exception as e:
            print(e)
            exit()
        
        print('===== {0} Events ====='.format(sport_string))
        for row in self.cursor:
            print(row[0])

    def search_NOC_medals(self, medal='gold'):
        ''' prints a list of nocs and their medal counts 
        for a given medal color (defaults to gold if no medal color provided)
        prints error message and usage statement if medal color is not 'gold', 'silver'
        or 'bronze' (case-insensitive). '''
        medal_color = medal.lower()
        if medal_color not in ['gold', 'silver', 'bronze']:
            print('''Invalid medal type, please try again with "gold", "silver", "bronze" or 
                    specify no color to print gold medal counts.''')
            self.print_usage()
        
        query = '''SELECT performances.noc, COUNT(performances.medal)
                    FROM performances
                    WHERE LOWER(performances.medal) LIKE %s
                    GROUP BY performances.noc
                    ORDER BY COUNT(performances.noc) DESC;'''
        try:
            self.cursor.execute(query, (medal_color, ))
        except Exception as e:
            print(e)
            exit()
        
        print('===== NOCs and {0} medal count====='.format(medal_color))
        for row in self.cursor:
            print(row[0], row[1])

    def print_usage(self):
        ''' prints usage statement from usage.txt '''
        usage = open('usage.txt', 'r')
        usage_statement = usage.read()
        print(usage_statement)
        exit()

    def get_parsed_arguments(self):
        parser = argparse.ArgumentParser(description='Searches olympic database', add_help=False)
        parser.add_argument('-a', '--athletes', nargs='?', default=None, const=None, help='tag for searching NOC athletes')
        parser.add_argument('-m', '--medals', nargs='?', default=None, const='gold', help='tag for searching NOC medal counts')
        parser.add_argument('-e','--events', nargs='?', default=None, help='tag for searching sport events')
        parser.add_argument('-h', '--help', action='store_true', help='tag for usage help')
        parsed_args = parser.parse_args()
        return parsed_args

def main():
    ''' Creates instance of OlympicSearchDispatcher, and using that instance, parses command line 
        arguments, executes search, and prints error messages/usage statement
        as necessary (functionality described in usage.txt). '''
    dispatcher = OlympicSearchDispatcher()
    arguments = dispatcher.get_parsed_arguments()
   
    if arguments.athletes is not None:
        dispatcher.search_NOC_olympians(arguments.athletes)

    elif arguments.medals is not None:
        dispatcher.search_NOC_medals(arguments.medals)

    elif arguments.events is not None:
        dispatcher.search_sport_events(arguments.events)

    else: 
        dispatcher.print_usage()

    dispatcher.connection.close() # close connection to database
    
if __name__ == '__main__':
    main()


