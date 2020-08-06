from sqlalchemy import *
from sqlalchemy_utils import *
from sqlalchemy.orm import sessionmaker


class DataConn():
    session = None

    def __init__(self):
        self.engine = create_engine('sqlite:///RandomUsers.db')
        if database_exists(self.engine.url): drop_database(self.engine.url)
        create_database(self.engine.url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
