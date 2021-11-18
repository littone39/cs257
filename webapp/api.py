'''
    api.py
    Emily Litton, Jayti Arora 
    11 November 2021

    Flask API to support the happiness web application.
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

@api.route('/api/help')
def help():
    help_text = open('api_help.txt').read()
    return flask.Response(help_text, mimetype='text/plain')

@api.route('/countries/') 
def get_countries():
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

##### this only works with new data.sql #####
# @api.route('/countries/happiness')
# def get_all_happiness():
#     ''' returns a list of dictionaries containing country code and life_ladder (happiness) score '''
#     query = '''SELECT country_abbreviations.abbreviation, world_happiness.life_ladder
#             FROM country_abbreviations, world_happiness, countries
#             WHERE country_abbreviations.country_name = countries.country_name
#             AND countries.id = world_happiness.country_id 
#             AND world_happiness.year = 2021; '''
#     happiness_list = []
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         cursor.execute(query)
#         for row in cursor:
#             entry = {'id':row[0],'life_ladder':row[1]}
#             happiness_list.append(entry)
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         print(e, file=sys.stderr)

#     return json.dumps(happiness_list)

@api.route('/country/<country_name>')
def get_country(country_name):
    ''' returns happiness score for one country for all years provided '''
    # maybe change to:
    # query = select * from world_happiness where country_id = %s
    query = '''SELECT  * FROM world_happiness, countries
            WHERE countries.country_name = %s 
            AND countries.id = world_happiness.country_id 
            ORDER BY year;'''
    happiness_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (country_name,))
        for row in cursor:
            entry = {'id':row[0],'life_ladder':row[2], 'year':row[1], 'gdp':row[3], \
            'social_support':row[4], 'life_expectancy':row[5], 'freedom':row[6], \
                'generosity':row[7], 'percieved_corruption':row[8], 'positive_affect':row[9],\
                    'negative_affect':row[10]}
            happiness_list.append(entry)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(happiness_list)

@api.route('/graph/<x_axis>/<y_axis>')
def get_graph_coords(x_axis, y_axis):
    ''' Takes in two variables and returns a list of all countries and their 
    data corresponding to those two variables for the year 2021. (i.e. .../graph/life_ladder/gdp
    would return somehting like [{country_name:"Afghanistan", "x":5.7, "y":9.1}...] for all countries.'''
    var_list = ['country_id', 'year','life_ladder','gdp','social_support','life_expectancy','freedom', \
        'generosity', 'percieved_corruption','positive_affect','negative_affect']
    
    if x_axis not in var_list or y_axis not in var_list:
        return json.dumps([])
    
    query = 'SELECT world_happiness.country_id,' + x_axis + ',' + y_axis + \
        ' FROM world_happiness WHERE year = 2021;'

    coords = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            print(row)
            coordinate = {'id':row[0], 'x':row[1], 'y':row[2]}
            coords.append(coordinate)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(coords)

