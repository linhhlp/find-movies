import logging

from cassandra import OperationTimedOut  # , ConsistencyLevel,
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster as CassandraCluster
from cassandra.cluster import ConnectionShutdown, NoHostAvailable
from cassandra.cluster import Session as CassandraSession

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Cassandra:
    """Connector for Cassandra.

    This is the simplified connector for the Cassandra in a cluster.
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
    """

    session: CassandraSession
    cluster: CassandraCluster

    def __init__(self, db_info, config):
        self.secure_bundle_path = db_info["secure_bundle_path"]
        self.client_id = db_info["client_id"]
        self.keyspace = db_info["keyspace"]
        self.client_secret = db_info["client_secret"]
        self.table_name = db_info["table_name"]
        if "protocol_version" in config:
            self.protocol_version = config["protocol_version"]

        self.cloud_config = {
            "secure_connect_bundle": db_info["secure_bundle_path"],
            'use_default_tempdir': True,
        }
        self.auth_provider = PlainTextAuthProvider(
            db_info["client_id"], db_info["client_secret"]
        )
        self.session = None

    def connect(self):
        err = None
        if self.session is not None:
            log.debug("session is not None, try to shut down first.")
            self.disconnect()

        try:
            self.cluster = CassandraCluster(
                cloud=self.cloud_config,
                auth_provider=self.auth_provider,
                protocol_version=self.protocol_version,
            )
            self.session = self.cluster.connect()
            self.set_keyspace(self.keyspace)

        except (OperationTimedOut, NoHostAvailable, ConnectionShutdown) as e:
            print(e)
            err = e

        if self.session is None:
            raise err

    def execute(self, command, arr=None):
        result = None
        if self.session is None:
            self.connect()

        try:
            result = self.session.execute(command, arr)
        except ConnectionShutdown:
            self.connect()
            result = self.session.execute(command, arr)
        return result

    def set_keyspace(self, keyspace):
        return self.execute(f"USE {keyspace};")

    def disconnect(self):
        try:
            self.cluster.shutdown()
        except Exception:
            log.debug("Can not shut down.")


def convert_text_2_vect(co, texts, model="embed-english-light-v2.0"):
    """Convert multiple text strings to vectors."

    Parameters
    ----------
    co : cohere.Client
        co = cohere.Client(API_key)
    texts : list of strings
        texts = [text1, text2, text3, text4, text5, text6...]
    model : str, optional
        Dimension of output vector, by default "embed-english-light-v2.0"
        "embed-english-light-v2.0" = 1024 dim
        "embed-english-v2.0" = 4096 dim

    Returns
    -------
    list of vectors
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], ... ]
    """
    response = co.embed(model=model, texts=texts)
    # print('Embeddings: {}'.format(response.embeddings))
    return response.embeddings
