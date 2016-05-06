"""
Module that implements a REST API as described by Elo7 to help
engineers to closely monitor the deployment times step-by-step.

"""

import logging
import MySQLdb

from time import gmtime, strftime
from datetime import datetime
from flask import Flask, jsonify, make_response, request
from steps_logging import setup_logging
from config import read_config
import db


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


def db_save_step(db_conn, step_data):
    """
    Saves the deployment step data into a database.

    Args:
       db_conn: db connection
       step_data: a dict containing the supplied user data about the step
    """

    cursor = db_conn.cursor()

    # Build the SQL columns and values list with the step data
    col_list = ",".join(step_data.iterkeys())
    values_list = "','".join(step_data.itervalues())
    values_list = "'" + values_list + "'"

    # Try to insert the new schedule into the database. If it fails, return
    # -1, otherwise, return the scheduled job id.
    sql = "INSERT INTO steps(%s) " \
        "VALUES(%s)" % (col_list, values_list)

    logging.debug("Saving step: %s", sql)

    try:
        cursor.execute(sql)

    except Exception as e:
        logging.critical("Error when saving job into DB: %s", str(e))
        return -1


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

    # Add a timestamp (UTC) to the dict to be stored into DB
    values["ts"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    logging.debug("is_missing=%s, values=%s" % (is_missing, values))

    # Try to store the dict into the database
    try:
        db_save_step(db_conn, values)

    except Exception as e:
        return make_response(
            jsonify({'Error': 'Something went wrong when updating DB - %s' % str(e)}), 500)

    # Return a json confirming the update
    return jsonify(values), 201


def csv_format(cursor):
    """
    Gets the cursor content (row by row) and returns a corresponding CSV output format
    in a string
    """

    # For each row, appends the output in CSV
    is_first_row = True
    res = ""
    for row in cursor:
        # Gets the column names in a CSV format if it's the first row
        if is_first_row:
            res = ",".join(str(row) for row in row.iterkeys())
            res += "\n"
            is_first_row = False

        # Collects the row values
        res += ",".join(str(row) for row in row.itervalues()) + "\n"

    return res


def valid_date_format(candidate):
    """
    Checks if the supplied string contains a valid date/time (that follows
    the YYYY-MM-DD HH:MM:SS format). Returns true if so (or if the string is
    null or empty), false otherwise.
    """

    # If candidate is None, return true
    if not candidate:
        return True

    # Verify if time format is ok and stores in into a time-tuple format
    try:
        stime = datetime.strptime(candidate, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False
    else:
        return True


def get_where_clause(request):
    """
    Builds a SQL WHERE clause corresponding to parameters passed in with a GET
    /v1/steps?parameters=xx request.

    Args:
        request: a Flask request object containing the parameters passed

    Return:
        A string (like " WHERE xx=yy") containing a WHERE clause to be appended
        to a SQL query. If no parameters were passed, an empty string is returned.
    """

    clause = ""

    if request.args.get("component"):
        clause += "component='%s' AND " % request.args.get("component")

    if request.args.get("owner"):
        clause += "owner='%s' AND " % request.args.get("owner")

    if request.args.get("start_datetime"):
        clause += "ts>='%s' AND " % request.args.get("start_datetime")

    if request.args.get("end_datetime"):
        clause += "ts<='%s'" % request.args.get("end_datetime")

    # Remove the hanging "AND " if necessary
    if clause[-4:] == "AND ":
        clause = clause[:-4]

    if clause != "":
        clause = " WHERE " + clause

    logging.debug("Clause=%s" % clause)
    return clause


@app.route('/v1/steps', methods=['GET'])
def list_steps():
    """
    This function handles the GET /v1/steps?format=csv|json&component=cc&\
    start_datetime=yyyy-mm-dd hh:mm:ss&end_datetime=yyyy-mm-dd hh:mm:ss requests.
    All parameters are optional.

    As a result, it returns a list of deployments steps in the specified format
    (defaults to csv). A full list is returned unless other parameters are specified.
    """

    # Check if supplied dates (if any) are in the expected format
    if not (valid_date_format(request.args.get("start_datetime")) and
            valid_date_format(request.args.get("end_datetime"))):
        return make_response(jsonify(
            {'Error': 'Datetimes must follow the YYYY-MM-DD HH:MM:SS format'}), 400)

    # Based on the supplied parameters, build and execute the SQL query against
    # the database to get the required list of deployment steps
    cursor = db_conn.cursor(MySQLdb.cursors.DictCursor)
    where_clause = get_where_clause(request)
    cursor.execute("SELECT * FROM steps" + where_clause)

    # Output using the proper format
    if request.args.get("format") == "json":
        return jsonify(steps=cursor.fetchall()), 200
    else:
        return csv_format(cursor), 200


@app.errorhandler(404)
def not_found(error):
    """
    404 handler
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


def empty_db(db_conn):
    """
    Empties the DB.
    """

    cursor = db_conn.cursor()
    cursor.execute("TRUNCATE steps")



def main():
    """ Main """

    global db_conn

    CONFIG_FILE = "config.yml"
    config = read_config(CONFIG_FILE)
    logging.debug("Config read: %s", config)

    setup_logging(config["log"])

    db_conn = db.open_connection(config["db"])

    app.run(host='0.0.0.0')


if __name__ == '__main__':
    db_conn = None
    main()

