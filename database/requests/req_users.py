from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Admin, Client


class ReqClients:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = DataBase().get_session()

    def get_all_users(self):
        result = self.session.execute(select(Client))
        return result.scalars().all()

    def get_client_by_phone(self, phone):
        stmt = select(Client).where(Client.phone == phone)
        res = self.session.execute(stmt).scalars().first()
        if res:
            return res

    def get_client_by_telegram_name(self, telegram_name):
        stmt = select(Client).where(Client.telegram_name == telegram_name)
        res = self.session.execute(stmt).scalars().first()
        if res:
            return res
