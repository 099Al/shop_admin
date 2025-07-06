from sqlalchemy import select, update, delete
from database.connect import DataBase
from database.models.models import Order


class ReqOrders:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = DataBase().get_session()

    def get_session(self):
        return self.session


    def get_all_orders(self):
        result = self.session.execute(select(Order))
        return result.scalars().all()