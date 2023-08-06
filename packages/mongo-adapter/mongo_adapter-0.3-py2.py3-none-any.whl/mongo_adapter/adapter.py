import logging

LOG = logging.getLogger(__name__)

class MongoAdapter(object):
    """Adapter for communicating with a mongo database
    
    Instantiate with a mongo client from mongoadapter.get_client.
    """
    def __init__(self, client=None, db_name=None):
        """
        Args:
            client(MongoClient)
            db_name(str)
        """
        self.client = client
        self.db = None
        self.db_name = None
        if (db_name and client):
            self.setup(db_name)

    def init_app(self, app):
        """Setup via Flask-pymongo"""
        host = app.config.get('MONGO_HOST', 'localhost')
        port = app.config.get('MONGO_PORT', 27017)
        self.db_name = app.config['MONGO_DBNAME']
        self.client = app.extensions['pymongo']['MONGO'][0]
        self.db = app.extensions['pymongo']['MONGO'][1]
        LOG.info("connecting to database: %s:%s/%s", host, port, self.db_name)

    def setup(self, db_name):
        """Setup connection to a database
        
        Args:
            db_name(str)
            db(pymongo.Database)
        """
        if self.client is None:
            raise SyntaxError("No client is available")
        if self.db is None:
            self.db = self.client[db_name]
            self.db_name = db_name
        LOG.info("Use database %s", self.db_name)
        # Specify collections that will be used here when overriding
        # eg self.food_collection = self.db.food etc
    
    def __str__(self):
        return "MongoAdapter(db={0})".format(self.db_name)