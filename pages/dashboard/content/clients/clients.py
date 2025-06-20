import flet as ft

from database.models.models import AdminRoles
from database.requests.req_admins import ReqAdmins
from database.requests.req_clients import ReqClients
from pages.config.errors import d_error_messages_admin
from pages.config.info_messages import snack_message_pass
from pages.dashboard.content.admins.add_button import AddAdminButton
from pages.dashboard.content.admins.admins_elements import AdminRow, AdminHeader
from pages.dashboard.head_elements import header


class ClientsContent:
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

        content_header = header(label_name="Клиенты", user_role=self.user_role)
        self.view_content.append(content_header)

        self.row_1 = ft.Row(controls=[ft.Container(margin=36)])  #empty row
        self.view_content.append(self.row_1)

        req = ReqClients()

        self.column_1 = ft.Column(
            controls=[
                # ClientHeader(self.page, self.column_with_rows.controls).build(),
                self.column_with_rows
            ],
            expand=True  # без expand scroll не работает
        )

        clients = req.get_all_clients()
        # ---rows--- заполнене списка
        for client in clients:
            self.column_with_rows.controls.append(
                ClientRow(
                    page=self.page,
                    client=client,
                    column_with_rows=self.column_with_rows
                )

            )

        self.row_scroll = ft.Row(controls=[self.column_1],
                                 expand=True,  # без expand scroll не работает
                                 scroll=ft.ScrollMode.ALWAYS
                                 )

        self.view_content.append(self.row_scroll)



        return self.view_content