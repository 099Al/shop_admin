from sqlalchemy import select, and_

from database.connect import DataBase
from database.models.models import Admin
from utils.functions import validate_email


class ReqAdmins:

    def __init__(self, db: DataBase):
        self.session = db.get_session()
    def check_login(self, login):
        result = self.session.execute(
            select(Admin)
            .where(Admin.login == login)
        )
        return result.scalars().first()


    def authorization(self, login, password):
        if validate_email(login):
            result = self.session.execute(
                select(Admin)
                .where(and_(Admin.email == login, Admin.password == password))
            )
        else:
            result = self.session.execute(
                select(Admin)
                .where(and_(Admin.login == login, Admin.password == password))
            )

        return result.scalars().first()