from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker


class DataBase:
    def __init__(self):
        load_dotenv()
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.connect = 'sqlite:///D:/WorkSpaces/PythonWs/shop/db.sqlite3'
        #self.connect =  f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        self.engine = create_engine(self.connect)
        self.metadata = MetaData()
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_session(self):
        return self.session

    def get_engine(self):
        return self.engine