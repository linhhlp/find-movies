"""Logging tool for find-movies.com to Cassandra"""

import datetime


class Logger:
    def __init__(self, db_name, db_session):
        self.db_name = db_name
        self.db_session = db_session
        self.create_table()

    def __repr__(self):
        return self.db_name + "." + self.db_session

    def data_2_str(self, data):
        results = ""
        for _, row in data.items():
            results += row.title + " " + str(row.year) + "; "
        return results

    def upload(self, content, flask):
        ip = flask.request.remote_addr
        session_id = flask.session["uid"]
        query = flask.request.values.get("content")

        preparedInsert = f"""
INSERT INTO {self.db_name} (ip, session_id, time, query, results) 
    VALUES (%s,%s,%s,%s,%s);
"""

        self.db_session.execute(
            preparedInsert,
            [ip, session_id, datetime.datetime.utcnow(), query, content],
        )

    def create_table(self):
        table_create_query = f"""
CREATE TABLE IF NOT EXISTS {self.db_name} (
ip text,
session_id uuid,
time timestamp,
query text,
results text,
PRIMARY KEY (ip, session_id, time)
);
"""
        self.db_session.execute(table_create_query)
