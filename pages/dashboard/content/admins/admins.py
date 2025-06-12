import flet as ft

from database.requests.req_admins import ReqAdmins
from pages.dashboard.content.admins.admins_elements import AdminRow
from pages.dashboard.head_elements import header


class AdminsContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []

    def build(self):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Пользователи (Администраторы)", user_role=self.user_role)
        self.view_content.append(content_header)

        req = ReqAdmins()
        admins = req.get_all_users()
        roles = [ft.DropdownOption(key=str(role), text=str(role)) for role in req.get_all_roles()]
        # ---rows--- заполнене списка продукатами
        for user in admins:
            self.column_with_rows.controls.append(
                AdminRow(
                    page=self.page,
                    admin=user,
                    roles=roles,
                    column_with_rows=self.column_with_rows
                )

            )

        self.view_content.append(self.column_with_rows)

        return self.view_content