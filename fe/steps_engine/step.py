"""
Module that implements a REST API as described by Elo7 to help
engineers to closely monitor the deployment times step-by-step.

"""

import logging
import MySQLdb

from time import gmtime, strftime
from flask import jsonify, make_response,  g
from steps_engine.my_date import Date


class Step(object):

    def __init__(self, values):

        self.component = values['component']
        self.version = values['version']
        self.owner = values['owner']
        self.status = values['status']
        self.ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def db_save(self, db_conn):
        """
        Saves the deployment step data into a database.

        Args:
           db_conn: db connection
        """

        # Build the SQL columns and values list with the step data
        col_list = "component, version, owner, status, ts"
        values_list = "'%s', '%s', '%s', '%s', '%s'" % (
            self.component, self.version, self.owner, self.status, self.ts)

        # Try to insert the new schedule into the database. If it fails, return
        # -1, otherwise, return the scheduled job id.
        sql = "INSERT INTO steps(%s) " \
            "VALUES(%s)" % (col_list, values_list)

        logging.debug("Saving step: %s", sql)

        try:
            db_conn.cursor().execute(sql)

        except Exception as e:
            logging.critical("Error when saving job into DB: %s", str(e))
            return -1

    @staticmethod
    def _csv_format(cursor):
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

    @staticmethod
    def _get_where_clause(request):
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

    @staticmethod
    def list(request):
        """
        This function handles the GET /v1/steps?format=csv|json&component=cc&\
        start_datetime=yyyy-mm-dd hh:mm:ss&end_datetime=yyyy-mm-dd hh:mm:ss requests.
        All parameters are optional.

        As a result, it returns a list of deployments steps in the specified format
        (defaults to csv). A full list is returned unless other parameters are specified.
        """

        #  Check if supplied dates (if any) are in the expected format
        if not (Date(request.args.get("start_datetime")).valid_format() and
                Date(request.args.get("end_datetime")).valid_format()):
            return make_response(jsonify(
                {'Error': 'Datetimes must follow the YYYY-MM-DD HH:MM:SS format'}), 400)

        # Based on the supplied parameters, build and execute the SQL query against
        # the database to get the required list of deployment steps
        cursor = g.db.cursor(MySQLdb.cursors.DictCursor)
        where_clause = Step._get_where_clause(request)
        cursor.execute("SELECT * FROM steps" + where_clause)

        # Output using the proper format
        if request.args.get("format") == "json":
            return jsonify(steps=cursor.fetchall()), 200
        else:
            return Step._csv_format(cursor), 200
