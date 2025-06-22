import flet as ft

from database.models.models import ClientsBan
from database.requests.req_clients import ReqClients
from pages.config.errors import d_error_messages_admin
from pages.config.sizes import d_client_column_size
from pages.dashboard.content.clients.clients_elements import ClientRow
from pages.dashboard.content.filter_header import GenericFilter
from pages.dashboard.content.header import GenericHeader
from pages.dashboard.head_elements import header





class ClientsContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        self.error_messages = d_error_messages_admin

        self.field_definitions_filter = [
            ("name", True),
            ("phone", True),
            # ("some_static_field", "c_static", False),  # not filterable, space reserved
            ("email", True),
            ("telegram_name", True),
            ("telegram_link", True),
        ]

        self.field_definitions_header = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Имя", "field_name": "name", "sort_attr": "name", "is_sortable": True, "type": str},
            {"label": "Телефон", "field_name": "phone", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Email", "field_name": "email", "sort_attr": "email", "is_sortable": True, "type": str},
            {"label": "Telegram", "field_name": "telegram_name", "sort_attr": "telegram_name", "is_sortable": True, "type": str},
            {"label": "Telegram Link", "field_name": "telegram_link", "sort_attr": "telegram_link", "is_sortable": True, "type": str},
            {"label": "Бан", "field_name": "is_banned", "sort_attr": "is_banned", "is_sortable": True, "type": int},
            {"label": "Причина", "field_name": "ban_reason", "sort_attr": None, "is_sortable": False, "type": None}
        ]

    def build(self):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Клиенты", user_role=self.user_role)
        self.view_content.append(content_header)

        self.row_1 = ft.Row(controls=[ft.Container(margin=36)])  #empty row
        self.view_content.append(self.row_1)

        req = ReqClients()


        self.column_1 = ft.Column(
            controls=[
                GenericFilter(self.page, self.column_with_rows.controls, self.field_definitions_filter, d_client_column_size).build(),
                GenericHeader(
                    self.page,
                    self.column_with_rows.controls,
                    self.field_definitions_header,
                    d_client_column_size,
                    default_sort_key='telegram_id',
                    sort_key_type=int,
                    sort_key_reverse=True,
                ).build(),
                self.column_with_rows
            ],
            expand=True  # без expand scroll не работает
        )

        d_ban = {1: "Бан", 0: "Снять бан"}
        clients = req.get_all_clients()
        # ---rows--- заполнене списка
        for client in clients:
            self.column_with_rows.controls.append(
                ClientRow(
                    page=self.page,
                    client=client,
                    l_ban_options=[ft.DropdownOption(key=status.value, text=d_ban[status.value]) for status in ClientsBan],
                    column_with_rows=self.column_with_rows
                )

            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)



        return self.view_content