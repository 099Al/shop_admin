import os

from sqlalchemy import create_engine, Table, MetaData, select, insert, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

from utils.functions import validate_email


class Database:
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

        self.adminUser = Table('admins', self.metadata, autoload_with=self.engine)

    def check_email(self, email):
        result = self.session.execute(
            select(self.adminUser)
            .where(self.adminUser.c.email == email)
        )
        return result.fetchone()

    def check_login(self, login):
        result = self.session.execute(
            select(self.adminUser)
            .where(self.adminUser.c.login == login)
        )
        return result.fetchone()

    def insert_user(self, login, email, password):
        self.session.execute(insert(self.adminUser)
                             .values(login=login,
                                     email=email,
                                     password=password
                                     )
                             )
        self.session.commit()

    def authorization(self, login, password):
        if validate_email(login):
            result = self.session.execute(
                select(self.adminUser)
                .where(and_(self.adminUser.c.email == login, self.adminUser.c.password == password))
            )
        else:
            result = self.session.execute(
                select(self.adminUser)
                .where(and_(self.adminUser.c.login == login, self.adminUser.c.password == password))
            )

        return result.fetchone()


