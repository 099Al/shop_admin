import flet as ft

from database.requests.req_admins import ReqAdmins
from pages.dashboard.content.admins.admins_elements import AdminRow, AdminHeader
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

        self.column_1 = ft.Column(
            controls=[
                AdminHeader(self.page, self.column_with_rows.controls).build(),
                self.column_with_rows
            ],
            expand=True  # без expand scroll не работает
        )

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

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)



        return self.view_content