from sqlalchemy import select, func, update, delete, insert

from database.connect import DataBase
from database.models.models import Admin

class ReqAdmins:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = DataBase().get_session()

    def get_session(self):
        return self.session

    def get_all_users(self):
        result = self.session.execute(select(Admin))
        #result = self.session.query(Admin.telegram_id, Admin.telegram_name, Admin.role, Admin.name, Admin.phone, Admin.email, Admin.login).all()
        return result.scalars().all()

    def get_all_roles(self):
        #todo: Роли должны задаваться через Enum
        result = self.session.execute(select(Admin.role))
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

    def get_admin_by_phone(self, phone):
        result = self.session.execute(
            select(Admin)
            .where(Admin.phone == phone)
        )
        return result.scalars().first()

    def get_admin_by_telegram_name(self, telegram_name):
        result = self.session.execute(
            select(Admin)
            .where(Admin.telegram_name == telegram_name)
        )
        return result.scalars().first()

    def set_password(self, telegram_id, password):
        self.session.execute(
            update(Admin)
            .where(Admin.telegram_id == telegram_id)
            .values(password=password)
        )
        self.session.commit()