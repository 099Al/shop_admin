import flet as ft

from pages.config.style import textFieldColor



class GenericFilter(ft.Row):
    def __init__(self, page, rows_controls, field_definitions, d_column_size):
        self.page = page
        self.rows_controls = rows_controls
        self.field_definitions = field_definitions
        self.d_colum_size = d_column_size

        self.filter_fields = {}  # field_name -> TextField (only for filterable fields)

        self.el_divider = ft.Container(
            height=25, width=1, bgcolor=None, margin=0, padding=0, visible=True
        )

    def _filter_row(self, row, field_name, text):
        value = getattr(row, field_name, "") or ""
        row.visible = text.lower() in value.lower()

    def _drop_row_filter(self, row):
        row.visible = True


    def drop_filter(self, e):
        for row in self.rows_controls:
            self._drop_row_filter(row)

        for tf in self.filter_fields.values():
            tf.value = ""

        self.c_drop_filter.content = None

        self.page.update()

    def filter_by(self, field_name, e):
        for row in self.rows_controls:
            self._filter_row(row, field_name, e.data)

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
        for i, (field_name, is_filterable) in enumerate(self.field_definitions):
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

            col_key = "c_" + field_name
            width = self.d_colum_size.get(col_key, 0) or self.d_colum_size.get(field_name, 100)

            filter_controls.append(
                ft.Container(content=content, width=width)
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