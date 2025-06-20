import flet as ft

from database.models.models import AdminRoles
from database.requests.req_admins import ReqAdmins
from pages.config.errors import d_error_messages_admin
from pages.config.info_messages import snack_message_pass
from pages.dashboard.content.admins.add_button import AddAdminButton
from pages.dashboard.content.admins.admins_elements import AdminRow, AdminHeader
from pages.dashboard.head_elements import header


class AdminsContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        self.error_messages = d_error_messages_admin

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

        self.column_1 = ft.Column(
            controls=[
                AdminHeader(self.page, self.column_with_rows.controls).build(),
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