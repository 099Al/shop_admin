from datetime import datetime

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

    def _filter_row(self, row, field_name, text, tp=None):
        if tp == "period":
            try:
                value_raw = getattr(row, field_name, "") or ""
                value_date = datetime.strptime(str(value_raw[0:10]), "%Y-%m-%d").date()
                text_date = datetime.strptime(str(text[0:10]), "%Y-%m-%d").date()
                row.visible = value_date >= text_date
            except (ValueError, TypeError):
                pass
        else:
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

    def filter_by(self, field_name, e, tp=None):
        for row in self.rows_controls:
            self._filter_row(row, field_name, e.data, tp)

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
        #is_filterable = True - поиск по совпадению
        #is_filterable = period - по периоду, старше указанной даты
        for i, (field_name, is_filterable) in enumerate(self.field_definitions):
            if is_filterable == True:
                tf = ft.TextField(
                    height=45,
                    read_only=False,
                    text_size=15,
                    border_color=textFieldColor,
                    color="white",
                    on_submit=lambda e, f=field_name: self.filter_by(f, e)
                )
                self.filter_fields[field_name] = tf
                content = tf
            elif is_filterable == "period":
                tf = ft.TextField(
                    height=45,
                    read_only=False,
                    text_size=15,
                    border_color=textFieldColor,
                    color="white",
                    on_submit=lambda e, f=field_name, tp='period': self.filter_by(f, e, tp)
                )
                self.filter_fields[field_name] = tf
                content = tf
            else:
                content = ft.Container()  # Empty placeholder, no filter

            if i > 0:
                filter_controls.append(self.el_divider)

            col_key = field_name
            width = self.d_colum_size.get(col_key, 0) or self.d_colum_size.get(field_name, 100)

            filter_controls.append(
                ft.Container(content=content, width=width)
            )

        self.c_drop_filter = ft.Container(
            content=None,
            width=50,
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.IconButton(icon=ft.icons.FILTER_ALT, scale=0.8),
                    height=40,
                    width=self.d_colum_size["edit"],
                    alignment=ft.alignment.center_right,
                    padding=0
                ),
                *filter_controls,
                self.c_drop_filter
            ],
            vertical_alignment=ft.CrossAxisAlignment.END
        )