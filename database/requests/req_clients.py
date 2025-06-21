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

    def update_client(self, telegram_id, **kwargs):
        try:
            self.session.execute(
                update(Client)
                .where(Client.telegram_id == telegram_id)
                .values(**kwargs)
            )
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            return None