import flet as ft

from pages.config.sizes import d_client_column_size
from pages.config.style import textFieldColor
from pages.dashboard.content.clients.clients_elements import ClientRow


class ClientsFilter(ft.Row):
    def __init__(self, page, rows_controls):
        self.page = page
        self.rows_controls: list[ClientRow] = rows_controls
        self.d_colum_size = d_client_column_size
        self.filter_fields = {}  # field_name -> TextField (only for filterable fields)

        self.el_divider = ft.Container(
            height=25, width=1, bgcolor=None, margin=0, padding=0, visible=True
        )

        # Format: (field_name, column_key, is_filterable)
        self.field_definitions = [
            ("name", "c_name", True),
            ("phone", "c_phone", True),
            #("some_static_field", "c_static", False),  # not filterable, space reserved
            ("email", "c_email", True),
            ("telegram_name", "c_telegram_name", True),
            ("telegram_link", "c_telegram_link", True),
        ]

    def drop_filter(self, e):
        for row in self.rows_controls:
            row.drop_filter()

        for tf in self.filter_fields.values():
            tf.value = ""

        self.c_drop_filter.content = None

        self.page.update()

    def filter_by(self, field_name, e):
        for row in self.rows_controls:
            row.filter_field(field_name, e.data)

        self.c_drop_filter.content = self.icon_drop_filter

        # Clear other filters
        for key, tf in self.filter_fields.items():
            if key != field_name:
                tf.value = ""

        self.page.update()

    def build(self):
        self.icon_drop_filter = ft.IconButton(
            icon=ft.icons.CANCEL,
            scale=0.8,
            on_click=self.drop_filter
        )

        # Dynamically build controls for each field
        filter_controls = []
        for i, (field_name, col_key, is_filterable) in enumerate(self.field_definitions):
            if is_filterable:
                tf = ft.TextField(
                    height=40,
                    read_only=False,
                    text_size=15,
                    border_color=textFieldColor,
                    color="white",
                    on_submit=lambda e, f=field_name: self.filter_by(f, e)
                )
                self.filter_fields[field_name] = tf
                content = tf
            else:
                content = ft.Container()  # Empty placeholder, no filter

            if i > 0:
                filter_controls.append(self.el_divider)

            filter_controls.append(
                ft.Container(content=content, width=self.d_colum_size[col_key])
            )

        self.c_drop_filter = ft.Container(
            content=None,
            width=self.d_colum_size["c_dell"]
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.IconButton(icon=ft.icons.FILTER_ALT, scale=0.8),
                    height=40,
                    width=self.d_colum_size["c_edit"],
                    alignment=ft.alignment.center_right,
                    padding=0
                ),
                *filter_controls,
                self.c_drop_filter
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        )