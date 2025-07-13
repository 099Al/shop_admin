from operator import and_

from sqlalchemy import select, update, delete
from database.connect import DataBase
from database.models.models import Order, Client


class ReqOrders:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = DataBase().get_session()

    def get_session(self):
        return self.session


    def get_all_orders_with_users(self, where_stm: list = None):

        sql_stm = (
            select(
                Client.phone,
                Client.telegram_link,
                Order.id,
                Order.user_tg_id,
                Order.order_sum,
                Order.status,
                Order.payment_status,
                Order.delivery_address,
                Order.comment,
                Order.created_at,
                Order.order_products
            )
            .join(Client, Client.telegram_id == Order.user_tg_id)
            .order_by(Order.created_at.desc())
        )

        if where_stm:
            if len(where_stm) == 1:
                sql_stm = sql_stm.where(where_stm[0])
            else:
                sql_stm = sql_stm.where(and_(*where_stm))

        result = self.session.execute(sql_stm)
        return result.all()

    def update_order(self, order_id, **kwargs):
        stmt = update(Order).where(Order.id == order_id).values(**kwargs)
        self.session.execute(stmt)
        self.session.commit()

    def delete_order(self, order_id):
        stmt = delete(Order).where(Order.id == order_id)
        self.session.execute(stmt)
        self.session.commit()

