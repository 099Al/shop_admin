import flet as ft

from database.requests.req_orders import ReqOrders
from pages.dashboard.head_elements import header


class OrdersContent:
    def __init__(self, instance):
        self.page = instance.page
        self.user_role = instance.user_role
        self.view_content = []
        # self.error_messages = d_error_messages_admin



    def build(self):
        self.column_with_rows = ft.Column(
            controls=[],
            spacing=1,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        content_header = header(label_name="Заказы", user_role=self.user_role)
        self.view_content.append(content_header)

        self.row_1 = ft.Row(controls=[ft.Container(margin=36)])  # empty row
        self.view_content.append(self.row_1)

        req = ReqOrders()

        return self.view_content