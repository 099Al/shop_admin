from datetime import date

import flet as ft

from pages.config.style import defaultFontColor




class SortHeader:

    def __init__(self, page, rows_controls, default_sort_key, sort_key_type, sort_key_reverse=False,  reset_others_callback=None):
        self.page = page
        self.rows_controls = rows_controls
        self.reset_others_callback = reset_others_callback

        self.sort_state = 0

        self.type_element = None
        self.key_to_sort = None

        #self.default_sort_key = default_sort_key
        self.sort_key_reverse = sort_key_reverse

        if sort_key_type == int:
            self.default_key_to_sort = lambda x: getattr(x, default_sort_key, 0) or 0
        elif sort_key_type == str:
            self.default_key_to_sort = lambda x: getattr(x, default_sort_key, '') or ''
        elif sort_key_type == date:
            self.default_key_to_sort = lambda x: getattr(x, default_sort_key, date(2000, 1, 1))

        self.sort_arrow_cell = ft.Container(
            content=ft.Text(""),
            alignment=ft.alignment.bottom_left,
            width=20,
            #padding=ft.padding.only(left=20),
            #bgcolor='red'
        )

    def reset_sort(self):
        self.sort_state = 0
        self.sort_arrow_cell.content = ft.Text("")


    def _create_sort_icon(self, state):

        if state == 1:
            rotation = 1.57
        elif state == 2:
            rotation = 4.71
        else:
            rotation = None

        if rotation is not None:
            sort_icon = ft.Icon(name=ft.icons.ARROW_RIGHT_ALT, rotate=rotation, color=ft.colors.WHITE, size=20)
        else:
            sort_icon = ft.Text("")

        return ft.Container(
            content=sort_icon,
            alignment=ft.alignment.bottom_right,
            padding=0,
            #bgcolor='orange'
        )



    def _on_click_handler(self, e):

        if self.reset_others_callback:
            self.reset_others_callback(self)

        self.sort_state = (self.sort_state + 1) % 3

        if self.sort_state == 1:
            self.rows_controls.sort(key=self.key_to_sort)
        elif self.sort_state == 2:
            self.rows_controls.sort(key=self.key_to_sort, reverse=True)
        else:
            self.rows_controls.sort(key=self.default_key_to_sort, reverse=self.sort_key_reverse)

        self.sort_arrow_cell.content = self._create_sort_icon(self.sort_state)
        self.page.update()



    def attribute_header_with_sort(self, header_name, width, type_element, element_to_sort):
        self.type_element = type_element

        if type_element == str:
            self.key_to_sort = lambda x: getattr(x, element_to_sort, '') or ''
        elif type_element == int:
            self.key_to_sort = lambda x: getattr(x, element_to_sort, 0) or 0
        elif type_element == date:
            self.key_to_sort = lambda x: getattr(x, element_to_sort, date(2000, 1, 1))

        return ft.Container(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            header_name,
                            color=defaultFontColor,
                            size=15,
                            font_family="cupurum",
                            # bgcolor='blue'
                        ),
                        alignment=ft.alignment.bottom_left
                    ),

                    ft.Row(
                        controls=[
                            self.sort_arrow_cell,
                            ft.Container(
                                content=ft.Icon(name=ft.icons.ARROW_DROP_DOWN, size=20),
                                alignment=ft.alignment.bottom_right,
                                padding=0,
                                on_click=self._on_click_handler,
                                # bgcolor='green'
                            )
                        ],
                        spacing=0
                    )  # два элемента в строку, чтобы прижать к правому краю
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=0,
            width=width,
            # bgcolor='yellow',

        )

