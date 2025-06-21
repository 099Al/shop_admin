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

    def filter_by(self, field_name, e):
        for row in self.rows_controls:
            row.filter_field(field_name, e.data)

        self.c_drop_filter.content = self.icon_drop_filter

        # Clear all filters
        self.tf_filter_name.value = "" if field_name != "name" else self.tf_filter_name.value
        self.tf_filter_phone.value = "" if field_name != "phone" else self.tf_filter_phone.value
        self.tf_filter_email.value = "" if field_name != "email" else self.tf_filter_email.value
        self.tf_filter_telegram.value = "" if field_name != "telegram_name" else self.tf_filter_telegram.value
        self.tf_filter_link.value = "" if field_name != "telegram_link" else self.tf_filter_link.value


        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"])
        self.page.update()

    def build(self):

        self.icon_drop_filter = ft.IconButton(icon=ft.icons.CANCEL, scale=0.8, on_click=self.drop_filter)

        self.tf_filter_name = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=lambda e: self.filter_by("name", e))
        self.tf_filter_phone = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=lambda e: self.filter_by("phone", e))
        self.tf_filter_email = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=lambda e: self.filter_by("email", e))
        self.tf_filter_telegram = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=lambda e: self.filter_by("telegram_name", e))
        self.tf_filter_link = ft.TextField(height=40, read_only=False, text_size=15, border_color=textFieldColor,  color="white", on_submit=lambda e: self.filter_by("telegram_link", e))

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
