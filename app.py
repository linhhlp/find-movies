"""This serves as Web Endpoints for Find-movies service."""

import cohere
import flask

from cred import (ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET,
                  SECURE_CONNECT_BUNDLE_PATH, API_key)
from utls import Cassandra, convert_text_2_vect

# get free Trial API Key at https://cohere.ai/
co = cohere.Client(API_key)

KEYSPACE_NAME = "demo"
TABLE_NAME = "movies_35K_vectorized"

db_info = {
    "secure_bundle_path": SECURE_CONNECT_BUNDLE_PATH,
    "client_id": ASTRA_CLIENT_ID,
    "client_secret": ASTRA_CLIENT_SECRET,
    "keyspace": KEYSPACE_NAME,
    "table_name": TABLE_NAME,
}

config = {
    "protocol_version": 4,
}

cass = Cassandra(db_info, config)

# Start web framework
app = flask.Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def find_movies():
    """Find movies."""
    data = {}
    if flask.request.method == "POST" and flask.request.values.get("content"):
        content = flask.request.values.get("content")
        method = flask.request.values.get("method")
        if not method:
            method = "plot_summary_vector_1024"
        vec = convert_text_2_vect(co, [content], "embed-english-light-v2.0")[0]
        i = 1
        for row in cass.execute(
            f"""SELECT year, title, director, cast, genre, wiki_link, plot_summary FROM 
            {KEYSPACE_NAME}.{TABLE_NAME} ORDER BY {method} ANN OF %s LIMIT 10
""",
            [vec],
        ):
            data[i] = row
            i += 1

    return flask.render_template("index.html", data=data)


#if __name__ == "__main__":
#    app.run(host="0.0.0.0")
