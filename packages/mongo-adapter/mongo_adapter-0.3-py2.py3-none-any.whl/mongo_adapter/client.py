"""
client.py

Establish a connection to the database

"""
import logging

from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure, ServerSelectionTimeoutError)

from pymongo import uri_parser

# For testing only
from mongomock import MongoClient as MockClient

from .exceptions import InterfaceError

try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus

LOG = logging.getLogger(__name__)

def check_connection(client):
    """Check if the mongod process is running
    
    Args:
        client(MongoClient)
    
    Returns:
        bool
    """
    try:
        client.server_info()
    except ServerSelectionTimeoutError as err:
        raise InterfaceError("Seems like mongod is not running")
    
    return True


def get_client(host='localhost', port=27017, username=None, password=None,
              uri=None, timeout=20, authdb=None):
    """Get a client to the mongo database

    Args:
        host(str): Host of database
        port(int): Port of database
        username(str)
        password(str)
        uri(str): If a certain uri should be used
        timeout(int): How long should the client try to connect

    Returns:
        client(pymongo.MongoClient)

    """
    # for testing only
    if (uri and uri.startswith("mongomock://")):
        LOG.warning("Use mongomock backend")
        return MockClient(host=host, port=port)

    if uri is None:
        if username and password:
            uri = ("mongodb://{}:{}@{}:{}"
                   .format(quote_plus(username), quote_plus(password), host, port))
            if authdb:
                uri += '/{}'.format(authdb)
        else:
            uri = ("mongodb://{0}:{1}".format(host, port))
    
    # Parse the uri and check if it is on the correct format    
    # Will raise pymongo.errors.InvalidURI if incorrect uri
    uri_info = uri_parser.parse_uri(uri)
    # nodelist is a list of tuples with (<host>,<port>)
    host = uri_info['nodelist'][0][0]
    port = uri_info['nodelist'][0][1]
    username = uri_info['username']
    password = uri_info['password']

    # Use this for logging
    pwd = None
    if password:
        pwd = '******'

    log_uri = "mongodb://{}:{}@{}:{}".format(username,pwd,host,port)
    LOG.info("Connecting to uri:%s", log_uri)
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=timeout)
    except ServerSelectionTimeoutError as err:
        LOG.warning("Connection Refused")
        raise InterfaceError
    
    LOG.debug("Check if mongod is running")
    check_connection(client)

    LOG.info("Connection established")
    return client
