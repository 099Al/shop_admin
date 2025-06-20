from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Client

class ReqClients:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = DataBase().get_session()

    def get_session(self):
        return self.session

    def get_all_clients(self):
        result = self.session.execute(select(Client))
        return result.scalars().all()