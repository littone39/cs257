'''
    app.py
    Emily Litton, Jayti Arora
    11 November 2021

    A small Flask application that provides a barelywebsite with an accompanying
    API (which is also tiny) to support that website.
'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/')

@app.route('/') 
def home():
    return flask.render_template('index.html')

@app.route('/chart')
def chart():
    return flask.render_template('chart.html')

# @app.route('/about')
# def about():
#     return flask.render_template('about.html')

# for some reason the above route breaks (error 404 page not found)
@app.route('/about-us')
def about_us():
    return flask.render_template('about.html')

@app.route('/map')
def map():
    return flask.render_template('map.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A world-happiness application, including API & DB')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
