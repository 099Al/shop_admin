import flet as ft

from pages.config.style import defaultFontColor
from pages.dashboard.content.sort_header import SortHeader


class GenericHeader(ft.Row):
    def __init__(self, page, rows_controls, field_definitions, d_column_size, default_sort_key, sort_key_type, sort_key_reverse):
        super().__init__()
        self.page = page
        self.rows_controls = rows_controls
        self.d_column_size = d_column_size
        self.field_definitions = field_definitions
        self.default_sort_key = default_sort_key
        self.sort_key_type = sort_key_type
        self.sort_key_reverse = sort_key_reverse

        self.el_divider = ft.Container(
            height=self.d_column_size['el_height'],
            width=1,
            bgcolor="white",
            margin=0,
            padding=0
        )


    def build(self):
        sort_headers = []

        def _reset_all_sort_headers_except(active_header):
            for hdr in sort_headers:
                if hdr != active_header:
                    hdr.reset_sort()

        header_controls = []

        for i, col in enumerate(self.field_definitions):
            # if i > 0:
            #     header_controls.append(self.el_divider)

            field_name = col.get("field_name")
            label = col["label"]
            width_key = f"{field_name}"
            width = self.d_column_size.get(width_key, 80)

            if col.get("is_sortable"):
                sort_header = SortHeader(
                    self.page,
                    self.rows_controls,
                    default_sort_key=self.default_sort_key,
                    sort_key_type=self.sort_key_type,
                    sort_key_reverse=self.sort_key_reverse,
                    reset_others_callback=_reset_all_sort_headers_except
                )
                sort_headers.append(sort_header)
                header_controls.append(
                    sort_header.attribute_header_with_sort(
                        label,
                        width,
                        col["type"],
                        col["sort_attr"]
                    )
                )
            else:
                header_controls.append(self._create_header_cell(label, width))

            if col.get("right_devider", 1):
                header_controls.append(self.el_divider)



        return ft.Row(
            controls=header_controls,
            height=50,
            vertical_alignment=ft.CrossAxisAlignment.END
        )

    def _create_header_cell(self, text, width, visible=True):
        return ft.Container(
            content=ft.Text(
                text,
                color=defaultFontColor,
                size=15,
                font_family="cupurum",
            ),
            width=width,
            alignment=ft.alignment.bottom_left,
            visible=visible
        )
