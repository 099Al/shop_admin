from datetime import date, datetime, timedelta

import flet as ft

from database.models.models import OrderSatus, Order
from database.requests.req_orders import ReqOrders
from pages.config.sizes import d_order_column_size
from pages.config.style import textFieldColor
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
            ("created_at", 'period'),
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


        self.filter_orders = [ft.DropdownOption(key="Все", text="Все"),
                              ft.DropdownOption(key="Новые", text="Новые"),
                              ft.DropdownOption(key="В работе", text="В работе"),
                              ft.DropdownOption(key="Отмененные", text="Отмененные"),
                              ft.DropdownOption(key="Завершенные", text="Завершенные"),
                              ft.DropdownOption(key="Завершенные 1 день", text="Завершенные 1 день"),
                              ft.DropdownOption(key="Завершенные неделя", text="Завершенные неделя"),
                              ft.DropdownOption(key="Завершенные месяц", text="Завершенные месяц"),
                              ]


    def filter_orders_change(self, e):
        filter = e.control.value
        if filter == "Новые":
            where_stm = [Order.status == OrderSatus.NEW.value]
        elif filter == "В работе":
            where_stm = [Order.status == OrderSatus.IN_PROCESS.value]
        elif filter == "Отмененные":
            where_stm = [Order.status == OrderSatus.REJECTED.value]
        elif filter == "Завершенные":
            where_stm = [Order.status == OrderSatus.DONE.value]
        elif filter == "Завершенные 1 день":
            where_stm = [Order.status == OrderSatus.DONE.value, Order.created_at > datetime.today() - timedelta(days=1)]
        elif filter == "Завершенные неделя":
            where_stm = [Order.status == OrderSatus.DONE.value, Order.created_at > datetime.today() - timedelta(days=7)]
        elif filter == "Завершенные месяц":
            where_stm = [Order.status == OrderSatus.DONE.value, Order.created_at > datetime.today() - timedelta(days=30)]
        else:
            where_stm = None

        self.build(where_stm)
        self.page.update()


    def build(self, where_stm=None):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Заказы", user_role=self.user_role)
        self.view_content.append(content_header)

        dd_order_filer = ft.Dropdown(
            width=230,
            editable=False,
            border_color=textFieldColor,
            color="white",
            on_change=self.filter_orders_change,
            # hint_text = v_status,
            hint_style=ft.TextStyle(font_family="cupurum", size=15, color="white"),
            menu_width=150 * 1.5,
            options=self.filter_orders
        )

        self.row_1 = ft.Row(controls=[ft.Container(margin=ft.margin.only(left=d_order_column_size["edit"]))])
        self.row_1.controls.append(dd_order_filer)





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

        l_status_options = [ft.DropdownOption(key=status.value, text=status.value) for status in OrderSatus]
        for order_info in req.get_all_orders_with_users(where_stm=where_stm):
            self.column_with_rows.controls.append(
                OrderRow(
                    page=self.page,
                    order_info=order_info,
                    column_with_rows=self.column_with_rows,
                    l_status_options=l_status_options
                )
            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)

        return self.view_content