import logging

import psycopg2
import psycopg2.extras

from db_controller.config import DATABASE_CONFIG

logger = logging.getLogger('DB Controller')
logger.setLevel(logging.INFO)

class DBController:

    def __init__(self):
        self.open_connection()

    def open_connection(self):
        conn_params = ""
        for (key, value) in DATABASE_CONFIG.items():
            conn_params = "{} {}={}".format(conn_params, key, value)
        self._conn = psycopg2.connect(conn_params.lstrip())
        logger.info("DB connection opened")

    def open_cursor(self):
        self._pg_cursor = self._conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        logger.info("DB cursor opened")

    def execute(self, command, values):
        logger.info("Executing ... \ncommand: {}\nvalues: {}".format(command, values))
        self._pg_cursor.execute(command, values)

    def get(self, table, column, value):
        """Retreives items from a table given a column value pair.

        :param table: Name of the table to retreive items from
        :param column: Name of the column to be checked against
        :param value: Value expected in the column

        :type table: str
        :type column: str
        :type value: type of the column

        :return: Fetched items
        """
        command = 'SELECT * FROM {} where {} = %s'.format(table, column)
        values = (value,)
        self.execute(command, values)
        return self._pg_cursor.fetchall()

    def commit(self):
        self._conn.commit()
        logger.info("Data committed to DB")

    def apply_cursor_method(self, method, *args, **kwargs):
        """Applies psycopg2 cursor methods

        :param method: Name of the method
        :param *args: Arguments to the method
        :param **kwargs: Keyword arguments to the method

        :type method: str

        :return: Response from the psycopg2 cursor method
        """
        return getattr(self._pg_cursor, method)(*args, **kwargs)

    def close_cursor(self):
        self._pg_cursor.close()
        logger.info("DB cursor closed")

    def close_connection(self):
        self.close_cursor()
        self._conn.close()
        logger.info("DB connection closed")
