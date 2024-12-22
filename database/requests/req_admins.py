from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Admin

class ReqAdmins:
    def __init__(self, db: DataBase):
        self.session = db.get_session()

    def get_all_users(self):
        result = self.session.execute(select(Admin))
        #result = self.session.query(Admin.telegram_id, Admin.telegram_name, Admin.role, Admin.name, Admin.phone, Admin.email, Admin.login).all()
        return result.scalars().all()

    def delete_admin(self, telegram_id):
        self.session.execute(
            delete(Admin)
            .where(Admin.telegram_id == telegram_id)
        )
        self.session.commit()

    # def get_max_length(self):
    #     result = self.session.execute(select(func.max(Admin.telegram_id)))
    #     return result.scalars().first()

    def update_user(self, telegram_id, **kwargs):
        try:
            self.session.execute(
                update(Admin)
                .where(Admin.telegram_id == telegram_id)
                .values(**kwargs)
            )
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            return None

    def new_user(self):
        try:
            result = self.session.execute(insert(Admin))
            self.session.commit()
            id = result.inserted_primary_key[0]  #use phone to get telegram_id
            return id
        except Exception as e:
            self.session.rollback()
            return None