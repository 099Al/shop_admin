import flet as ft

from pages.config.sizes import d_client_column_size
from pages.config.style import textFieldColor
from pages.dashboard.content.clients.clients_elements import ClientRow


class ClientsFilter(ft.Row):
    def __init__(self, page, rows_controls):
        self.page = page
        self.rows_controls: list[ClientRow] = rows_controls
        self.d_colum_size = d_client_column_size

        self.el_divider = ft.Container(
            height=25,
            width=1,
            bgcolor=None,
            margin=0,
            padding=0,
            visible=True
        )

    def drop_filter(self, e):
        for row in self.rows_controls:
            row.drop_filter()

        self.c_drop_filter.content = None
        self.tf_filter_name.value = ""
        self.tf_filter_phone.value = ""
        self.tf_filter_email.value = ""
        self.tf_filter_telegram.value = ""
        self.tf_filter_link.value = ""
        self.page.update()

    def filter_name(self, e):
        for row in self.rows_controls:
            row.filter_field("name", e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_phone.value = ""
        self.tf_filter_email.value = ""
        self.tf_filter_telegram.value = ""
        self.tf_filter_link.value = ""

        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"])

        self.page.update()

    def filter_phone(self, e):
        for row in self.rows_controls:
            row.filter_field("phone", e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_name.value = ""
        self.tf_filter_email.value = ""
        self.tf_filter_telegram.value = ""
        self.tf_filter_link.value = ""

        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"])
        self.page.update()

    def filter_email(self, e):
        for row in self.rows_controls:
            row.filter_field("email", e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_name.value = ""
        self.tf_filter_phone.value = ""
        self.tf_filter_telegram.value = ""
        self.tf_filter_link.value = ""
        self.page.update()

    def filter_telegram(self, e):
        for row in self.rows_controls:
            row.filter_field("telegram_name", e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_name.value = ""
        self.tf_filter_phone.value = ""
        self.tf_filter_email.value = ""
        self.tf_filter_link.value = ""
        self.page.update()

    def filter_link(self, e):
        for row in self.rows_controls:
            row.filter_field("telegram_link", e.data)

        self.c_drop_filter.content = self.icon_drop_filter
        self.tf_filter_name.value = ""
        self.tf_filter_phone.value = ""
        self.tf_filter_email.value = ""
        self.tf_filter_telegram.value = ""
        self.page.update()


        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"])
        self.page.update()

    def build(self):

        self.icon_drop_filter = ft.IconButton(icon=ft.icons.CANCEL, scale=0.8, on_click=self.drop_filter)

        self.tf_filter_name = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=self.filter_name)
        self.tf_filter_phone = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=self.filter_phone)
        self.tf_filter_email = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=self.filter_email)
        self.tf_filter_telegram = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=self.filter_telegram)
        self.tf_filter_link = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=self.filter_link)

        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"])

        return ft.Row(
            controls=[
                ft.Container(content=ft.IconButton(icon=ft.icons.FILTER_ALT, scale=0.8), height=40,
                             width=self.d_colum_size["c_edit"], alignment=ft.alignment.center_right, padding=0),

                self.el_divider,
                ft.Container(
                    content=self.tf_filter_name,
                    width=self.d_colum_size["c_name"]),
                self.el_divider,
                ft.Container(
                    content=self.tf_filter_phone,
                    width=self.d_colum_size["c_phone"]),
                self.el_divider,
                ft.Container(
                    content=self.tf_filter_email,
                    width=self.d_colum_size["c_email"]),
                self.el_divider,
                ft.Container(
                    content=self.tf_filter_telegram,
                    width=self.d_colum_size["c_telegram_name"]),
                self.el_divider,
                ft.Container(
                    content=self.tf_filter_link,
                    width=self.d_colum_size["c_telegram_link"]),

                self.c_drop_filter
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        )
