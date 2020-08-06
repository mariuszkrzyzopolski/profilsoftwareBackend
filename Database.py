from sqlalchemy import *
from sqlalchemy_utils import *


class DataConn():
    def __init__(self, sessionmake):
        self.engine = create_engine('sqlite:///RandomUsers.db')
        self.session = sessionmake(bind=self.engine)

    def createnewdatabase(self):
        if database_exists(self.engine.url): drop_database(self.engine.url)
        create_database(self.engine.url)
        return self.session
