import flet as ft

from database.models.models import AdminRoles
from database.requests.req_admins import ReqAdmins
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

        return self.view_content