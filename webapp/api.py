'''
    api.py
    Emily Litton, Jayti Arora 
    11 November 2021

    Flask API to support the tiny happiness web application.
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/countries/') 
def get_authors():
    ''' Returns a list of all the countries in our database. 

        By default, the list is presented in alphabetical order
        by country name.

    '''
    query = '''SELECT id, country_name from countries ORDER BY country_name'''

    country_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            country = {'id':row[0], 'country_name':row[1]}
            country_list.append(country)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(country_list)

@api.route('/country/<country_id>')
def get_books_for_author(country_id):
    ''' returns happiness score for one country for all years provided '''
    query = '''SELECT  countries.country_name, world_happiness.life_ladder,world_happiness.year, world_happiness.gdp, 
                    world_happiness.social_support, world_happiness.life_expectancy, world_happiness.freedom 
            FROM countries, world_happiness 
            WHERE countries.id = world_happiness.country_id 
            AND countries.id = %s order by year;'''
    happiness_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (country_id,))
        for row in cursor:
            entry = {'name':row[0],'life_ladder':row[1], 'year':row[2], 'gdp':row[3], \
            'social_support':row[4], 'life_expectancy':row[5], 'freedom':row[6]}
                # 'generosity':row[7], 'percieved_corruption':row[8], 'positive_affect':row[9],\
                #     'negative_affect':row[10]}
            happiness_list.append(entry)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(happiness_list)

