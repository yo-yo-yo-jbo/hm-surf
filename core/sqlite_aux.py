from core.utils import Utils

import sqlite3
import tempfile
import shutil
import os

class SqliteAux(object):
    """
        SQLITE database helper.
    """

    def __init__(self, path):
        """
            Creates an instance.
        """

        # Save path and initialize other members
        self.path = path
        self.temp_path = None
        self.conn = None

    @staticmethod
    def __connect(path):
        """
            Attempts to connect to the given database as read-only. Returns None upon failure.
        """

        # Open the path as read only and attempt to fetch something from it
        try:
            conn = sqlite3.connect(f'file:{Utils.encode_as_uri(path)}?mode=ro', uri=True)
            conn.cursor().execute('SELECT name FROM my_db.sqlite_master WHERE type=\'table\';')
            return conn
        except sqlite3.OperationalError:
            return None

    def connect(self):
        """
            Connects to the database.
        """

        # Connect to database
        self.conn = self.__class__.__connect(self.path)
        if self.conn is not None:
            return
        
        # Some databases might still try to write during SELECT clauses so we attempt to copy the file temporarily as a counter-measure
        # We also handle TCC-related permission errors
        try:
            self.temp_path = tempfile.mktemp()
            shutil.copy2(self.path, self.temp_path)
            self.conn = self.__class__.__connect(self.temp_path)    
        except PermissionError:
            pass

    def __enter__(self):
        """
            Connects to the database.
        """

        # Connect
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Cleans up.
        """

        # Clean up
        self.close()

    def close(self):
        """
            Cleans up.
        """

        # Clean up connection
        if self.conn is not None:
            self.conn.close()
            self.conn = None

        # Unlink temporary file
        if self.temp_path is not None:
            try:
                os.unlink(self.temp_path)
            except FileNotFoundError:
                pass
            self.temp_path = None

    def run_query(self, query):
        """
            Runs a query.
        """

        # Runs a query unless there is no connection
        if self.conn is None:
            return []
        return self.conn.cursor().execute(query).fetchall()

