import flet as ft

from database.models.models import AdminRoles
from database.requests.req_admins import ReqAdmins
from pages.config.errors import d_error_messages_admin
from pages.config.info_messages import snack_message_pass
from pages.config.sizes import d_admin_column_size
from pages.dashboard.content.admins.add_button import AddAdminButton
from pages.dashboard.content.admins.admins_elements import AdminRow
from pages.dashboard.content.header import GenericHeader
from pages.dashboard.head_elements import header


class AdminsContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        self.error_messages = d_error_messages_admin

        self.field_definitions = [
            {"label": "", "field_name": "edit", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Telegram", "field_name": "telegram_name", "sort_attr": "telegram_name", "is_sortable": True, "type": str},
            {"label": "Роль", "field_name": "role", "sort_attr": "role", "is_sortable": True, "type": int},
            {"label": "Телефон", "field_name": "phone", "sort_attr": None, "is_sortable": False, "type": None},
            {"label": "Email", "field_name": "email", "sort_attr": "email", "is_sortable": True, "type": str},
            {"label": "Имя", "field_name": "name", "sort_attr": "name", "is_sortable": True, "type": str},
            {"label": "Telegram Link", "field_name": "telegram_link", "sort_attr": "telegram_link", "is_sortable": True, "type": str},
            {"label": "Пароль", "field_name": "password", "sort_attr": None, "is_sortable": False, "type": None},
            ]

    def build(self):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Пользователи (Администраторы)", user_role=self.user_role)
        self.view_content.append(content_header)

        add_button = AddAdminButton(
            page=self.page,
            column_with_rows=self.column_with_rows,
            # передается ссылка на список строк, чтобы к нему добавить новую категорию
        ).build()

        self.row_1 = ft.Row(
            controls=[add_button],
            alignment=ft.MainAxisAlignment.END,  # Приживается к правому краю. При изменении размеров окна - сдвигается соответственно
        )

        self.view_content.append(self.row_1)

        generic_header = GenericHeader(
            self.page,
            self.column_with_rows.controls,
            self.field_definitions,
            d_admin_column_size,
            default_sort_key='telegram_id',
            sort_key_type=int,
            sort_key_reverse=True,
        ).build()

        self.column_1 = ft.Column(
            controls=[
                generic_header,
                #AdminHeader(self.page, self.column_with_rows.controls).build(),
                self.column_with_rows
            ],
            expand=True  # без expand scroll не работает
        )

        req = ReqAdmins()
        admins = req.get_all_users()
        roles = [ft.DropdownOption(key=role.value, text=role.name.replace("_", " ").title()) for role in AdminRoles]
        # ---rows--- заполнене списка
        for user in admins:
            self.column_with_rows.controls.append(
                AdminRow(
                    page=self.page,
                    admin=user,
                    roles=roles,
                    column_with_rows=self.column_with_rows
                )

            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)

        self.view_content.append(self.error_messages["admin_exists"])
        self.view_content.append(self.error_messages["admin_not_exists"])
        self.view_content.append(snack_message_pass)



        return self.view_content