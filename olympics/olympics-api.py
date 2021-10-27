#!/usr/bin/env python3
'''
    olympics-api.py
    Emily Litton, 26 October 2021

    Flask api implementation for olympic data from olympics.sql. 
'''

import flask
import json
import psycopg2
import argparse
from config import database, user, password

# Establishing a connection to the database
try:
    connection = psycopg2.connect(database=database, user=user, password=password)
    cursor = connection.cursor()
except Exception as e:
    print(e)
    exit()

app = flask.Flask(__name__)

@app.route('/games')
def get_games():
    ''' Returns a JSON list of dictionaries that represent individial olympic games. Includes
    information about the year, season, and city the games were held in. '''
    query = 'SELECT * FROM games;'
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    games_list = []
    for game in cursor:
        game_info = {'id':int(game[0]), 'year':int(game[1]), 'season':game[2], 'city':game[3]}
        games_list.append(game_info)
    
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    ''' Returns a JSON list of dictionaries that represent noc abreviation and corresponding full
    name. '''
    query = '''SELECT * FROM noc_countries
                ORDER BY noc;'''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    nocs_list = []
    for noc in cursor:
        noc_info = {'abreviation':noc[0], 'name':noc[1]}
        nocs_list.append(noc_info)
    
    return json.dumps(nocs_list)

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    '''Returns a JSON list of dictionaries, each representing one athlete
        and the medal they earned in the specified games. If noc is spefified
        in the url, only athletes from that noc will be in the returned list '''
    noc = flask.request.args.get('noc')
    games_id = int(games_id)
    if noc is not None:
        query = '''SELECT athletes.id, athletes.full_name, athletes.sex, events.sport, events.event_competed, performances.medal
                    FROM performances, games, athletes, events
                    WHERE games.id = %s
                    AND performances.athlete_id = athletes.id
                    AND performances.event_id = events.id
                    AND performances.game_id = games.id
                    AND performances.noc LIKE %s
                    AND performances.medal LIKE %s;'''
        try:
            cursor.execute(query, (games_id, noc, '%'))
        except Exception as e:
            print(e)
            exit()
    else:
        query = '''SELECT athletes.id, athletes.full_name, athletes.sex, events.sport, events.event_competed, performances.medal
                    FROM performances, games, athletes, events
                    WHERE games.id = %s
                    AND performances.athlete_id = athletes.id
                    AND performances.event_id = events.id
                    AND performances.game_id = games.id
                    AND performances.medal LIKE %s;'''
        try:
            cursor.execute(query, (games_id,'%'))
        except Exception as e:
            print(e)
            exit()
    
    medalist_list = []
    for medalist in cursor:
        medalist_info = {'athlete_id':int(medalist[0]), 'athlete_name':medalist[1], \
            'athlete_sex':medalist[2], 'sport':medalist[3], 'event':medalist[4], 'medal':medalist[5]}
        medalist_list.append(medalist_info)
    
    return json.dumps(medalist_list)

   
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)