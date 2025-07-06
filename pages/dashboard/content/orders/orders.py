from datetime import date

import flet as ft

from database.requests.req_orders import ReqOrders
from pages.config.sizes import d_order_column_size
from pages.dashboard.content.filter_header import GenericFilter
from pages.dashboard.content.header import GenericHeader
from pages.dashboard.content.orders.order_elements import OrderRow
from pages.dashboard.head_elements import header


class OrdersContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        # self.error_messages = d_error_messages_orders


        self.field_definitions_filter = [
            ("phone", True),
            ("telegram_link", True),
            ("created_at", True),
            ("order_sum", False),
            ("status", True),
            ("payment_status", True),
            ("delivery_address", False),
            ("comment", False),
            ("order_id", True)
        ]

        self.field_definitions_header = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Телефон", "field_name": "phone", "sort_attr": "phone", "is_sortable": False, "type": str},
            {"label": "Телеграм Link", "field_name": "telegram_link", "sort_attr": "telegram_link", "is_sortable": False,"type": str},
            {"label": "Дата", "field_name": "created_at", "sort_attr": "created_at", "is_sortable": True, "type": str},
            {"label": "Сумма", "field_name": "order_sum", "sort_attr": "order_sum", "is_sortable": True, "type": str},
            {"label": "Статус", "field_name": "status", "sort_attr": "status", "is_sortable": True, "type": str},
            {"label": "Оплата", "field_name": "payment_status", "sort_attr": "payment_status", "is_sortable": True,"type": str},
            {"label": "Адрес", "field_name": "delivery_address", "sort_attr": "delivery_address", "is_sortable": False,"type": str},
            {"label": "Комментарий", "field_name": "comment", "sort_attr": "comment", "is_sortable": False,"type": str},
            {"label": "Номер заказа", "field_name": "order_id", "sort_attr": "order_id", "is_sortable": True, "type": str},
            {"label": "Позиции", "field_name": "order_products", "sort_attr": "order_products", "is_sortable": False,"type": str},
        ]





    def build(self):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Заказы", user_role=self.user_role)
        self.view_content.append(content_header)

        self.row_1 = ft.Row(controls=[ft.Container(margin=36)])  # empty row  #Todo: фильтр по статусу заказов RadioButton
        self.view_content.append(self.row_1)

        req = ReqOrders()

        self.column_1 = ft.Column(
            controls=[
                GenericFilter(self.page, self.column_with_rows.controls, self.field_definitions_filter, d_order_column_size).build(),
                GenericHeader(
                    self.page,
                    self.column_with_rows.controls,
                    self.field_definitions_header,
                    d_order_column_size,
                    default_sort_key='created_at',
                    sort_key_type=date,
                    sort_key_reverse=True
                ).build(),
                self.column_with_rows],
            expand=True
        )


        for order_info in req.get_all_orders_with_users():
            self.column_with_rows.controls.append(
                OrderRow(
                    page=self.page,
                    order_info=order_info,
                    column_with_rows=self.column_with_rows
                )

            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)

        return self.view_content