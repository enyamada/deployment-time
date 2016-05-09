from datetime import datetime


class Date:

    def __init__(self, dt):
        print "init"
        self.dt = dt

    def valid_format(self):
        """
        Checks if the supplied string contains a valid date/time (that follows
        the YYYY-MM-DD HH:MM:SS format). Returns true if so (or if the string is
        null or empty), false otherwise.
        """

        # If candidate is None, return true
        if not self.dt:
            print "dt empty"
            return True

        # Verify if time format is ok and stores in into a time-tuple format
        try:
            stime = datetime.strptime(self.dt, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return False
        else:
            return True


