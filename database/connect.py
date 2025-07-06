from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings


class DataBase:
    def __init__(self):


        self.connect = settings.connect_url
        #self.connect =  f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        self.engine = create_engine(self.connect, echo=True)

        self.metadata = MetaData()
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_session(self):
        return self.session

    def get_engine(self):
        return self.engine