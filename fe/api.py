"""
Module that implements a REST API as described by Elo7 to help
engineers to closely monitor the deployment times step-by-step.

"""

import logging
import MySQLdb

from time import gmtime, strftime
from datetime import datetime
from flask import Flask, jsonify, make_response, request, g
from steps_engine.steps_logging import setup_logging
from steps_engine.config import read_config
import steps_engine.db
from my_date import Date
from steps_engine.step import Step


# Instantiates a Flask app
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Handles the / request. Just to check the sevice is alive.
    """
    return 'Hello World!\n'


def verify_parameters(request, list_mandatory_parameters):
    """
    Verifies if all the expected/mandatory parameters were actually passed in
    a given http request.

    Args:
        request: a Flask request object (containing the http parameters)

    Return:
        Two elements. The first one is boolean saying if all expected parameters are
        present; if not, the second element is a name of a missing parameter, otherwise an
        additional dict is returned with the supplied values.
    """

    values = {}

    for parameter in list_mandatory_parameters:
        values[parameter] = request.args.get(parameter)
        if values[parameter] is None:
            return True, parameter

    return False, values



@app.route('/v1/steps', methods=['POST'])
def process_deployment_step():
    """
    Handles the POST /v1/steps/?status=xxx&component=yyy&version=zzz&owner=www&status=sss
    request.

    ALL paramaters are mandatory.

    """

    # Store the provided parameters into a dict ("values") and check
    # if any mandatory one is missing
    is_missing, values = verify_parameters(request, ["status", "component",
                                                     "version", "owner"])

    # Return an error message if any mandatory parameter is missing
    if is_missing:
        return make_response(jsonify({'Error':
                                      'Missing %s parameter' % values}), 400)
    
    step = Step(values)

    logging.debug("is_missing=%s, values=%s" % (is_missing, values))

    # Try to store the dict into the database
    try:
        step.db_save(g.db)


    except Exception as e:
        return make_response(
            jsonify({'Error': 'Something went wrong when updating DB - %s' % str(e)}), 500)

    # Return a json confirming the update
    return jsonify(values), 201



@app.route('/v1/steps', methods=['GET'])
def list_steps():
    """
    This function handles the GET /v1/steps?format=csv|json&component=cc&\
    start_datetime=yyyy-mm-dd hh:mm:ss&end_datetime=yyyy-mm-dd hh:mm:ss requests.
    All parameters are optional.

    As a result, it returns a list of deployments steps in the specified format
    (defaults to csv). A full list is returned unless other parameters are specified.
    """
    result, http_code =  Step.list(request)
    return result, http_code


@app.errorhandler(404)
def not_found(error):
    """
    404 handler
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.before_request
def before_request():
    """
    Before each http request, open a connection to the database according
    the configured paramaters.
    """
    g.db = steps_engine.db.open_connection(config["db"])

@app.teardown_request
def teardown_request(exception):
    """ 
    After the completion of each http request, closes the database
    connection.
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def empty_db(db_conn):
    """
    Empties the DB.
    """

    cursor = db_conn.cursor()
    cursor.execute("TRUNCATE steps")



def main():
    """ Main """

    global config

    CONFIG_FILE = "config.yml"
    config = read_config(CONFIG_FILE)
    logging.debug("Config read: %s", config)

    setup_logging(config["log"])

    app.debug = True
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    config = None
    main()

