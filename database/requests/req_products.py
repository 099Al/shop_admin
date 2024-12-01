from sqlalchemy import select

from database.connect import DataBase
from database.models.models import Category


class ReqCategory:

    def __init__(self, db: DataBase):
        self.session = db.get_session()

    def get_all_categories(self):
        result = self.session.execute(select(Category))
        return result.scalars().all()

